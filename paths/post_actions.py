import os
from settings import CAMPAIGN_DB, PATH_NEW, PATH_HOME, PATH_MANAGE
from settings import HOME_TEMPLATE, NEW_TEMPLATE
from settings import GETVAR_CAMPAIGN_NOT_FOUND, GETVAR_INVALID_NAME
from settings import GETVAR_NAME_UNAVAILABLE, GETVAR_PATH_UNAVAILABLE
from settings import GETVAR_SAVE_SUCCESS
from db import delete_campaign, insert_campaign, query_campaign, update_campaign
from db import insert_page
from db.exc import CampaignNotFoundError, InvalidNameError, NameUnavailableError
from db.exc import PageNotFoundError, PathUnavailableError
from db.models import Campaign

### Public ###

def destroy_campaign(form):
    campaign_id = form['campaign_id'].value
    redirect_path = PATH_HOME
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
        db_name = campaign.db_name
        db_skin = campaign.get_skin()
    except CampaignNotFoundError:
        redirect_path = '?error=' + GEVAR_CAMPAIGN_NOT_FOUND
        db_id = ''
        db_name = ''
        db_skin = ''
    
    data = {
        'redirect_path': redirect_path,
        'id': str(campaign_id),
        'db': db_name,
        'skin': db_skin
    }
    return data

def save_new_campaign(form):
    name = form['name'].value
    skin = form['skin'].value
    try:
        db_id = insert_campaign(name, skin=skin)
        campaign = query_campaign(db_id)

        # Make sure home page exists
        insert_page(
            campaign.db_name,
            PATH_HOME,
            name,
            template=HOME_TEMPLATE
        )
        # Make sure new page form exists
        insert_page(
            campaign.db_name,
            PATH_NEW,
            "Create a New Page",
            template=NEW_TEMPLATE
        )

        redirect_path = PATH_HOME
        db_name = campaign.db_name
        db_skin = campaign.get_skin()
    except NameUnavailableError:
        redirect_path = PATH_NEW + '?error=' + GETVAR_NAME_UNAVAILABLE
        db_id = ''
        db_name = ''
        db_skin = ''
    
    data = {
        'redirect_path': redirect_path,
        'id': str(db_id),
        'db': db_name,
        'skin': db_skin
    }
    return data

def save_update_campaign(form):
    campaign_id = form['campaign_id'].value
    name = form['name'].value
    skin = form['skin'].value

    redirect_path = PATH_HOME + '?message=' + GETVAR_SAVE_SUCCESS
    try:
        update_campaign(int(campaign_id), name=name, skin=skin)
    except CampaignNotFoundError:
        redirect_path = PATH_MANAGE + '?error=' + GETVAR_CAMPAIGN_NOT_FOUND
    except InvalidNameError:
        redirect_path = PATH_MANAGE + '?campaign_id=' + campaign_id + '&error=' + GETVAR_INVALID_NAME
    except NameUnavailableError:
        redirect_path = PATH_MANAGE + '?campaign_id=' + campaign_id + '&error=' + GETVAR_NAME_UNAVAILABLE
    return redirect_path
        

def save_page(db_name, form):
    path = form['page_path'].value
    if not path:
        path = '/'
    elif path[0] is not '/':
        path = '/' + path

    title = form['page_title'].value
    if 'page_body' in form:
        body = form['page_body'].value
    else:
        body = ''

    try:
        insert_page(db_name, path, title, body=body)
        _create_superpage(db_name, path)
        redirect_path = path
    except PathUnavailableError:
        redirect_path = PATH_NEW = '?error=' + GETVAR_PATH_UNAVAILABLE

    return redirect_path


### Private ###

def _create_superpage(db_name, path):
    superpage_path = os.path.dirname(path)
    if path is not superpage_path:
        try:
            query_page(db_name, superpage_path)
        except PageNotFoundError:
            insert_page(db_name, superpage_path)
        update_page(db_name, path, superpage_path=superpage_path)
        _create_superpage(db_name, superpage_path)

