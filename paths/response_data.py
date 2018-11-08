import os
from mako.template import Template
from mako.lookup import TemplateLookup
from db import all_campaigns, query_campaign, query_page
from db import query_quicklinks, query_subpages
from db.exc import PageNotFoundError
from db.models import Campaign, Page
from paths.post_actions import destroy_campaign, open_campaign, save_new_campaign
from paths.post_actions import save_update_campaign, save_page, toggle_quicklink
from settings import PATH_HOME, PATH_MANAGE, PATH_NEW, PATH_NOT_FOUND
from settings import GETVAR_CAMPAIGN_NOT_FOUND, GETVAR_INVALID_NAME
from settings import GETVAR_NAME_UNAVAILABLE, GETVAR_PATH_UNAVAILABLE
from settings import GETVAR_SAVE_SUCCESS
from settings import GETVAR_INVALID_TITLE
from settings import POST_DELETE_CAMPAIGN, POST_OPEN_CAMPAIGN
from settings import POST_SAVE_CAMPAIGN, POST_UPDATE_CAMPAIGN
from settings import POST_SAVE_PAGE, POST_TOGGLE_QUICKLINK
from settings import CAMPAIGN_DB, DB_DIR
from settings import CAMPAIGN_HOME_TEMPLATE, CAMPAIGN_MANAGE_TEMPLATE
from settings import CAMPAIGN_NEW_TEMPLATE
from settings import HOME_TEMPLATE, NEW_TEMPLATE, PARTIALS_TEMPLATE
from settings import COMMON_JS
from settings import CSS_DIR, JS_DIR, ROOT_DIR, TEMPLATE_DIR
from settings import CSS_SUFFIX, JS_SUFFIX, TEMPLATE_SUFFIX
from settings import STATUS_OK, STATUS_NOT_FOUND
from settings import STATUS_REDIRECT, STATUS_SERVER_ERR
from settings import COOKIE_ID, COOKIE_DB, COOKIE_NAME, COOKIE_SKIN
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
            campaign_name = cookie[COOKIE_NAME].value
            db_name = cookie[COOKIE_DB].value
            skin = cookie[COOKIE_SKIN].value

    if db_name:
        # Means the user is looking at a specific campaign
        try:
            page = query_page(db_name, path)
            subpages = query_subpages(db_name, path)
        except PageNotFoundError:
            page = Page.page_not_found(path)
            subpages = []

        quicklinks = query_quicklinks(db_name)
        status = page.status
        template_name = page.template

        attributes = {
            'campaign_name': campaign_name,
            'cookie_id': COOKIE_ID,
            'cookie_db': COOKIE_DB,
            'cookie_name': COOKIE_NAME,
            'cookie_skin': COOKIE_SKIN,
            'css_filepath': _build_css_path(skin),
            'home_path': PATH_HOME,
            'js_common': COMMON_JS + JS_SUFFIX,
            'js_filepath': _build_js_path(template_name),
            'new_path': PATH_NEW,
            'partials_filepath': _build_template_filename(PARTIALS_TEMPLATE),
            'path_links': _build_path_links(page.path),
            'quicklinks': quicklinks,
            'subpages': subpages,
            'superpage_path': os.path.dirname(page.path),
            'title': page.title
        }

        if path == PATH_NEW:
            if 'path' in get_vars:
                page_path_value = get_vars['path'][0]
            else:
                page_path_value = ''

            attributes['save_page'] = POST_SAVE_PAGE
            attributes['page_path_value'] = page_path_value
        elif path != PATH_HOME:
            attributes['page_path'] = page.path
            attributes['quicklink'] = page.quicklink
            attributes['toggle_quicklink'] = POST_TOGGLE_QUICKLINK

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
                'campaign_skin': campaign.skin,
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
            return {'status': STATUS_REDIRECT, 'content': PATH_HOME}

    # Error messages to display after a POST
    if 'error' in get_vars:
        error = get_vars['error'][0]
        if error == GETVAR_CAMPAIGN_NOT_FOUND:
            attributes['error'] = 'The campaign couldn\'t be found'
        elif error == GETVAR_INVALID_NAME:
            attributes['error'] = 'The campaign must have a name'
        elif error == GETVAR_INVALID_TITLE:
            attributes['error'] = 'The page must have a title'
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
        set_cookie.append((COOKIE_NAME, data['name']))
        set_cookie.append((COOKIE_SKIN, data['skin']))
            
    elif path == POST_SAVE_CAMPAIGN:
        data = save_new_campaign(form)
        redirect_path = data['redirect_path']
        set_cookie.append((COOKIE_ID, data['id']))
        set_cookie.append((COOKIE_DB, data['db']))
        set_cookie.append((COOKIE_NAME, data['name']))
        set_cookie.append((COOKIE_SKIN, data['skin']))

    elif path == POST_UPDATE_CAMPAIGN:
        redirect_path = save_update_campaign(form)

    elif path == POST_SAVE_PAGE:
        if COOKIE_DB in cookie:
            db_name = cookie[COOKIE_DB].value
            redirect_path = save_page(db_name, form)
        else:
            redirect_path = PATH_NOT_FOUND

    elif path == POST_TOGGLE_QUICKLINK:
        if COOKIE_DB in cookie:
            db_name = cookie[COOKIE_DB].value
            redirect_path = toggle_quicklink(db_name, form)
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

def _build_path_links(path):
    if path == '/':
        path_links = []
    else:
        path_links = _build_path_links(os.path.dirname(path))
        path_links.append({
            'path': path,
            'basename': os.path.basename(path)
        })
    return path_links

def _build_template_dir():
    return ROOT_DIR + TEMPLATE_DIR

def _build_template_filename(template_name):
    return template_name + TEMPLATE_SUFFIX

