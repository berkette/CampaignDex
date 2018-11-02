class PageNotFoundError(Exception):
    def __init__(self, page_path):
        message = 'No page was found at path {}'.format(page_path)
        super().__init__(message)

class PathUnavailableError(Exception):
    def __init__(self, page_path):
        message = 'A page already exists at path {}'.format(page_path)
        super().__init__(message)
