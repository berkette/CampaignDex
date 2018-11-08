import os
from mako.template import Template
from mako.lookup import TemplateLookup
from db import all_campaigns, query_campaign, query_page
from db import query_quicklinks, query_subpages
from db.exc import PageNotFoundError
from db.helpers import get_rtf_fullpath
from db.models import Campaign, Page
from paths.post_actions import destroy_campaign, open_campaign
from paths.post_actions import save_new_campaign, save_update_campaign
from paths.post_actions import save_page, toggle_quicklink
from paths.post_actions import apply_rtf, save_rtf
from settings import PATH_EXIT, PATH_HOME, PATH_MANAGE, PATH_NEW
from settings import PATH_NOT_FOUND, PATH_QUILL, PATH_ROOT
from settings import GETVAR_CAMPAIGN_NOT_FOUND
from settings import GETVAR_INVALID_PATH, GETVAR_INVALID_NAME
from settings import GETVAR_NAME_UNAVAILABLE, GETVAR_PATH_UNAVAILABLE
from settings import GETVAR_SAVE_SUCCESS
from settings import GETVAR_INVALID_TITLE
from settings import POST_DELETE_CAMPAIGN, POST_OPEN_CAMPAIGN
from settings import POST_SAVE_CAMPAIGN, POST_UPDATE_CAMPAIGN
from settings import POST_APPLY_RTF, POST_SAVE_RTF
from settings import POST_SAVE_PAGE, POST_TOGGLE_QUICKLINK
from settings import CAMPAIGN_DB, DB_DIR
from settings import CAMPAIGN_HOME_TEMPLATE, CAMPAIGN_MANAGE_TEMPLATE
from settings import CAMPAIGN_NEW_TEMPLATE
from settings import HOME_TEMPLATE, NEW_TEMPLATE, PARTIALS_TEMPLATE
from settings import COMMON_JS
from settings import CSS_DIR, JS_DIR, ROOT_DIR, TEMPLATE_DIR, RTF_DIR
from settings import CSS_SUFFIX, JS_SUFFIX, TEMPLATE_SUFFIX
from settings import STATUS_OK, STATUS_NOT_FOUND
from settings import STATUS_REDIRECT, STATUS_SERVER_ERR
from settings import COOKIE_ID, COOKIE_DB, COOKIE_NAME, COOKIE_SKIN
from settings import SKIN_CAMPAIGN, SKIN_DEFAULT
from settings import PAGE_SKINS
from settings import QUILL_JS, QUILL_SNOW, QUILL_DIR

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

    wiki = (os.path.commonprefix([path, PATH_HOME]) == PATH_HOME)
    wiki_op = (path == PATH_NEW)

    if db_name and (wiki or wiki_op):
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

        if 'edit' in get_vars:
            template_name = "edit_" + template_name

        attributes = {
            'campaign_name': campaign_name,
            'cookie_id': COOKIE_ID,
            'cookie_db': COOKIE_DB,
            'cookie_name': COOKIE_NAME,
            'cookie_skin': COOKIE_SKIN,
            'css_filepath': _build_css_path(skin),
            'home_path': PATH_HOME,
            'js_common': COMMON_JS + JS_SUFFIX,
            'js_filepath': _build_js_path(page.template),
            'new_path': PATH_NEW,
            'partials_filepath': _build_template_filename(PARTIALS_TEMPLATE),
            'path_links': _build_path_links(page.path),
            'page_path': page.path,
            'quicklinks': quicklinks,
            'exit_path': PATH_EXIT,
            'subpages': subpages,
            'title': page.title
        }

        if path != PATH_NEW:
            attributes['rtf_content'] = _get_rtf_content(\
                db_name, page.rtf)
            attributes['db_name'] = db_name
            attributes['apply_page'] = POST_APPLY_RTF
            attributes['save_page'] = POST_SAVE_RTF
            attributes['quill_js'] = PATH_QUILL + QUILL_JS
            attributes['quill_snow'] = PATH_QUILL + QUILL_SNOW

        if path == PATH_NEW:
            if 'path' in get_vars:
                page_path_value = get_vars['path'][0]
            else:
                page_path_value = PATH_HOME

            attributes['save_page'] = POST_SAVE_PAGE
            attributes['page_path_value'] = page_path_value

        elif path != PATH_HOME:
            attributes['quicklink'] = page.quicklink
            attributes['superpage_path'] = os.path.dirname(page.path)
            attributes['toggle_quicklink'] = POST_TOGGLE_QUICKLINK

    elif db_name:
        # Probably a resource query
        set_cookie = []
        content_type = "text/html"
        content_length = None
        if os.path.commonprefix([path, PATH_QUILL]) == PATH_QUILL:
            # Looking for Quill resources
            if path == PATH_QUILL + QUILL_JS:
                status = 200
                content = _get_file_content(ROOT_DIR + QUILL_DIR + QUILL_JS)
                content_length = len(content)
                content_type = "text/javascript"
            elif path == PATH_QUILL + QUILL_SNOW:
                status = 200
                content = _get_file_content(ROOT_DIR + QUILL_DIR + QUILL_SNOW)
                content_length = len(content)
                content_type = "text/css"
                
        elif path == PATH_EXIT:
            # User is exiting a campaign
            status = STATUS_REDIRECT
            content = PATH_ROOT
            set_cookie.append((COOKIE_ID, ''))
            set_cookie.append((COOKIE_DB, ''))
            set_cookie.append((COOKIE_NAME, ''))
            set_cookie.append((COOKIE_SKIN, ''))

        else:
            status = STATUS_REDIRECT
            content = PATH_HOME

        data = {
            'status': status,
            'content': content,
            'content_length': content_length,
            'content_type': content_type,
            'set_cookie': set_cookie
        }

        return data

    else:
        # Means the user is looking at campaign selection/creation
        if path == PATH_ROOT:
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
                'home_path': PATH_ROOT,
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
                'home_path': PATH_ROOT,
                'css_filepath': _build_css_path(SKIN_CAMPAIGN),
                'js_filepath': _build_js_path(CAMPAIGN_NEW_TEMPLATE),
                'name': get_var_name,
                'save_campaign': POST_SAVE_CAMPAIGN,
                'skins': PAGE_SKINS
            }
            template_name = CAMPAIGN_NEW_TEMPLATE
        else:
            return {'status': STATUS_REDIRECT, 'content': PATH_ROOT}

    # Error messages to display after a POST
    if 'error' in get_vars:
        error = get_vars['error'][0]
        if error == GETVAR_CAMPAIGN_NOT_FOUND:
            attributes['error'] = 'The campaign couldn\'t be found'
        elif error == GETVAR_INVALID_PATH:
            attributes['error'] = 'The path must be a subpage of {}'.format(PATH_HOME)
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

    data = {
        'status': status,
        'content': content,
        'content_type': "text/html",
        'content_length': None,
        'set_cookie': ''
    }

    return data

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

    elif path == POST_APPLY_RTF:
        if COOKIE_DB in cookie:
            db_name = cookie[COOKIE_DB].value
            redirect_path = apply_rtf(db_name, form)
        else:
            redirect_path = PATH_NOT_FOUND
        
    elif path == POST_SAVE_RTF:
        if COOKIE_DB in cookie:
            db_name = cookie[COOKIE_DB].value
            redirect_path = save_rtf(db_name, form)
        else:
            redirect_path = PATH_NOT_FOUND

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
    if (os.path.commonprefix([path, PATH_HOME]) != PATH_HOME) or (path == PATH_HOME):
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

def _get_rtf_content(db_name, rtf):
    rtf_full_path = get_rtf_fullpath(db_name, rtf)
    if os.path.isfile(rtf_full_path):
        return _get_file_content(rtf_full_path)
    else:
        return ''

def _get_file_content(filepath):
    f = open(filepath)
    response = f.read()
    f.close()
    return response
