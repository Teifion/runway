from ...system.lib import (
    install_f,
    site_settings_f,
    schema_f,
)
import os
import transaction

_folder_path = os.path.realpath(__file__).replace('/core/plugins/lib/plugins_f.py', '')

plugins = []

def check_plugin(plugin_name, the_plugin):
    # Route prefix
    if hasattr(the_plugin, "route_prefix"):
        # raise AttributeError("{} has no route_prefix attribute".format(plugin_name))
        
        if type(the_plugin.route_prefix) != str:
            raise AttributeError("{}.route_prefix is not a string, it is a {}".format(plugin_name, type(the_plugin.route_prefix)))
    
    # Schema
    if hasattr(the_plugin, "schema"):
        if not hasattr(the_plugin.schema, "schema"):
            raise AttributeError("{} has no schema.version attribute".format(plugin_name))
        
        if type(the_plugin.schema.version) not in (float, int):
            raise AttributeError("{}.schema.version is not a number, it is a {}".format(plugin_name, type(the_plugin.schema.version)))
        
        if not hasattr(the_plugin, "schema"):
            raise AttributeError("{} has no schema attribute".format(plugin_name))

def install_module(the_plugin):
    """
    Called when we have nothing for a module and need to install it from scratch
    """
    # with transaction.manager:
    #     site_settings_f.install_settings(install_f.get_module_settings(the_plugin))
    
    # Check for a schema
    if hasattr(the_plugin, "schema"):
        # We know this is a fresh install so we don't need to check the
        # schema versioning
        with transaction.manager:
            schema_f.add_schema(the_plugin.route_prefix, the_plugin.schema.version)
    
    # If it's got a specific install function we'll call that
    if hasattr(the_plugin, "install"):
        the_plugin.install()
    
    # Now call update as that copies over things like static assets
    update_module(the_plugin)


def update_module(the_plugin):
    """
    Called when we have a module already installed but just need to check to see
    if we need to update it (any new settings, schema etc)
    """
    
    module_default_settings = install_f.get_module_settings(the_plugin)
    module_settings = site_settings_f.get_settings(*module_default_settings.keys())
    
    new_settings = {}
    for name, default in module_default_settings.items():
        if name not in module_settings:
            new_settings[name] = default
    
    if len(new_settings) > 0:
        with transaction.manager:
            site_settings_f.install_settings(new_settings)
    
    if hasattr(the_plugin, "schema"):
        current_version = schema_f.get_version(the_plugin.route_prefix)
        
        if the_plugin.schema.version > current_version:
            with transaction.manager:
                schema_f.update_schema(the_plugin.schema.schema, current_version)
                schema_f.add_schema(the_plugin.route_prefix, the_plugin.schema.version)
    
    # If there's a static folder, copy that over
    plugin_static = "{fp}/plugins/{plugin}/static/".format(fp=_folder_path, plugin=the_plugin.route_prefix)
    if os.path.isdir(plugin_static):
        cmd = "cp -R {plugin_static} {fp}/static/{plugin}".format(fp=_folder_path, plugin=the_plugin.route_prefix, plugin_static=plugin_static)
        os.system(cmd)
    
    # If it's got a specific update function we'll call that
    if hasattr(the_plugin, "update"):
        the_plugin.update()
    
    
