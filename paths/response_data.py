from mako.template import Template
from db import all_campaigns, query_page
from db.exc import PageNotFoundError
from db.models import Campaign, Page
from paths.post_actions import open_campaign, save_campaign
from paths.post_actions import save_page
from settings import CAMPAIGN_DB, DB_DIR, ROOT_DIR, TEMPLATE_DIR
from settings import TEMPLATE_SUFFIX
from settings import CAMPAIGN_HOME_TEMPLATE, CAMPAIGN_NEW_TEMPLATE
from settings import PATH_HOME, PATH_NOT_FOUND
from settings import STATUS_OK, STATUS_NOT_FOUND
from settings import STATUS_REDIRECT, STATUS_SERVER_ERR
from settings import COOKIE_ID, COOKIE_DB, COOKIE_SKIN
from settings import SKIN_DEFAULT

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
        template_path = _build_template_path(page.template)

    else:
        # Means the user is looking at campaign selection/creation
        if path == PATH_HOME:
            status = STATUS_OK
            attributes = {
                'campaigns': all_campaigns()
            }
            template_path = _build_template_path(CAMPAIGN_HOME_TEMPLATE)
        elif path == PATH_NEW:
            status = STATUS_OK
            attributes = {}
            template_path = _build_template_path(CAMPAIGN_NEW_TEMPLATE)
        else:
            page = Page.page_not_found(path)
            status = page.status
            attributes = page.get_content()
            template_path = _build_template_path(page.template)

    # Error messages to display after a POST
    if 'error' in get_vars:
        error = get_vars['error'][0]
        if error == 'name_unavailable':
            attributes['error'] = 'A campaign with this name already exists'
        elif error == 'path_unavailable':
            attributes['error'] = 'A page at this path already exists'

    # Build the response content    
    try:
        template = Template(filename=template_path)
        content = template.render(attributes=attributes)
    except FileNotFoundError:
        status = STATUS_SERVER_ERR
        content = 'FileNotFoundError: Could not locate the template {}'.format(template_path)

    return {'status': status, 'content': content}

def post_action(path, form, cookie=None):
    set_cookie = []

    if path == '/open_campaign':
        if form['campaign'].value == 'new':
            redirect_path = PATH_NEW
        else:
            data = open_campaign(form)
            redirect_path = data['redirect_path']
            set_cookie.append((COOKIE_ID, data['id']))
            set_cookie.append((COOKIE_DB, data['db']))
            set_cookie.append((COOKIE_SKIN, data['skin']))
            
    elif path == '/save_campaign':
        data = save_campaign(form)
        redirect_path = data['redirect_path']
        set_cookie.append((COOKIE_ID, data['id']))
        set_cookie.append((COOKIE_DB, data['db']))
        set_cookie.append((COOKIE_SKIN, data['skin']))

    elif path == '/save_page':
        if COOKIE_DB in cookie:
            db_name = cookie[COOKIE_DB].value
            redirect_path = save_page(db_name, form)
        else:
            redirect_path = PATH_NOT_FOUND

    else:
        redirect_path = PATH_NOT_FOUND

    return (redirect_path, set_cookie)


### Private ###

def _build_template_path(template_name):
    return ROOT_DIR + TEMPLATE_DIR + template_name + TEMPLATE_SUFFIX

