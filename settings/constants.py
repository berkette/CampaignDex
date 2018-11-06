# Server
HOST_NAME = 'localhost'
PORT_NUMBER = 9000

# Page paths
PATH_HOME = '/'
PATH_MANAGE = '/manage'
PATH_NEW = '/new'
PATH_NOT_FOUND = '/not_found'

POST_OPEN_CAMPAIGN = '/open_campaign'
POST_SAVE_CAMPAIGN = '/save_campaign'
POST_SAVE_PAGE = '/save_page'

# Database files, paths, and directories
CAMPAIGN_DB = 'campaigns.db'
DB_DIR = 'data/db/'
DB_PREFIX = 'sqlite:///'

# Template files, paths, and directories
CAMPAIGN_BASE_TEMPLATE = 'campaign_base'
CAMPAIGN_HOME_TEMPLATE = 'campaign_home'
CAMPAIGN_NEW_TEMPLATE = 'campaign_new'
BASE_TEMPLATE = 'base'
HOME_TEMPLATE = 'home'
NEW_TEMPLATE = 'new'

CSS_DIR = 'assets/css/'
CSS_SUFFIX = '.css'

JS_DIR = 'assets/js/'
JS_SUFFIX = '.js'

TEMPLATE_DIR = 'assets/templates/'
TEMPLATE_SUFFIX = '.template'

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
SKIN_DEFAULT = 'default'
