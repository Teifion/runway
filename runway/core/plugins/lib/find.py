from ...base import DBSession
import os
import re

folder_name = re.compile(r'^[a-zA-Z0-9][a-zA-Z0-9_]+$')

def scan_for_plugins(folder_path):
    """
    Scans the plugins folder for valid plugins and returns a dictionary of the names
    and information about each plugin.
    """
    
    listdir = os.listdir(folder_path + '/plugins')
    
    for f in listdir:
        if folder_name.search(f):
            yield f
