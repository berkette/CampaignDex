class CampaignNotFoundError(Exception):
    def __init__(self, id):
        message = 'No campaign was found with id {}'.format(id)
        super().__init__(message)

class DatabaseNotFoundError(Exception):
    def __init__(self, db_name):
        message = 'No database found with name {}'.format(db_name)

class InvalidNameError(Exception):
    def __init__(self, name):
        message = 'The name {} is not valid'.format(name)
        super().__init__(message)

class InvalidSkinError(Exception):
    def __init__(self, skin):
        message = '{} is not a valid skin'.format(skin)
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

class ServerResponseError(Exception):
    def __init__(self, page_path):
        message = 'Something went wrong while trying to reach {}'.format(page_path)
        super().__init__(message)

class UpdateUnspecifiedError(Exception):
    def __init__(self):
        message = 'A field to update must be specified'
        super().__init__(message)
