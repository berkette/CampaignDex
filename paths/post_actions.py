import os
from settings import CAMPAIGN_DB, PATH_NEW, PATH_HOME, PATH_MANAGE
from settings import PATH_NOT_FOUND, PATH_ROOT
from settings import HOME_TEMPLATE, NEW_TEMPLATE
from settings import GETVAR_CAMPAIGN_NOT_FOUND
from settings import GETVAR_INVALID_PATH, GETVAR_INVALID_NAME
from settings import GETVAR_NAME_UNAVAILABLE, GETVAR_PATH_UNAVAILABLE
from settings import GETVAR_SAVE_SUCCESS
from settings import GETVAR_INVALID_TITLE
from db import delete_campaign, insert_campaign, query_campaign, update_campaign
from db import delete_page, insert_page, query_page, update_page
from db.exc import CampaignNotFoundError, InvalidNameError, NameUnavailableError
from db.exc import PageNotFoundError, PathUnavailableError
from db.helpers import get_rtf_fullpath
from db.models import Campaign

### Public ###

def destroy_campaign(form):
    campaign_id = form['campaign_id'].value
    redirect_path = PATH_ROOT
    try:
        delete_campaign(int(campaign_id))
    except CampaignNotFoundError:
        redirect_path = redirect_path + '?error=' + GETVAR_CAMPAIGN_NOT_FOUND
    return redirect_path

def open_campaign(form):
    campaign_id = form['campaign'].value
    try:
        campaign = query_campaign(campaign_id)
        redirect_path = PATH_HOME
        campaign_name = campaign.name
        db_name = campaign.db_name
        campaign_skin = campaign.skin
    except CampaignNotFoundError:
        redirect_path = PATH_ROOT + '?error=' + GEVAR_CAMPAIGN_NOT_FOUND
        campaign_name = ''
        db_name = ''
        campaign_skin = ''
    
    data = {
        'redirect_path': redirect_path,
        'id': str(campaign_id),
        'db': db_name,
        'name': campaign_name,
        'skin': campaign_skin
    }
    return data

def save_new_campaign(form):
    if 'name' in form:
        name = form['name'].value
        skin = form['skin'].value
        try:
            campaign_id = insert_campaign(name, skin=skin)
            campaign = query_campaign(campaign_id)

            # Make sure home page exists
            insert_page(
                campaign.db_name,
                PATH_HOME,
                title="Home",
                template=HOME_TEMPLATE
            )
            # Make sure new page form exists
            insert_page(
                campaign.db_name,
                PATH_NEW,
                title="Create a New Page",
                template=NEW_TEMPLATE
            )

            redirect_path = PATH_HOME
            db_name = campaign.db_name
            campaign_name = campaign.name
            campaign_skin = campaign.skin
        except NameUnavailableError:
            redirect_path = PATH_NEW + '?error=' +\
                GETVAR_NAME_UNAVAILABLE + '&name=' + name
            campaign_id = ''
            db_name = ''
            campaign_name = ''
            campaign_skin = ''
    else:
        redirect_path = PATH_NEW + '?error=' + GETVAR_INVALID_NAME
        campaign_id = ''
        db_name = ''
        campaign_name = ''
        campaign_skin = ''
    
    data = {
        'redirect_path': redirect_path,
        'id': str(campaign_id),
        'db': db_name,
        'name': campaign_name,
        'skin': campaign_skin
    }
    return data

def save_update_campaign(form):
    campaign_id = form['campaign_id'].value
    if 'name' in form:
        name = form['name'].value
        skin = form['skin'].value

        redirect_path = PATH_ROOT + '?message=' + GETVAR_SAVE_SUCCESS
        try:
            update_campaign(int(campaign_id), name=name, skin=skin)
        except CampaignNotFoundError:
            redirect_path = PATH_MANAGE + '?error=' + GETVAR_CAMPAIGN_NOT_FOUND
        except InvalidNameError:
            redirect_path = PATH_MANAGE + '?campaign_id=' + campaign_id +\
                '&error=' + GETVAR_INVALID_NAME
        except NameUnavailableError:
            redirect_path = PATH_MANAGE + '?campaign_id=' + campaign_id +\
                '&error=' + GETVAR_NAME_UNAVAILABLE
    else:
        redirect_path = PATH_MANAGE + '?campaign_id=' + campaign_id +\
            '&error=' + GETVAR_INVALID_NAME
    return redirect_path
        
