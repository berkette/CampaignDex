import os
from sqlalchemy import create_engine
from db.models import Base, Campaign
from settings import DB_DIR, DB_PREFIX, CAMPAIGN_DB, CAMPAIGN_TABLE_NAME

root_dir = os.path.dirname(os.path.realpath(__file__))
engine_path = DB_PREFIX + root_dir + '/' + DB_DIR
engine = create_engine(engine_path + CAMPAIGN_DB)

campaign_table = Base.metadata.tables[CAMPAIGN_TABLE_NAME]
Base.metadata.create_all(engine, tables=[campaign_table])
