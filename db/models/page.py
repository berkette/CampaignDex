import uuid
from sqlalchemy import Column, Boolean, Integer, String, Text
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from db.models.base import Base
from settings import NEW_TEMPLATE, PAGE_TABLE_NAME, PAGE_TEMPLATE
from settings import RTF_SUFFIX
from settings import STATUS_NOT_FOUND, STATUS_SERVER_ERR

class Page(Base):
    __tablename__ = PAGE_TABLE_NAME

    id = Column(Integer, primary_key=True)
    path = Column('path', String(250), unique=True, nullable=False)
    title = Column('title', String(250), nullable=False)
    rtf = Column('rtf', String(250), unique=True)
    quicklink = Column('quicklink', Boolean)
    status = Column('status', Integer)
    superpage_path = Column('superpage_path', String(250),\
        ForeignKey(PAGE_TABLE_NAME + '.path'))
    template = Column('template', String(250))

    superpage = relationship('Page', backref='subpages', remote_side=[path])

    def new(path, *, title='Untitled', quicklink=False, status=200,\
        superpage_path=None, template=PAGE_TEMPLATE):
        page = Page()

        page.path = path
        page.title = title
        page.quicklink = quicklink
        page.status = status
        page.superpage_path = superpage_path
        page.template = template

        if template != NEW_TEMPLATE:
            page.rtf = str(uuid.uuid4()) + RTF_SUFFIX

        return page

    def update(self, path, **kwargs):
        self.path = path
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
            status=STATUS_NOT_FOUND
        )
        return page

    def page_error(path):
        page = Page.new(
            path,
            title='Internal Server Error',
            status=STATUS_SERVER_ERR
        )
        return page