##### Page #####

def apply_rtf(db_name, form):
    if 'rtf' in form:
        rtf_content = form['rtf'].value
    else:
        rtf_content = ''

    if 'path' in form:
        page_path = form['path'].value
        try:
            page = query_page(db_name, page_path)
            rtf_fullpath = get_rtf_fullpath(db_name, page.rtf)
            _overwrite_rtf(rtf_fullpath, rtf_content)
            redirect_path = page_path
        except PageNotFoundError:
            redirect_path = PATH_NOT_FOUND
    else:
        redirect_path = PATH_NOT_FOUND
    
    return redirect_path

def destroy_page(db_name, form):
    if 'path' in form:
        path = form['path'].value
        try:
            delete_page(db_name, path)
            redirect_path = PATH_HOME + '?message=' + GETVAR_SAVE_SUCCESS
        except PageNotFoundError:
            redirect_path = PATH_NOT_FOUND
    else:
        redirect_path = PATH_NOT_FOUND
        
    return redirect_path

def save_rtf(db_name, form):
    redirect_path = apply_rtf(db_name, form)
    if redirect_path != PATH_NOT_FOUND:
        redirect_path = redirect_path + '?edit=true&message=' + GETVAR_SAVE_SUCCESS
    return redirect_path

def save_new_page(db_name, form):
    if 'page_path' in form:
        path = form['page_path'].value
        if path[0] is not '/':
            path = '/' + path

        if not _valid_path(path):
            redirect_path = PATH_NEW + '?error=' + GETVAR_INVALID_PATH
        elif 'page_title' in form:
            title = form['page_title'].value
            try:
                insert_page(db_name, path, title=title)
                _create_superpage(db_name, path)
                redirect_path = path
            except PathUnavailableError:
                redirect_path = PATH_NEW + '?error=' + GETVAR_PATH_UNAVAILABLE
        else:
            redirect_path = PATH_NEW + '?error=' + GETVAR_INVALID_TITLE
    else:
        redirect_path = PATH_NEW + '?error=' + GETVAR_INVALID_PATH

    return redirect_path

def save_update_page(db_name, form):
    if 'original_path' in form:
        path = form['original_path'].value
        
        if 'page_path' in form:
            page_path = form['page_path'].value
            if page_path[0] is not '/':
                page_path = '/' + page_path

            if not _valid_path(page_path):
                redirect_path = path + '?manage=true&error=' + GETVAR_INVALID_PATH
            elif 'page_title' in form:
                title = form['page_title'].value
                try:
                    update_page(db_name, page_path, title=title)
                    _create_superpage(db_name, page_path)
                    redirect_path = page_path
                except PageNotFoundError:
                    redirect_path = PATH_NOT_FOUND
                except PathUnavailableError:
                    redirect_path = path + '?manage=true&error=' + GETVAR_PATH_UNAVAILABLE
            else:
                redirect_path = path + '?manage=true&error=' + GETVAR_INVALID_TITLE
        else:
            redirect_path = path + '?manage=true&error=' + GETVAR_INVALID_PATH
    else:
        redirect_path = PATH_NOT_FOUND

    return redirect_path


def toggle_quicklink(db_name, form):
    page_path = form['path'].value
    form_ql = form['quicklink'].value
    if form_ql == 'False':
        quicklink = True
    else:
        quicklink = False

    try:
        page = update_page(db_name, page_path, quicklink=quicklink)
        redirect_path = page_path + '?message=' + GETVAR_SAVE_SUCCESS
    except PageNotFoundError:
        redirect_path = PATH_NOT_FOUND

    return redirect_path

### Private ###

def _create_superpage(db_name, path):
    superpage_path = os.path.dirname(path)
    if path != PATH_HOME:
        try:
            query_page(db_name, superpage_path)
        except PageNotFoundError:
            insert_page(db_name, superpage_path)
        update_page(db_name, path, superpage_path=superpage_path)
        _create_superpage(db_name, superpage_path)

def _overwrite_rtf(filepath, content):
    rtf = open(filepath, 'w')
    rtf.write(content)
    rtf.close()

def _valid_path(path):
    return (os.path.commonprefix([path, PATH_HOME]) == PATH_HOME)
