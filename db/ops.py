from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from db.exc import PageNotFoundError, PathUnavailableError
from db.models import Page

### Private Methods

def _start_session(db_path):
    engine = create_engine('sqlite:///{}'.format(db_path))
    Session = sessionmaker(bind=engine)
    session = Session()
    return (engine, session)

def _end_session(engine, session):
    session.close()
    engine.dispose()


### Public Methods

def insert_page(db_path, page_path, title, **kwargs):
    (engine, session) = _start_session(db_path)
    
    try:
        new_page = Page(page_path, title, **kwargs)
        session.add(new_page)
        session.commit()
        _end_session(engine, session)
    except IntegrityError:
        _end_session(engine, session)
        raise PathUnavailableError(page_path)

def query_page(db_path, page_path):
    (engine, session) = _start_session(db_path)

    try:
        page = session.query(Page).filter(Page.path == page_path).one()
        _end_session(engine, session)
    except NoResultFound:
        _end_session(engine, session)
        raise PageNotFoundError(page_path) 

    return page

def update_page(db_path, page_path, title, **kwargs):
    (engine, session) = _start_session(db_path)
    
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
