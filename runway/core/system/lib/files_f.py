import os
from os.path import isfile, join, dirname, realpath

def iter_tree(folder_path, filter_f=None):
    """
    Recursively go through all the folders/files in a folder
    """
    file_list = os.listdir(folder_path)
    
    for f in file_list:
        if not isfile(join(folder_path, f)):
            yield from iter_tree(join(folder_path, f), filter_f)
            continue
        
        if filter_f is None or filter_f(f):
            yield folder_path, f
