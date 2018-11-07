import json
import uuid
from sqlalchemy import Column, Integer, String, Text
from db.exc import DuplicateQuicklinkError, InvalidNameError
from db.exc import QuicklinkNotFoundError
from db.models.base import Base
from settings import CAMPAIGN_TABLE_NAME

class Campaign(Base):
    __tablename__ = CAMPAIGN_TABLE_NAME

    id = Column(Integer, primary_key=True)
    name = Column('name', String(250), unique=True, nullable=False)
    db_name = Column('db_name', String(250), unique=True, nullable=False)
    options = Column('options', Text)

    def new(name, *, skin='default', quicklinks=[]):
        # quicklinks should be a list of dicts, with values for 'path' and
        # 'title'.
        # E.g. quicklinks=[{'path': 'some/path', 'title': 'Some Title'}]

        campaign = Campaign()

        options = {
            'skin': skin,
            'quicklinks': quicklinks
        }

        if Campaign.valid_name(name):
            campaign.name = name
        else:
            raise InvalidNameError

        campaign.db_name = str(uuid.uuid4()) + '.db'
        campaign.options = json.dumps(options)
        return campaign

    def add_quicklink(self, path, title):
        opts = self.get_options()
        qls = opts['quicklinks']
        new_ql = Campaign.format_quicklink(path, title)

        if new_ql in qls:
            raise DuplicateQuicklinkError(new_ql)

        qls.append(new_ql)
        self.options = json.dumps(opts)

    def get_options(self):
        return json.loads(self.options)

    def get_skin(self):
        return self.get_options()['skin']

    def remove_quicklink(self, path, title):
        opts = self.get_options()
        ql = Campaign.format_quicklink(path, title)
        qls = opts['quicklinks']
        
        if ql in qls:
            qls.remove(ql)
        else:
            raise QuicklinkNotFoundError(ql)

        self.options = json.dumps(opts)
    
    def update_name(self, name):
        if Campaign.valid_name(name):
            self.name = name
        else:
            raise InvalidNameError

    def update_skin(self, skin='default'):
        opts = self.get_options()
        opts['skin'] = skin
        self.options = json.dumps(opts)

    # Class Methods
    def valid_name(name):
        valid = True
        if not name:
            valid = False
        return valid

    def format_quicklink(path, title):
        return {'path': path, 'title': title}

