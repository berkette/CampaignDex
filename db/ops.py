from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Page

def start_session(db_path):
    engine = create_engine('sqlite:///{}'.format(db_path))
    Session = sessionmaker(bind=engine)
    session = Session()
    return (engine, session)

def insert_page(db_path, page_path, title):
    # Need to make sure page_path is unique
    (engine, session) = start_session(db_path)
    
    count = session.query(Page).filter(Page.path == page_path).count()
    if count == 0:
        new_page = Page(page_path, title)
        session.add(new_page)
        session.commit()
    else:
        raise Exception("Page at this path already exists")

def query_page(db_path, page_path):
    (engine, session) = start_session(db_path)
    page = session.query(Page).filter(Page.path == page_path).one()
    return page
