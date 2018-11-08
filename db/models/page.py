from sqlalchemy import Column, Boolean, Integer, String, Text
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from db.models.base import Base
from settings import PAGE_TABLE_NAME

class Page(Base):
    __tablename__ = PAGE_TABLE_NAME

    id = Column(Integer, primary_key=True)
    path = Column('path', String(250), unique=True, nullable=False)
    title = Column('title', String(250))
    body = Column('body', Text)
    quicklink = Column('quicklink', Boolean)
    status = Column('status', Integer)
    superpage_path = Column('superpage_path', String(250),\
        ForeignKey(PAGE_TABLE_NAME + '.path'))
    template = Column('template', String(250))

    superpage = relationship('Page', backref='subpages', remote_side=[path])

    def new(path, *, title='Untitled', body='', quicklink=False, status=200,\
        superpage_path=None, template='page'):
        page = Page()
        page.path = path
        page.title = title
        page.body = body
        page.quicklink = quicklink
        page.status = status
        page.superpage_path = superpage_path
        page.template = template
        return page

    def update(self, path, **kwargs):
        self.path = path
        if 'body' in kwargs:
            self.body = kwargs['body']
        if 'quicklink' in kwargs:
            self.quicklink = kwargs['quicklink']
        if 'status' in kwargs:
            self.status = kwargs['status']
        if 'superpage_path' in kwargs:
            self.superpage_path = kwargs['superpage_path']
        if 'template' in kwargs:
            self.template = kwargs['template']
        if 'title' in kwargs:
            self.title = kwargs['title']

    ### Class Methods ###

    def page_not_found(path):
        page = Page.new(
            path, 
            title='Page Not Found',
            body="The page you are looking for doesn't exist. Sorry!",
            status=404
        )
        return page

