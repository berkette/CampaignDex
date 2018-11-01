import os
from sqlalchemy import create_engine
from db.models import *
from settings import DB_DIR

root_dir = os.path.dirname(os.path.realpath(__file__))
engine_path = 'sqlite:///' + root_dir + '/data/db/'
engine = create_engine(engine_path + 'test.db')
Base.metadata.create_all(engine)
