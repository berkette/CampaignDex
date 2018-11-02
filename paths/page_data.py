from mako.template import Template
from db import query_page
from db.exc import PageNotFoundError
from db.models import Page
from settings import DB_DIR

# Need to make this more sophisticated

def get_page_data(path):
    # server.py calls this method, so don't change the name. Should
    # return a dictionary with keys 'status' (int) and 'content' (string)

    try:
        page = query_page(DB_DIR + 'test.db', path)
    except PageNotFoundError:
        page = Page.page_not_found(path)

    template_path = 'views/' + page.template
    try:
        template = Template(filename=template_path)
        content = template.render(attributes=page.get_content())
    except FileNotFoundError:
        status = 500
        content = 'FileNotFoundError: Could not locate the template {}'.format(template_path)

    return {'status': page.status, 'content': content}
