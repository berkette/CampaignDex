import os
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from db.exc import PageNotFoundError, PathUnavailableError
from db.models import Base, Campaign, Page
from settings import CAMPAIGN_DB, DB_DIR, DB_PREFIX, PAGE_TABLE_NAME

### Private Methods

def _start_session(db_path):
    engine = create_engine(DB_PREFIX + db_path)
    Session = sessionmaker(bind=engine)
    session = Session()
    return (engine, session)

def _end_session(engine, session):
    session.close()
    engine.dispose()


### Public Methods

##### Campaign #####
def all_campaigns():
    (engine, session) = _start_session(DB_DIR + CAMPAIGN_DB)
    
    campaigns = session.\
        query(Campaign.id, Campaign.name, Campaign.db_name).\
        all()

    _end_session(engine, session)
    return campaigns

def delete_campaign(id):
    (engine, session) = _start_session(DB_DIR + CAMPAIGN_DB)

    try:
        campaign = session.query(Campaign).filter(Campaign.id == id).one()
    except NoResultFound:
        _end_session(engine, session)
        raise CampaignNotFoundError(id)
    
    db_to_del = campaign.db_name
    session.delete(campaign)
    session.flush()

    # Remove the campaign's page db
    os.remove(DB_DIR + db_to_del)

    session.commit()
    _end_session(engine, session)

def insert_campaign(name, **kwargs):
    (engine, session) = _start_session(DB_DIR + CAMPAIGN_DB)

    try:
        new_campaign = Campaign.new(name, **kwargs)
        session.add(new_campaign)
        session.flush()
    except IntegrityError:
        _end_session(engine, session)
        raise NameUnavailableError(name) 

    # create the campaign's db
    p_engine = create_engine(DB_PREFIX + DB_DIR + new_campaign.db_name)

    p_table = Base.metadata.tables[PAGE_TABLE_NAME]
    Base.metadata.create_all(p_engine, tables=[p_table])
    p_engine.dispose()

    session.commit()
    _end_session(engine, session)

def query_campaign(id):
    (engine, session) = _start_session(DB_DIR + CAMPAIGN_DB)
    
    try:
        campaign = session.query(Campaign).filter(Campaign.id == id).one()
        _end_session(engine, session)
    except NoResultFound:
        _end_session(engine, session)
        raise CampaignNotFoundError(id)

    return campaign

def update_campaign(id, name=None, skin=None, add_quicklink=None,\
    remove_quicklink=None):
    # Must specify at least one change
    if not (name or skin or add_quicklink or remove_quicklink):
        raise Exception('Did not specify what to update')

    (engine, session) = _start_session(DB_DIR + CAMPAIGN_DB)
   
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

    if add_quicklink:
        # Make sure the quicklink page exists
        try:
            ql_title = query_page(campaign.db_name, add_quicklink).title
        except PageNotFoundError:
            _end_session(engine, session)
            raise PageNotFoundError(add_quicklink)
        
        campaign.add_quicklink(add_quicklink, ql_title)

    if remove_quicklink:
        try:
            campaign.remove_quicklink(
                remove_quicklink[0],
                remove_quicklink[1]
            )
        except QuicklinkNotFoundError:
            _end_session(engine, session)
            raise QuicklinkNotFoundError(
                Campaign.format_quicklink(
                    remove_quicklink[0], 
                    remove_quicklink[1]
                )
            )

    # Save changes
    try:
        session.commit()
        _end_session(engine, session)
    except IntegrityError:
        _end_session(engine, session)
        raise NameUnavailableError(name)


##### Page #####
def delete_page(db_name, page_path):
    (engine, session) = _start_session(DB_DIR + db_name)

    try:
        page = session.query(Page).filter(Page.path == page_path).one()
    except NoResultFound:
        _end_session(engine, session)
        raise PageNotFoundError(page_path)

    session.delete(page)
    session.commit()
    _end_session(engine, session)
    

def insert_page(db_name, page_path, title, **kwargs):
    (engine, session) = _start_session(DB_DIR + db_name)
    
    try:
        new_page = Page.new(page_path, title, **kwargs)
        session.add(new_page)
        session.commit()
        _end_session(engine, session)
    except IntegrityError:
        _end_session(engine, session)
        raise PathUnavailableError(page_path)

def query_page(db_name, page_path):
    (engine, session) = _start_session(DB_DIR + db_name)

    try:
        page = session.query(Page).filter(Page.path == page_path).one()
        _end_session(engine, session)
    except NoResultFound:
        _end_session(engine, session)
        raise PageNotFoundError(page_path) 

    return page

def update_page(db_name, page_path, title, **kwargs):
    (engine, session) = _start_session(DB_DIR + db_name)
    
    try:
        page = session.query(Page).filter(Page.path == page_path).one()
        page.update(page_path, title, **kwargs)
        session.commit()
        _end_session(engine, session)
    except NoResultFound:
        _end_session(engine, session)
        raise PageNotFoundError(page_path)
    except IntegrityError:
        _end_session(engine, session)
        raise PathUnavailableError(page_path)
