# Server
HOST_NAME = 'localhost'
PORT_NUMBER = 9000
LOG_DIR = 'data/log/'

# Image Content Types
IMAGE_TYPES = ['image/png', 'image/jpeg', 'image/gif']

# Page paths
PATH_EXIT = '/exit'
PATH_HOME = '/wiki'
PATH_MANAGE = '/manage'
PATH_NEW = '/new'
PATH_NOT_FOUND = '/not_found'
PATH_ERROR = '/error'
PATH_ROOT = '/'

# Resource query path partials
PATH_JQUERY = '/jquery/'
PATH_QUILL = '/quill/'
PATH_RTF = '/rtf/'
PATH_IMAGES = '/images/'

# GET variable names
GETVAR_CAMPAIGN_NOT_FOUND = 'campaign_not_found'
GETVAR_INVALID_PATH = 'invalid_path'
GETVAR_INVALID_NAME = 'invalid_name'
GETVAR_INVALID_TITLE = 'invalid_title'
GETVAR_NAME_UNAVAILABLE = 'name_unavailable'
GETVAR_NO_PATH = 'no_path'
GETVAR_PAGE_NOT_FOUND = 'page_not_found'
GETVAR_PATH_UNAVAILABLE = 'path_unavailable'
GETVAR_SAVE_SUCCESS = 'save_success'

# POST paths
POST_DELETE_CAMPAIGN = '/delete_campaign'
POST_OPEN_CAMPAIGN = '/open_campaign'
POST_SAVE_CAMPAIGN = '/save_campaign'
POST_UPDATE_CAMPAIGN = '/update_campaign'

POST_APPLY_RTF = '/apply_rtf'
POST_DELETE_PAGE = '/delete_page'
POST_SAVE_PAGE = '/save_page'
POST_SAVE_RTF = '/save_rtf'
POST_UPDATE_PAGE = '/update_page'
POST_TOGGLE_QUICKLINK = '/toggle_quicklink'

# Database files, paths, and directories
CAMPAIGN_DB = 'campaigns.db'
DB_DIR = 'data/db/'
DB_PREFIX = 'sqlite:///'
DB_SUFFIX = '.db'

# Template files, paths, and directories
CAMPAIGN_HOME_TEMPLATE = 'campaign_home'
CAMPAIGN_MANAGE_TEMPLATE = 'campaign_manage'
CAMPAIGN_NEW_TEMPLATE = 'campaign_new'
EDIT_TEMPLATE = 'edit'
ERROR_TEMPLATE = 'error'
HOME_TEMPLATE = 'home'
NEW_TEMPLATE = 'new'
NOT_FOUND_TEMPLATE = 'not_found'
PAGE_TEMPLATE = 'page'
PARTIALS_TEMPLATE = 'partials'

MANAGE_TEMPLATE_PREFIX = 'manage_'

COMMON_JS = 'common'

CSS_DIR = 'css/'
CSS_SUFFIX = '.css.mako'

JS_DIR = 'js/'
JS_SUFFIX = '.js.mako'

TEMPLATE_DIR = 'assets/templates/'
TEMPLATE_SUFFIX = '.html.mako'

# Content files, paths, and directories
RTF_DIR = 'data/rtf/'
RTF_SUFFIX = '.delta'

IMAGES_DIR = 'assets/images/'

# Table names
CAMPAIGN_TABLE_NAME = 'campaigns'
PAGE_TABLE_NAME = 'pages'

# Status Codes
STATUS_OK = 200
STATUS_NOT_FOUND = 404
STATUS_REDIRECT = 303
STATUS_SERVER_ERR = 500

# Cookie Names
COOKIE_ID = 'CAMPAIGNDEX_ID'
COOKIE_DB = 'CAMPAIGNDEX_DB'
COOKIE_NAME = 'CAMPAIGNDEX_NAME'
COOKIE_SKIN = 'CAMPAIGNDEX_SKIN'

# Quill
QUILL_JS = 'quill.js'
QUILL_SNOW = 'quill.snow.css'
QUILL_DIR = 'assets/quill/'

# JQuery
JQUERY_JS = 'jquery-3.3.1.min.js'
JQUERY_DIR = 'assets/jquery/'
