class CampaignNotFoundError(Exception):
    def __init__(self, id):
        message = 'No campaign was found with id {}'.format(id)
        super().__init__(message)

class DuplicateQuicklinkError(Exception):
    def __init__(self, quicklink):
        message = '{} is already a quicklink'.format(quicklink)
        super().__init__(message)
        self.errors = {'quicklink': quicklink}

class InvalidNameError(Exception):
    def __init__(self, name):
        message = 'The name {} is not valid'.format(name)
        super().__init__(message)

class NameUnavailableError(Exception):
    def __init__(self, name):
        message = 'A campaign already exists with name {}'.format(name)
        super().__init__(message)

class PageNotFoundError(Exception):
    def __init__(self, page_path):
        message = 'No page was found at path {}'.format(page_path)
        super().__init__(message)

class PathUnavailableError(Exception):
    def __init__(self, page_path):
        message = 'A page already exists at path {}'.format(page_path)
        super().__init__(message)

class QuicklinkNotFoundError(Exception):
    def __init__(self, ql):
        message = 'The quicklink {} does not exist'.format(ql)
        super().__init__(message)

class UpdateUnspecifiedError(Exception):
    def __init__(self):
        message = 'A field to update must be specified'
        super().__init__(message)
