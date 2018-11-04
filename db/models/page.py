from sqlalchemy import Column, Integer, String, Text
from db.models.base import Base
from settings import PAGE_TABLE_NAME

class Page(Base):
    __tablename__ = PAGE_TABLE_NAME

    id = Column(Integer, primary_key=True)
    path = Column('path', String(250), unique=True, nullable=False)
    title = Column('title', String(250))
    body = Column('body', Text)
    status = Column('status', Integer)
    template = Column('template', String(250))

    def new(path, title, *, body='', status=200, template='page.template'):
        page = Page()
        page.path = path
        page.title = title
        page.body = body
        page.status = status
        page.template = template
        return page

    def get_content(self):
        return {'title': self.title, 'body': self.body}

    def is_root(self):
        return self.path == '/'

    def update(self, path, title, **kwargs):
        self.path = path
        self.title = title
        if 'body' in kwargs:
            self.body = kwargs['body']
        if 'status' in kwargs:
            self.status = kwargs['status']
        if 'template' in kwargs:
            self.template = kwargs['template']

    def page_not_found(path):
        page = Page(
            path, 
            'Page Not Found',
            body="The page you are looking for doesn't exist. Sorry!",
            status=404
        )
        return page

