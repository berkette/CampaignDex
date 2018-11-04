from mako.template import Template
from db import query_page
from db.exc import PageNotFoundError
from db.models import Campaign, Page
from settings import CAMPAIGN_DB, DB_DIR

# Need to make this more sophisticated

def get_response_data(path, db_name=None):
    # server.py calls this method, so don't change the name. Should
    # return a dictionary with keys 'status' (int) and 'content' (string)

    if db_name:
        # Means the user is looking at a specific campaign
        try:
            page = query_page(db_name, path)
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
    else:
        # Means the user is looking at campaign selection/creation
        if path == '/':
            pass
        elif path == '/start_campaign':
            pass
        else:
            page = Page.page_not_found(path)
            # TODO?
