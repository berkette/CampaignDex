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
        #opts = paths[path]
        #if opts['template']:
        #    return readTemplate(opts['filename'], opts['content_additions'])
        #else:
        #    return readView(opts['filename'])
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


def readView(opts):
    # Views are html files that are not being modified with content
    # additions
    status = 200
    try:
        open_file = open('views/{}'.format(filename))
        content = open_file.read()
    except Exception as err:
        content = "Error: ", err.message
        status = 500
    return {'status': status, 'content': content}



def readTemplate(filename, content_additions):
    # Templates get content additions. Maybe these should be python files
    # rather than htmls? Consider how to insert content into these.
    # f-strings, maybe? Also want to make sure an error is thrown if the
    # number of content_additions expected and provided don't match up
    status = 200
    try:
        open_file = open('templates/{}'.format(filename))
        content = open_file.read().format(content_additions)
    except Exception as err:
        content = "Error: ", err.message
        status = 500
    return {'status': status, 'content': content}
