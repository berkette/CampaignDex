from cgi import FieldStorage
from db import insert_page
from db.exc import PathUnavailableError
from settings import DB_DIR

def save_page(form):
    path = form['page_path'].value
    title = form['page_title'].value
    if 'page_body' in form:
        body = form['page_body'].value
    else:
        body = ''

    try:
        insert_page(DB_DIR + '/test.db', path, title, body=body)
    except PathUnavailableError:
        print("Can't save the page")
