plugins = []

def check_plugin(plugin_name, the_plugin):
    # Route prefix
    if hasattr(the_plugin, "route_prefix"):
        # raise AttributeError("{} has no route_prefix attribute".format(plugin_name))
        
        if type(the_plugin.route_prefix) != str:
            raise AttributeError("{}.route_prefix is not a string, it is a {}".format(plugin_name, type(the_plugin.route_prefix)))
    
    # Version
    if hasattr(the_plugin, "schema"):
        if not hasattr(the_plugin.schema, "schema"):
            raise AttributeError("{} has no schema.version attribute".format(plugin_name))
        
        if type(the_plugin.schema.version) not in (float, int):
            raise AttributeError("{}.schema.version is not a number, it is a {}".format(plugin_name, type(the_plugin.schema.version)))
        
        # Schema
        if not hasattr(the_plugin, "schema"):
            raise AttributeError("{} has no schema attribute".format(plugin_name))
