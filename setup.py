import os
from sqlalchemy import create_engine
from db.models import Base, Campaign
from settings import DB_PREFIX, CAMPAIGN_DB, CAMPAIGN_TABLE_NAME
from settings import DB_DIR, LOG_DIR, ROOT_DIR, RTF_DIR

def create_campaign_db():
    db_dir = ROOT_DIR + DB_DIR
    log_dir = ROOT_DIR + LOG_DIR
    rtf_dir = ROOT_DIR + RTF_DIR
    
    if not os.path.isdir(db_dir):
        os.makedirs(db_dir)

    if not os.path.isdir(log_dir):
        os.makedirs(log_dir)

    if not os.path.isdir(rtf_dir):
        os.makedirs(rtf_dir)

    if not os.path.isfile(db_dir + CAMPAIGN_DB):
        db_path = DB_PREFIX + db_dir + CAMPAIGN_DB
        engine = create_engine(db_path)

        campaign_table = Base.metadata.tables[CAMPAIGN_TABLE_NAME]
        Base.metadata.create_all(engine, tables=[campaign_table])

if __name__ == '__main__':
    create_campaign_db()
