from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

import transaction
import os
import re
from datetime import datetime
import warnings

from .system.lib import site_settings_f, user_settings_f, tweens
from sqlalchemy.engine.reflection import Inspector
from .cli.lib import cli_f

_folder_path = os.path.realpath(__file__).replace('/core/main.py', '')

def routes(config, routing_name=""):
    from . import (
        admin,
        cli,
        cron,
        system,
        dev,
        plugins,
        apis,
        testing,
        widgets,
        documentation,
        triggers,
        themes,
        hooks,
        commands,
    )
    
    config.include(system, route_prefix=routing_name+"")
    config.include(admin, route_prefix=routing_name+"admin")
    config.include(dev, route_prefix=routing_name+"dev")
    config.include(cli, route_prefix=routing_name+"cli")
    config.include(cron, route_prefix=routing_name+"cron")
    config.include(plugins, route_prefix=routing_name+"plugins")
    config.include(apis, route_prefix=routing_name+"api")
    config.include(testing, route_prefix=routing_name+"testing")
    config.include(widgets, route_prefix=routing_name+"widgets")
    config.include(documentation, route_prefix=routing_name+"documentation")
    config.include(triggers, route_prefix=routing_name+"triggers")
    config.include(themes, route_prefix=routing_name+"themes")
    config.include(hooks, route_prefix=routing_name+"hooks")
    config.include(commands, route_prefix=routing_name+"commands")
    
    from .system.lib import site_settings_f
    site_settings_f.include_plugin(system.site_settings)
    site_settings_f.include_plugin(themes.site_settings)
    
    user_settings_f.include_plugin(system.user_settings)
    
    return config

def plugin_routes(config, route_settings, routing_name=""):
    from .. import plugins
    from .plugins.lib import find, plugins_f
    from .system.lib import site_settings_f, user_settings_f
    
    for plugin_name in find.scan_for_plugins(_folder_path):
        if route_settings.get("runway.modules.{}".format(plugin_name), None) != "True":
            continue
        
        exec("from ..plugins import %s" % plugin_name, plugins.__dict__)
        the_plugin = plugins.__dict__[plugin_name]
        
        plugins_f.plugins.append(the_plugin)
        
        if hasattr(the_plugin, "route_prefix"):
            config.include(the_plugin, route_prefix=routing_name+the_plugin.route_prefix)
        
        if hasattr(the_plugin, "user_settings"):
            user_settings_f.include_plugin(the_plugin.user_settings)
        
        if hasattr(the_plugin, "site_settings"):
            site_settings_f.include_plugin(the_plugin.site_settings)
        
        if hasattr(the_plugin, "site_menu"):
            site_settings_f._hidden_settings['site_menu'][the_plugin.site_menu['id']] = the_plugin.site_menu
    
    return config

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    from .base import DBSession
    
    _re_folder_name = re.search(r'/([a-zA-Z0-9_]+)/core$', os.path.dirname(os.path.realpath(__file__)))
    _folder_name = _re_folder_name.groups()[0] + "/"
    
    if settings.get('ignore_folder', False):
        routing_name = ""
    else:
        routing_name = _folder_name
    
    _settings_table_found = True
    
    # If we're testing then sometimes we might try to create multiple sessions
    if "testing_mode" not in settings:
        engine = engine_from_config(settings, 'sqlalchemy.')
        # DBSession.configure(bind=engine, autocommit=True)
        DBSession.configure(bind=engine)
        
        # Take this out if the debug toolbar is activated
        warnings.simplefilter('error')
        
        # warnings.simplefilter('error', SAWarning)
        
        inspector = Inspector.from_engine(engine)
        _settings_table_found = "runway_settings" in inspector.get_table_names()
    
    if not _settings_table_found:
        print("\n\n")
        print(cli_f.shell_text("[r]WARNING: No runway_settings table found[/r]"))
        print("\n\n")
    
    # The config
    config = Configurator(settings=settings, root_factory='.system.lib.auth.RootFactory')
    
    # We use this here as well because it doesn't work in testing otherwise
    config.include('pyramid_chameleon')
    
    # Logging tween
    
    config.add_tween('.system.lib.tweens.menu_tween_factory')
    config.add_tween('.system.lib.tweens.settings_tween_factory')
    config.add_tween('.system.lib.tweens.render_tween_factory')
    config.add_tween('.system.lib.tweens.logging_tween_factory')
    config.add_static_view('static', '../static', cache_max_age=3600)
    
    # Routes
    routes(config, routing_name=routing_name)
    # routes(config, name='venu/')
    
    # Plugins
    if _settings_table_found:
        route_settings = site_settings_f.get_settings_like("runway.modules%")
        plugin_routes(config, route_settings, routing_name=routing_name)
    
    # Imports for other stuff
    from .system.lib import auth
    auth.init()
    
    from .system.models.user import groupfinder
    
    # User auth
    authn_policy = AuthTktAuthenticationPolicy('K*WJGU&j8AA ZT?=J1T-TUfH9*lY#!>@' + _folder_name, callback=groupfinder, hashalg='sha512')
    authz_policy = ACLAuthorizationPolicy()
    # authz_policy = RunwayACLAuthorizationPolicy()
    
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)
    
    # Set settings
    if site_settings_f._settings_collection is None and _settings_table_found:
        site_settings_f._settings_collection = site_settings_f.build_runway_settings_collection()
        site_settings_f._server_ini = global_config['__file__']
    
    r = config.make_wsgi_app()
    
    # Call startup hook
    from .hooks import call_hook
    call_hook("startup")
    
    if _settings_table_found:
        with transaction.manager:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            site_settings_f.set_setting("runway.system.last_startup", now)
            site_settings_f.set_setting("runway.system.last_change", now)
    
    return r

