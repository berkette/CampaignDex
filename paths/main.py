from mako.template import Template

paths = {
    '/': {
        'filename': 'home.html',
        'content_additions': {}
    },
    '/bye': {
        'filename': 'test.mako',
        'content_additions': {'content': "Goodbye World..."}
    }
}

# Need to make this more sophisticated

def getPageData(path):
    # server.py calls this method, so don't change the name. Should
    # return a dictionary with keys 'status' (int) and 'content' (string)
    if path in paths:
        opts = paths[path]
        return buildPageData(opts['filename'], opts['content_additions'])
    else:
        return {'status': 404, 'content': '404 - Page Not Found'}


def buildPageData(filename, content_additions={}):
    status = 200
    filepath = 'views/' + filename
    try:
        template = Template(filename=filepath)
        content = template.render(attributes=content_additions)
    except FileNotFoundError:
        status = 500
        content = 'FileNotFoundError: Could not locate the template {}'.format(filepath)
    return {'status': status, 'content': content}

