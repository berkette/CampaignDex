import os
from settings import DB_DIR, ROOT_DIR, RTF_DIR

def get_rtf_fullpath(db_name, rtf):
    rtf_sub_dir = os.path.splitext(db_name)[0] + '/'
    rtf_full_path = ROOT_DIR + RTF_DIR + rtf_sub_dir + rtf
    return rtf_full_path

def db_exists(db_name):
    return os.path.isfile(ROOT_DIR + DB_DIR + db_name)
