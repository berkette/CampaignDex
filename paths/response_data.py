import os
from mako.template import Template
from mako.lookup import TemplateLookup
from db import all_campaigns, query_campaign, query_campaign_by_db_name, get_db_names
from db import  query_page, query_quicklinks, query_subpages
from db.exc import CampaignNotFoundError, PageNotFoundError, DatabaseNotFoundError
from db.helpers import get_rtf_fullpath
from db.models import Campaign, Page
from paths.post_actions import destroy_campaign, open_campaign
from paths.post_actions import save_new_campaign, save_update_campaign
from paths.post_actions import destroy_page, save_new_page, save_update_page
from paths.post_actions import toggle_quicklink
from paths.post_actions import apply_rtf, save_rtf
from settings import PATH_ERROR, PATH_EXIT, PATH_HOME, PATH_IMAGES, PATH_JQUERY
from settings import PATH_MANAGE, PATH_NEW, PATH_NOT_FOUND, PATH_QUILL
from settings import PATH_ROOT, PATH_RTF
from settings import GETVAR_CAMPAIGN_NOT_FOUND
from settings import GETVAR_INVALID_PATH, GETVAR_INVALID_NAME
from settings import GETVAR_NAME_UNAVAILABLE, GETVAR_PATH_UNAVAILABLE
from settings import GETVAR_SAVE_SUCCESS
from settings import GETVAR_INVALID_TITLE
from settings import GETVAR_NO_PATH, GETVAR_PAGE_NOT_FOUND
from settings import POST_DELETE_CAMPAIGN, POST_OPEN_CAMPAIGN
from settings import POST_SAVE_CAMPAIGN, POST_UPDATE_CAMPAIGN
from settings import POST_APPLY_RTF, POST_SAVE_RTF
from settings import POST_DELETE_PAGE, POST_SAVE_PAGE, POST_TOGGLE_QUICKLINK
from settings import POST_UPDATE_PAGE
from settings import CAMPAIGN_DB, DB_DIR
from settings import CAMPAIGN_HOME_TEMPLATE, CAMPAIGN_MANAGE_TEMPLATE
from settings import CAMPAIGN_NEW_TEMPLATE
from settings import EDIT_TEMPLATE, ERROR_TEMPLATE, HOME_TEMPLATE, NEW_TEMPLATE
from settings import PARTIALS_TEMPLATE, MANAGE_TEMPLATE_PREFIX
from settings import COMMON_JS
from settings import CSS_DIR, JS_DIR, ROOT_DIR, TEMPLATE_DIR, RTF_DIR
from settings import CSS_SUFFIX, JS_SUFFIX, TEMPLATE_SUFFIX
from settings import STATUS_OK, STATUS_NOT_FOUND
from settings import STATUS_REDIRECT, STATUS_SERVER_ERR
from settings import COOKIE_DB
from settings import SKIN_CAMPAIGN, SKIN_DEFAULT
from settings import PAGE_SKINS
from settings import IMAGES_DIR
from settings import JQUERY_JS, JQUERY_DIR
from settings import QUILL_JS, QUILL_SNOW, QUILL_DIR

### Public ###

