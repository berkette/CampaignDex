from sqlalchemy import Column, Integer, String, Text
from db.models.base import Base

class Page(Base):
    __tablename__ = 'pages'

    id = Column(Integer, primary_key=True)
    path = Column('path', String(250), nullable=False)
    title = Column('title', String(250), nullable=False)
    body = Column('body', Text)

    def __init__(self, path, title):
        self.path = path
        self.title = title

    def get_content(self):
        return {'title': self.title, 'body': self.body}

    def is_root(self):
        return self.path == '/'

