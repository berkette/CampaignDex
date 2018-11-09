import json
import uuid
from sqlalchemy import Column, Integer, String
from db.exc import InvalidNameError, InvalidSkinError
from db.models.base import Base
from settings import CAMPAIGN_TABLE_NAME, DB_SUFFIX
from settings import PAGE_SKINS

class Campaign(Base):
    __tablename__ = CAMPAIGN_TABLE_NAME

    id = Column(Integer, primary_key=True)
    name = Column('name', String(250), unique=True, nullable=False)
    db_name = Column('db_name', String(250), unique=True, nullable=False)
    skin = Column('skin', String(250), nullable=False)

    def new(name, *, skin='default'):
        campaign = Campaign()

        if Campaign.valid_name(name):
            campaign.name = name
        else:
            raise InvalidNameError(name)

        if skin in PAGE_SKINS:
            campaign.skin = skin
        else:
            raise InvalidSkinError(skin)

        campaign.db_name = str(uuid.uuid4()) + DB_SUFFIX
        return campaign

    def update_name(self, name):
        if Campaign.valid_name(name):
            self.name = name
        else:
            raise InvalidNameError(name)

    def update_skin(self, skin='default'):
        if skin in PAGE_SKINS:
            self.skin = skin
        else:
            raise InvalidSkinError(skin)

    # Class Methods
    def valid_name(name):
        valid = True
        if not name:
            valid = False
        return valid
