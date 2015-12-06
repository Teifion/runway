from ...base import DBSession
# from ..models.plugins import Plugin
import os
import re

folder_name = re.compile(r'^[a-zA-Z0-9][a-zA-Z0-9_]+$')

def scan_for_plugins(folder_path):
    """
    Scans the plugins folder for valid plugins and returns a dictionary of the names
    and information about each plugin.
    """
    
    # folder_path = '/Users/teifion/programming/python/venustate/venustate/'
    listdir = os.listdir(folder_path + '/plugins')
    
    for f in listdir:
        if folder_name.search(f):
            yield f

# def enabled_plugins():
#     return (p[0] for p in DBSession.query(Plugin.name).filter(Plugin.enabled == True))

# def update_plugin_list():
#     found_plugins = tuple(scan_for_plugins())
    
#     superfluous = set()
#     missing = set(found_plugins)
    
#     # query = (p[0] for p in DBSession.query(Plugin.name))
    
#     for (plugin_name,) in DBSession.query(Plugin.name):
#         if plugin_name in found_plugins:
#             missing.remove(plugin_name)
#         else:
#             superfluous.add(plugin_name)
    
#     # Remove superfluous
#     DBSession.query(Plugin).filter(Plugin.name.in_(superfluous)).delete(synchronize_session='fetch')
    
#     # Add missing
#     for plugin_name in missing:
#         DBSession.add(Plugin(
#             name      = plugin_name,
#             enabled   = False,
#             installed = False,
#         ))
    
