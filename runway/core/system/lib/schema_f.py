from ...base import DBSession
from ..models.system import Schema
from ...plugins.lib import find
from functools import reduce
import transaction

"""
Schemas are a dictionary of:

(min, max, target): [queries]

min is the minimum version this change targets
max is the maximum version this change targets (can be the same as min)
target is the version of the schema you will be on after performing this change

queries is the sequence of queries which perform the change

"""

def get_versions():
    return {row.module:row for row in DBSession.query(Schema)}
    
    
    # for plugin_name in find.scan_for_plugins(_folder_path):
    #     exec("from ..plugins import %s" % plugin_name, plugins.__dict__)
    #     the_plugin = plugins.__dict__[plugin_name]
        
    #     if "runway.modules.{}".format(plugin_name) not in route_settings:
    #         setting_dict["runway.modules.{}".format(plugin_name)] = "False"
        
    #     setting_dict.update(install_f.get_module_settings(the_plugin))
        
    #     # If it's got a specific install function we'll call that
    #     if hasattr(the_plugin, "install"):
    #         the_plugin.install()
        
    #     # If there's a static folder, copy that over
    #     plugin_static = "{fp}/plugins/{plugin}/static/".format(fp=_folder_path, plugin=plugin_name)
    #     if os.path.isdir(plugin_static):
    #         cmd = "cp -R {plugin_static} {fp}/static/{plugin}".format(fp=_folder_path, plugin=plugin_name, plugin_static=plugin_static)
            
    #         os.system(cmd)

def add_schema(module, version):
    the_schema = DBSession.query(Schema).filter(Schema.module == module).first()
    
    if the_schema != None:
        DBSession.query(Schema).filter(Schema.module == module).delete()
    
    the_schema = Schema(module=module, version=version)
    DBSession.add(the_schema)

def update_schema(schema, current_version):
    path = find_path(schema, current_version)
    
    # Flatten the queries down
    nested_queries = [schema[p] for p in path]
    queries = [item for sublist in nested_queries for item in sublist]
    
    with transaction.manager:
        for q in queries:
            
            # It could be a query, it could be a function
            if isinstance(q, str):
                DBSession.execute(q)
            else:
                q()
        
        if len(queries) > 0:
            DBSession.execute("COMMIT")

def find_path(schema, current_version):
    valid_option = lambda k: k[0] <= current_version and k[1] >= current_version
    max_key = lambda k1, k2: k1 if k1[2] > k2[2] else k2
    
    # First find all valid options
    chosen = reduce(max_key, filter(valid_option, schema.keys()))
    max_option = reduce(max_key, schema.keys())
    
    if chosen[2] == max_option[2]:
        return [chosen]
    
    return [chosen] + find_path(schema, chosen[2])
