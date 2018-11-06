import os
from sqlalchemy import create_engine
from db.models import Base, Campaign
from settings import DB_DIR, DB_PREFIX, CAMPAIGN_DB, CAMPAIGN_TABLE_NAME
from settings import ROOT_DIR

def create_campaign_db():
    db_path = DB_PREFIX + ROOT_DIR + DB_DIR + CAMPAIGN_DB
    engine = create_engine(db_path)

    campaign_table = Base.metadata.tables[CAMPAIGN_TABLE_NAME]
    Base.metadata.create_all(engine, tables=[campaign_table])

if __name__ == '__main__':
    create_campaign_db()