def get_response_data(path, *, cookie=None, get_vars={}):
    # server.py calls this method, so don't change the name. Should
    # return a dictionary with keys 'status' (int) and 'content' (string)

    # Default response values
    status = STATUS_OK
    content = None
    content_type = "text/html"
    content_length = None
    redirect_path = None
    set_cookie = []

    # Internal build options
    build_response = True   # Whether the response will be built from a template
    reset_cookies = False   # Whether cookies will be cleared
    display_error_page = False # Whether something bad happened

    try:
        # Cookie values
        cookie_db_val = False

        if cookie and (COOKIE_DB in cookie):
            # Is it a valid db_name
            if cookie[COOKIE_DB].value in get_db_names():
                # Campaign's db name
                cookie_db_val = cookie[COOKIE_DB].value
                try:
                    campaign = query_campaign_by_db_name(cookie_db_val)
                except CampaignNotFoundError as e:
                    display_error_page = True
                    error_page_message = str(e)
            else:
                # There is an invalid db_name stored in a cookie
                reset_cookies = True    # Probably an out-of-date browser session

        # GET variables
        getvar_campaign_id = False
        getvar_edit = False
        getvar_error = False
        getvar_manage = False
        getvar_message = False
        getvar_name = ''
        getvar_path = False

        if 'campaign_id' in get_vars:
            getvar_campaign_id = int(get_vars['campaign_id'][0])
        if 'edit' in get_vars:
            getvar_edit = True
        if 'error' in get_vars:
            getvar_error = get_vars['error'][0]
        if 'manage' in get_vars:
            getvar_manage = True
        if 'message' in get_vars:
            getvar_message = get_vars['message'][0]
        if 'name' in get_vars:
            getvar_name = get_vars['name'][0]
        if 'path' in get_vars:
            getvar_path = get_vars['path'][0]

        # Check if the path is /new or a subpage of /wiki
        wiki = _is_subpage(path, PATH_HOME)
        wiki_new = (path == PATH_NEW)
        wiki_error = (path == PATH_ERROR)
        wiki_not_found = (path == PATH_NOT_FOUND)
        wiki_op = wiki_new or wiki_error or wiki_not_found

        if cookie_db_val and (wiki or wiki_op):
            # Means the user is looking at a specific campaign's pages
            try:
                page = query_page(cookie_db_val, path)
                subpages = query_subpages(cookie_db_val, path)
            except PageNotFoundError:
                # Give a pretty 404 Not Found Page
                page = Page.page_not_found(path)
                subpages = []

            quicklinks = query_quicklinks(cookie_db_val)
            status = page.status
            template_name = page.template

            attributes = {  # attributes that apply to all pages
                'campaign_name': campaign.name,
                'css_filepath': _build_css_path(campaign.skin),
                'home_path': PATH_HOME,
                'jquery_js': PATH_JQUERY + JQUERY_JS,
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

            if wiki:
                # Home or /wiki subpage
                attributes['rtf'] = PATH_RTF + page.rtf
                attributes['quill_js'] = PATH_QUILL + QUILL_JS
                attributes['quill_snow'] = PATH_QUILL + QUILL_SNOW
                attributes['apply_page'] = POST_APPLY_RTF
                attributes['save_page'] = POST_SAVE_RTF
                if getvar_edit:
                    # Means the user wants to edit quill content
                    template_name = EDIT_TEMPLATE
                elif getvar_manage:
                    # Means the user wants to manage the page
                    template_name = MANAGE_TEMPLATE_PREFIX + template_name
                    if getvar_path:
                        page_path_value = getvar_path
                    else:
                        page_path_value = path

                    attributes['save_page'] = POST_UPDATE_PAGE
                    attributes['page_path_value'] = page_path_value


            if wiki_new:
                # /new
                if getvar_path:
                    # Presets a path for the form
                    page_path_value = getvar_path
                else:
                    page_path_value = PATH_HOME

                attributes['save_page'] = POST_SAVE_PAGE
                attributes['page_path_value'] = page_path_value

            elif path != PATH_HOME:
                # /wiki subpage view
                attributes['delete_page'] = POST_DELETE_PAGE
                attributes['quicklink'] = page.quicklink
                attributes['superpage_path'] = os.path.dirname(page.path)
                attributes['toggle_quicklink'] = POST_TOGGLE_QUICKLINK

        elif path == PATH_JQUERY + JQUERY_JS:
            # Asking for the jquery library
            build_response = False
            content = _get_file_content(ROOT_DIR + JQUERY_DIR + JQUERY_JS)
            content_length = _byte_len(content)
            content_type = "application/javascript"

        elif _is_subpage(path, PATH_QUILL):
            # Looking for Quill resources
            build_response = False
            if path == PATH_QUILL + QUILL_JS:
                # quill.js
                content = _get_file_content(ROOT_DIR + QUILL_DIR + QUILL_JS)
                content_length = _byte_len(content)
                content_type = "application/javascript"
            elif path == PATH_QUILL + QUILL_SNOW:
                # quill.snow.css
                content = _get_file_content(ROOT_DIR + QUILL_DIR + QUILL_SNOW)
                content_length = _byte_len(content)
                content_type = "text/css"

        elif _is_subpage(path, PATH_IMAGES):
            # Looking for an image
            build_response = False
            image_name = os.path.basename(path)
            content = _get_file_content(ROOT_DIR + IMAGES_DIR + image_name, True)
            content_length = len(content)
            content_type = "image/" + os.path.splitext(image_name)[1][1:]

        elif cookie_db_val:
            build_response = False
            # Probably RTF query or exit
            if _is_subpage(path, PATH_RTF):
                # Looking for rtf page contents
                content = _get_file_content(ROOT_DIR + RTF_DIR + \
                    _get_rtf_filepath(cookie_db_val, path))
                content_length = _byte_len(content)
                content_type = "application/json"
                    
            elif path == PATH_EXIT:
                # User is exiting a campaign
                status = STATUS_REDIRECT
                redirect_path = PATH_ROOT
                reset_cookies = True

            else:
                # Any other URL gets redirected to /wiki
                status = STATUS_REDIRECT
                redirect_path = PATH_HOME

        else:
            # Means the user is looking at campaign selection/creation
            if path == PATH_ROOT:
                attributes = {
                    'campaigns': all_campaigns(),
                    'css_filepath': _build_css_path(SKIN_CAMPAIGN),
                    'js_filepath': _build_js_path(CAMPAIGN_HOME_TEMPLATE),
                    'manage_path': PATH_MANAGE,
                    'new_path': PATH_NEW,
                    'open_campaign': POST_OPEN_CAMPAIGN
                }
                template_name = CAMPAIGN_HOME_TEMPLATE

            elif path == PATH_MANAGE and getvar_campaign_id:
                campaign = query_campaign(getvar_campaign_id)
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
                attributes = {
                    'home_path': PATH_ROOT,
                    'css_filepath': _build_css_path(SKIN_CAMPAIGN),
                    'js_filepath': _build_js_path(CAMPAIGN_NEW_TEMPLATE),
                    'name': getvar_name,
                    'save_campaign': POST_SAVE_CAMPAIGN,
                    'skins': PAGE_SKINS
                }
                template_name = CAMPAIGN_NEW_TEMPLATE

            else:
                build_response = False
                status = STATUS_REDIRECT
                redirect_path = PATH_ROOT

        # Error messages to display after a POST
        if getvar_error == GETVAR_CAMPAIGN_NOT_FOUND:
            attributes['error'] = 'The campaign couldn\'t be found'
        elif getvar_error == GETVAR_INVALID_PATH:
            attributes['error'] = 'The path must be a subpage of {}'.format(PATH_HOME)
        elif getvar_error == GETVAR_INVALID_NAME:
            attributes['error'] = 'The campaign must have a name'
        elif getvar_error == GETVAR_INVALID_TITLE:
            attributes['error'] = 'The page must have a title'
        elif getvar_error == GETVAR_NAME_UNAVAILABLE:
            attributes['error'] = 'A campaign with this name already exists'
        elif getvar_error == GETVAR_NO_PATH:
            attributes['error'] = 'Form submission did not include a value for path'
        elif getvar_error == GETVAR_PATH_UNAVAILABLE:
            attributes['error'] = 'A page at this path already exists'
        elif getvar_error == GETVAR_PAGE_NOT_FOUND:
            attributes['error'] = 'Could not find the page you tried to change'

        # Non-error messages
        if getvar_message == GETVAR_SAVE_SUCCESS:
            attributes['message'] = 'Changes successfully saved'

    except DatabaseNotFoundError as e:
        display_error_page = True
        error_page_message = str(e)

    
    # If something went wrong, display an "Internal Server Error" page
    if display_error_page:
        template_name = ERROR_TEMPLATE
        build_response = True
        attributes = {
            'error': error_page_message,
            'css_filepath': _build_css_path(SKIN_CAMPAIGN)
        }

    # Build the response content from a template
    if build_response:
        try:
            template_lookup = TemplateLookup(directories=[_build_template_dir()])
            template_filename = _build_template_filename(template_name)
            template = template_lookup.get_template(template_filename)
            content = template.render(attributes=attributes)
        except FileNotFoundError:
            status = STATUS_SERVER_ERR
            content = 'FileNotFoundError: Could not locate the template {}'.format(template_name)

    # Reset cookies
    if reset_cookies:
        set_cookie = _clear_cookies(set_cookie)

    data = {
        'status': status,
        'content': content,
        'content_type': content_type,
        'content_length': content_length,
        'redirect_path': redirect_path,
        'set_cookie': set_cookie
    }
    return data

################
##### POST #####
################

def post_action(path, form, *, cookie=None, get_vars={}):
    # Handles POST requests
    set_cookie = []

    if path == POST_DELETE_CAMPAIGN:
        redirect_path = destroy_campaign(form)

    elif path == POST_OPEN_CAMPAIGN:
        data = open_campaign(form)
        redirect_path = data['redirect_path']
        set_cookie.append((COOKIE_DB, data['db']))
            
    elif path == POST_SAVE_CAMPAIGN:
        data = save_new_campaign(form)
        redirect_path = data['redirect_path']
        set_cookie.append((COOKIE_DB, data['db']))

    elif path == POST_UPDATE_CAMPAIGN:
        redirect_path = save_update_campaign(form)

    elif cookie and (COOKIE_DB in cookie):
        # Post comes from campaign-specific path
        cookie_db_val = cookie[COOKIE_DB].value
        if cookie_db_val in get_db_names():
            # Must be a valid db_name
            if path == POST_APPLY_RTF:
                redirect_path = apply_rtf(cookie_db_val, form)
            elif path == POST_DELETE_PAGE:
                redirect_path = destroy_page(cookie_db_val, form)
            elif path == POST_SAVE_RTF:
                redirect_path = save_rtf(cookie_db_val, form)
            elif path == POST_SAVE_PAGE:
                redirect_path = save_new_page(cookie_db_val, form)
            elif path == POST_TOGGLE_QUICKLINK:
                redirect_path = toggle_quicklink(cookie_db_val, form)
            elif path == POST_UPDATE_PAGE:
                redirect_path = save_update_page(cookie_db_val, form)
            else:
                redirect_path = PATH_NOT_FOUND
        else:
            redirect_path = PATH_NOT_FOUND
            set_cookie = _clear_cookies(set_cookie)

    else:
        redirect_path = PATH_NOT_FOUND

    return (redirect_path, set_cookie)


### Private ###

def _build_css_path(template_name):
    return CSS_DIR + template_name + CSS_SUFFIX

def _build_js_path(template_name):
    return JS_DIR + template_name + JS_SUFFIX

def _build_path_links(path):
    if (not _is_subpage(path, PATH_HOME)) or (path == PATH_HOME):
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

def _byte_len(str):
    return len(str.encode('utf-8'))

def _clear_cookies(set_cookie):
    set_cookie.append((COOKIE_DB, ''))
    return set_cookie

def _get_file_content(filepath, image=False):
    if os.path.isfile(filepath):
        if image:
            f = open(filepath, 'rb')
        else:
            f = open(filepath, 'r')
        response = f.read()
        f.close()
    else:
        response = ''
    return response

def _get_rtf_filepath(db_name, rtf):
    return os.path.splitext(db_name)[0] + '/' + os.path.basename(rtf)

def _is_subpage(path, superpage_path):
    return os.path.commonprefix([path, superpage_path]) == superpage_path
