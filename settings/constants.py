# Server
HOST_NAME = 'localhost'
PORT_NUMBER = 9000

# Page paths
PATH_HOME = '/'
PATH_MANAGE = '/manage'
PATH_NEW = '/new'
PATH_NOT_FOUND = '/not_found'

GETVAR_CAMPAIGN_NOT_FOUND = 'campaign_not_found'
GETVAR_INVALID_NAME = 'invalid_name'
GETVAR_NAME_UNAVAILABLE = 'name_unavailable'
GETVAR_PATH_UNAVAILABLE = 'path_unavailable'
GETVAR_SAVE_SUCCESS = 'save_success'

POST_OPEN_CAMPAIGN = '/open_campaign'
POST_SAVE_CAMPAIGN = '/save_campaign'
POST_UPDATE_CAMPAIGN = '/update_campaign'
POST_SAVE_PAGE = '/save_page'

# Database files, paths, and directories
CAMPAIGN_DB = 'campaigns.db'
DB_DIR = 'data/db/'
DB_PREFIX = 'sqlite:///'

# Template files, paths, and directories
CAMPAIGN_BASE_TEMPLATE = 'campaign_base'
CAMPAIGN_HOME_TEMPLATE = 'campaign_home'
CAMPAIGN_MANAGE_TEMPLATE = 'campaign_manage'
CAMPAIGN_NEW_TEMPLATE = 'campaign_new'
BASE_TEMPLATE = 'base'
HOME_TEMPLATE = 'home'
NEW_TEMPLATE = 'new'

CSS_DIR = 'css/'
CSS_SUFFIX = '.css.mako'

JS_DIR = 'js/'
JS_SUFFIX = '.js.mako'

TEMPLATE_DIR = 'assets/templates/'
TEMPLATE_SUFFIX = '.html.mako'

# Table names
CAMPAIGN_TABLE_NAME = 'campaigns'
PAGE_TABLE_NAME = 'pages'

# Status Codes
STATUS_OK = 200
STATUS_NOT_FOUND = 404
STATUS_REDIRECT = 303
STATUS_SERVER_ERR = 500

# Cookies
COOKIE_ID = 'CAMPAIGNDEX_ID'
COOKIE_DB = 'CAMPAIGNDEX_DB'
COOKIE_SKIN = 'CAMPAIGNDEX_SKIN'

# Skins
SKIN_CAMPAIGN = 'campaign'
SKIN_DEFAULT = 'default'

PAGE_SKINS = [SKIN_DEFAULT]
