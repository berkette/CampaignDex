import os
from settings import ROOT_DIR, RTF_DIR

def get_rtf_fullpath(db_name, rtf):
    rtf_sub_dir = os.path.splitext(db_name)[0] + '/'
    rtf_full_path = ROOT_DIR + RTF_DIR + rtf_sub_dir + rtf
    return rtf_full_path