def install():
    from . import system
    from .. import plugins
    from .plugins.lib import find, plugins_f
    from .themes.lib import themes_f
    from .system.lib import install_f
    from .system.lib import schema_f
    from .system.models import schema as runway_schema
    
    install_f.create_tables()
    system.install()
    
    route_settings = site_settings_f.get_settings_like("runway.modules%")
    setting_dict = {}
    schema_versions = schema_f.get_versions()
    
    # Plugins
    for plugin_name in find.scan_for_plugins(_folder_path):
        if route_settings.get(plugin_name, 'False') != 'True':
            continue
        
        exec("from ..plugins import %s" % plugin_name, plugins.__dict__)
        the_plugin = plugins.__dict__[plugin_name]
        
        plugins_f.check_plugin(plugin_name, the_plugin)
        
        if "runway.modules.{}".format(plugin_name) not in route_settings:
            setting_dict["runway.modules.{}".format(plugin_name)] = "False"
        
        setting_dict.update(install_f.get_module_settings(the_plugin))
        
        # If it's got a specific install function we'll call that
        if hasattr(the_plugin, "install"):
            the_plugin.install()
        
        # If there's a static folder, copy that over
        plugin_static = "{fp}/plugins/{plugin}/static/".format(fp=_folder_path, plugin=plugin_name)
        if os.path.isdir(plugin_static):
            cmd = "cp -R {plugin_static} {fp}/static/{plugin}".format(fp=_folder_path, plugin=plugin_name, plugin_static=plugin_static)
            
            os.system(cmd)
        
        # Check for a schema
        if hasattr(the_plugin, "schema"):
            # Now check to see if the schema is the latest version
            if plugin_name not in schema_versions:
                # If we can't find the version then we've not installed this plugin before
                # and this is a fresh install
                with transaction.manager:
                    schema_f.add_schema(plugin_name, the_plugin.schema.version)
            else:
                with transaction.manager:
                    if the_plugin.schema.version > schema_versions[plugin_name].version:
                        schema_f.update_schema(the_plugin.schema.schema, schema_versions[plugin_name].version)
                        schema_f.add_schema(plugin_name, the_plugin.schema.version)
    
    # Now do the schema thing with the main module too
    runway_name = "runway"
    if runway_name not in schema_versions:
        with transaction.manager:
            schema_f.add_schema(runway_name, runway_schema.version)
    else:
        with transaction.manager:
            if runway_schema.version > schema_versions[runway_name].version:
                schema_f.update_schema(runway_schema.schema, schema_versions[runway_name].version)
                schema_f.add_schema(runway_name, runway_schema.version)
    
    # Install settings as needed
    if len(setting_dict) > 0:
        with transaction.manager:
            site_settings_f.install_settings(setting_dict)
    
    # Now install any theme media we need for themes
    for theme_name in themes_f.scan_themes_folder():
        
        # If there's a static folder, copy that over
        theme_static = "{fp}/{theme}/static/".format(fp=themes_f._folder_path, theme=theme_name)
        if os.path.isdir(theme_static):
            cmd = "cp -R {theme_static} {fp}/static/themes/{theme}".format(fp=_folder_path, theme=theme_name, theme_static=theme_static)
            os.system(cmd)
