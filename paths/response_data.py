from mako.template import Template
from mako.lookup import TemplateLookup
from db import all_campaigns, query_campaign, query_page
from db.exc import PageNotFoundError
from db.models import Campaign, Page
from paths.post_actions import destroy_campaign, open_campaign, save_new_campaign
from paths.post_actions import save_update_campaign, save_page
from settings import PATH_HOME, PATH_MANAGE, PATH_NEW, PATH_NOT_FOUND
from settings import GETVAR_CAMPAIGN_NOT_FOUND, GETVAR_INVALID_NAME
from settings import GETVAR_NAME_UNAVAILABLE, GETVAR_PATH_UNAVAILABLE
from settings import GETVAR_SAVE_SUCCESS
from settings import POST_DELETE_CAMPAIGN, POST_OPEN_CAMPAIGN
from settings import POST_SAVE_CAMPAIGN, POST_UPDATE_CAMPAIGN
from settings import POST_SAVE_PAGE
from settings import CAMPAIGN_DB, DB_DIR
from settings import CAMPAIGN_BASE_TEMPLATE
from settings import CAMPAIGN_HOME_TEMPLATE, CAMPAIGN_MANAGE_TEMPLATE
from settings import CAMPAIGN_NEW_TEMPLATE
from settings import BASE_TEMPLATE, HOME_TEMPLATE, NEW_TEMPLATE
from settings import CSS_DIR, JS_DIR, ROOT_DIR, TEMPLATE_DIR
from settings import CSS_SUFFIX, JS_SUFFIX, TEMPLATE_SUFFIX
from settings import STATUS_OK, STATUS_NOT_FOUND
from settings import STATUS_REDIRECT, STATUS_SERVER_ERR
from settings import COOKIE_ID, COOKIE_DB, COOKIE_SKIN
from settings import SKIN_CAMPAIGN, SKIN_DEFAULT
from settings import PAGE_SKINS

### Public ###

def get_response_data(path, *, cookie=None, get_vars={}):
    # server.py calls this method, so don't change the name. Should
    # return a dictionary with keys 'status' (int) and 'content' (string)
    campaign_id = None
    db_name = None
    skin = SKIN_DEFAULT

    if cookie:
        if COOKIE_ID in cookie:
            campaign_id = cookie[COOKIE_ID].value
            db_name = cookie[COOKIE_DB].value
            skin = cookie[COOKIE_SKIN].value

    if db_name:
        # Means the user is looking at a specific campaign
        try:
            page = query_page(db_name, path)
        except PageNotFoundError:
            page = Page.page_not_found(path)

        status = page.status
        attributes = page.get_content()
        template_name = page.template

    else:
        # Means the user is looking at campaign selection/creation
        if path == PATH_HOME:
            status = STATUS_OK
            attributes = {
                'campaigns': all_campaigns(),
                'css_filepath': _build_css_path(SKIN_CAMPAIGN),
                'js_filepath': _build_js_path(CAMPAIGN_HOME_TEMPLATE),
                'manage_path': PATH_MANAGE,
                'new_path': PATH_NEW,
                'open_campaign': POST_OPEN_CAMPAIGN
            }
            template_name = CAMPAIGN_HOME_TEMPLATE
        elif path == PATH_MANAGE:
            campaign = query_campaign(int(get_vars['campaign_id'][0]))
            status = STATUS_OK
            attributes = {
                'campaign_id': campaign.id,
                'campaign_name': campaign.name,
                'campaign_skin': campaign.get_skin(),
                'css_filepath': _build_css_path(SKIN_CAMPAIGN),
                'delete_campaign': POST_DELETE_CAMPAIGN,
                'home_path': PATH_HOME,
                'js_filepath': _build_js_path(CAMPAIGN_MANAGE_TEMPLATE),
                'update_campaign': POST_UPDATE_CAMPAIGN,
                'skins': PAGE_SKINS
            }
            template_name = CAMPAIGN_MANAGE_TEMPLATE
        elif path == PATH_NEW:
            if 'name' in get_vars:
                get_var_name = get_vars['name'][0]
            else:
                get_var_name = ''
            status = STATUS_OK
            attributes = {
                'home_path': PATH_HOME,
                'css_filepath': _build_css_path(SKIN_CAMPAIGN),
                'js_filepath': _build_js_path(CAMPAIGN_NEW_TEMPLATE),
                'name': get_var_name,
                'save_campaign': POST_SAVE_CAMPAIGN,
                'skins': PAGE_SKINS
            }
            template_name = CAMPAIGN_NEW_TEMPLATE
        else:
            page = Page.page_not_found(path)
            status = page.status
            attributes = page.get_content()
            template_name = page.template

    # Error messages to display after a POST
    if 'error' in get_vars:
        error = get_vars['error'][0]
        if error == GETVAR_CAMPAIGN_NOT_FOUND:
            attributes['error'] = 'The campaign couldn\'t be found'
        elif error == GETVAR_INVALID_NAME:
            attributes['error'] = 'The campaign must have a name'
        elif error == GETVAR_NAME_UNAVAILABLE:
            attributes['error'] = 'A campaign with this name already exists'
        elif error == GETVAR_PATH_UNAVAILABLE:
            attributes['error'] = 'A page at this path already exists'

    if 'message' in get_vars:
        message = get_vars['message'][0]
        if message == GETVAR_SAVE_SUCCESS:
            attributes['message'] = 'Changes successfully saved'

    # Build the response content    
    try:
        template_lookup = TemplateLookup(directories=[_build_template_dir()])
        template_filename = _build_template_filename(template_name)
        template = template_lookup.get_template(template_filename)
        content = template.render(attributes=attributes)
    except FileNotFoundError:
        status = STATUS_SERVER_ERR
        content = 'FileNotFoundError: Could not locate the template {}'.format(template_name)

    return {'status': status, 'content': content}

def post_action(path, form, cookie=None):
    set_cookie = []

    if path == POST_DELETE_CAMPAIGN:
        redirect_path = destroy_campaign(form)

    elif path == POST_OPEN_CAMPAIGN:
        data = open_campaign(form)
        redirect_path = data['redirect_path']
        set_cookie.append((COOKIE_ID, data['id']))
        set_cookie.append((COOKIE_DB, data['db']))
        set_cookie.append((COOKIE_SKIN, data['skin']))
            
    elif path == POST_SAVE_CAMPAIGN:
        data = save_new_campaign(form)
        redirect_path = data['redirect_path']
        set_cookie.append((COOKIE_ID, data['id']))
        set_cookie.append((COOKIE_DB, data['db']))
        set_cookie.append((COOKIE_SKIN, data['skin']))

    elif path == POST_UPDATE_CAMPAIGN:
        redirect_path = save_update_campaign(form)

    elif path == POST_SAVE_PAGE:
        if COOKIE_DB in cookie:
            db_name = cookie[COOKIE_DB].value
            redirect_path = save_page(db_name, form)
        else:
            redirect_path = PATH_NOT_FOUND

    else:
        redirect_path = PATH_NOT_FOUND

    return (redirect_path, set_cookie)


### Private ###

def _build_css_path(template_name):
    return CSS_DIR + template_name + CSS_SUFFIX

def _build_js_path(template_name):
    return JS_DIR + template_name + JS_SUFFIX

def _build_template_dir():
    return ROOT_DIR + TEMPLATE_DIR

def _build_template_filename(template_name):
    return template_name + TEMPLATE_SUFFIX

