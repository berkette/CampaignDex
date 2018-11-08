import os
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from db.exc import NameUnavailableError, UpdateUnspecifiedError
from db.exc import PageNotFoundError, PathUnavailableError
from db.models import Base, Campaign, Page
from settings import CAMPAIGN_DB, DB_DIR, DB_PREFIX, PAGE_TABLE_NAME
from settings import ROOT_DIR

### Public Methods ###

####################
##### Campaign #####
####################

def all_campaigns():
    (engine, session) = _start_session(CAMPAIGN_DB)
    
    campaigns = session.\
        query(Campaign.id, Campaign.name, Campaign.db_name).\
        order_by(Campaign.name).\
        all()

    _end_session(engine, session)
    return campaigns

def delete_campaign(id):
    (engine, session) = _start_session(CAMPAIGN_DB)

    try:
        campaign = session.query(Campaign).filter(Campaign.id == id).one()
    except NoResultFound:
        _end_session(engine, session)
        raise CampaignNotFoundError(id)
    
    db_to_del = ROOT_DIR + DB_DIR + campaign.db_name
    session.delete(campaign)
    session.flush()

    # Remove the campaign's page db
    os.remove(db_to_del)

    session.commit()
    _end_session(engine, session)

def insert_campaign(name, **kwargs):
    (engine, session) = _start_session(CAMPAIGN_DB)

    try:
        new_campaign = Campaign.new(name, **kwargs)
        session.add(new_campaign)
        session.flush()
    except IntegrityError:
        _end_session(engine, session)
        raise NameUnavailableError(name) 

    # create the campaign's db
    p_db_path = DB_PREFIX + ROOT_DIR + DB_DIR + new_campaign.db_name
    p_engine = create_engine(p_db_path)

    p_table = Base.metadata.tables[PAGE_TABLE_NAME]
    Base.metadata.create_all(p_engine, tables=[p_table])
    p_engine.dispose()

    new_id = new_campaign.id
    session.commit()
    _end_session(engine, session)

    return new_id

def query_campaign(id):
    (engine, session) = _start_session(CAMPAIGN_DB)
    
    try:
        campaign = session.query(Campaign).filter(Campaign.id == id).one()
        _end_session(engine, session)
    except NoResultFound:
        _end_session(engine, session)
        raise CampaignNotFoundError(id)

    return campaign

def update_campaign(id, name=None, skin=None):
    # Must specify at least one change
    if not (name or skin):
        raise UpdateUnspecifiedError

    (engine, session) = _start_session(CAMPAIGN_DB)
   
    # Get the campaign
    try:
        campaign = session.query(Campaign).filter(Campaign.id == id).one()
    except NoResultFound:
        _end_session(engine, session)
        raise CampaignNotFoundError(id)

    # Determine what needs to be changed
    if name:
        campaign.update_name(name)

    if skin:
        campaign.update_skin(skin)

    # Save changes
    try:
        session.commit()
        _end_session(engine, session)
    except IntegrityError:
        _end_session(engine, session)
        raise NameUnavailableError(name)

################
##### Page #####
################

def delete_page(db_name, page_path):
    (engine, session) = _start_session(db_name)

    try:
        page = session.query(Page).filter(Page.path == page_path).one()
    except NoResultFound:
        _end_session(engine, session)
        raise PageNotFoundError(page_path)

    # TODO: case where the page to delete has children

    session.delete(page)
    session.commit()
    _end_session(engine, session)
    

def insert_page(db_name, page_path, **kwargs):
    (engine, session) = _start_session(db_name)
    
    try:
        new_page = Page.new(page_path, **kwargs)
        session.add(new_page)
        session.flush()
    except IntegrityError:
        _end_session(engine, session)
        raise PathUnavailableError(page_path)

    session.commit()
    _end_session(engine, session)

def query_page(db_name, page_path):
    (engine, session) = _start_session(db_name)

    try:
        page = session.query(Page).filter(Page.path == page_path).one()
        _end_session(engine, session)
    except NoResultFound:
        _end_session(engine, session)
        raise PageNotFoundError(page_path) 

    return page

def update_page(db_name, page_path, **kwargs):
    (engine, session) = _start_session(db_name)
    
    try:
        page = session.query(Page).filter(Page.path == page_path).one()
        page.update(page_path, **kwargs)
        session.flush()
    except NoResultFound:
        _end_session(engine, session)
        raise PageNotFoundError(page_path)
    except IntegrityError:
        _end_session(engine, session)
        raise PathUnavailableError(page_path)
    
    session.commit()
    _end_session(engine, session)

def query_quicklinks(db_name):
    (engine, session) = _start_session(db_name)

    try:
        ql_pages = session.query(Page).filter(Page.quicklink == True).all()
    except NoResultFound:
        ql_pages = []

    quicklinks = []

    for ql_page in ql_pages:
        quicklinks.append({'path': ql_page.path, 'title': ql_page.title})

    _end_session(engine, session)
    return quicklinks

def query_subpages(db_name, page_path):
    (engine, session) = _start_session(db_name)

    try:
        page = session.query(Page).filter(Page.path == page_path).one()
    except NoResultFound:
        _end_session(engine, session)
        raise PageNotFoundError(page_path)

    subpages = []
    raw_subpages = page.subpages
    for subpage in raw_subpages:
        subpages.append({'path': subpage.path, 'title': subpage.title})

    _end_session(engine, session)
    return subpages


### Private Methods ###

def _start_session(db_name):
    db_path = DB_PREFIX + ROOT_DIR + DB_DIR + db_name
    engine = create_engine(db_path)
    Session = sessionmaker(bind=engine)
    session = Session()
    return (engine, session)

def _end_session(engine, session):
    session.close()
    engine.dispose()
