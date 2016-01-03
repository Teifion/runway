def dev_views(config):
    from .views import dev
    
    config.add_route('triggers.dev.home', 'dev/home')
    config.add_view(dev.home, route_name='triggers.dev.home', renderer='templates/dev/home.pt', permission='developer')
    
    config.add_route('triggers.dev.triggers.view', 'dev/triggers/view/{trigger_name}')
    config.add_route('triggers.dev.triggers.run', 'dev/triggers/run/{trigger_name}')
    config.add_view(dev.view_trigger, route_name='triggers.dev.triggers.view', renderer='templates/dev/view_trigger.pt', permission='developer')
    config.add_view(dev.run_trigger, route_name='triggers.dev.triggers.run', renderer='templates/dev/run_trigger.pt', permission='developer')
    
    config.add_route('triggers.dev.actions.view', 'dev/actions/view/{action_name}')
    config.add_route('triggers.dev.actions.run', 'dev/actions/run/{action_name}')
    config.add_view(dev.view_action, route_name='triggers.dev.actions.view', renderer='templates/dev/view_action.pt', permission='developer')
    config.add_view(dev.run_action, route_name='triggers.dev.actions.run', renderer='templates/dev/run_action.pt', permission='developer')

def user_views(config):
    from .views import general
    
    config.add_route('triggers.user.control_panel', 'user/control_panel')
    config.add_route('triggers.user.create', 'user/create')
    config.add_route('triggers.user.edit', 'user/edit/{trigger_script_id}')
    config.add_route('triggers.user.gui_edit', 'user/gui_edit/{trigger_script_id}')
    config.add_route('triggers.user.delete', 'user/delete/{trigger_script_id}')
    config.add_route('triggers.user.test_trigger_script', 'user/test_trigger_script/{trigger_script_id}')
    
    # config.add_route('triggers.user.run', 'user/run/{trigger_script_id}')
    # config.add_route('triggers.user.run_now', 'user/run_now/{trigger_script_id}')
    # # config.add_route('triggers.user.check', 'user/check/{trigger_script_id}')
    # config.add_route('triggers.user.pause', 'user/pause/{trigger_script_id}')
    # config.add_route('triggers.user.resume', 'user/resume/{trigger_script_id}')
    # config.add_route('triggers.user.unlock', 'user/unlock/{trigger_script_id}')
    
    # config.add_route('triggers.human_time', 'human_time')
    # config.add_route('triggers.human_time_test', 'human_time_test')
    
    config.add_view(general.control_panel, route_name='triggers.user.control_panel', renderer='templates/user/control_panel.pt', permission='loggedin')
    config.add_view(general.create, route_name='triggers.user.create', renderer='templates/user/create.pt', permission='loggedin')
    config.add_view(general.edit, route_name='triggers.user.edit', renderer='templates/user/edit.pt', permission='loggedin')
    config.add_view(general.gui_edit, route_name='triggers.user.gui_edit', renderer='templates/user/gui_edit.pt', permission='loggedin')
    config.add_view(general.delete, route_name='triggers.user.delete', renderer='templates/user/delete.pt', permission='loggedin')
    config.add_view(general.test_trigger_script, route_name='triggers.user.test_trigger_script', renderer='templates/user/test_trigger_script.pt', permission='loggedin')
    
    # config.add_view(general.run, route_name='triggers.user.run', renderer='templates/user/run.pt', permission='loggedin')
    # config.add_view(general.run_now, route_name='triggers.user.run_now', renderer='templates/user/run_now.pt', permission='loggedin')
    # # config.add_view(general.check, route_name='triggers.user.check', renderer='string', permission='loggedin')
    # config.add_view(general.pause, route_name='triggers.user.pause', permission='loggedin')
    # config.add_view(general.resume, route_name='triggers.user.resume', permission='loggedin')
    # config.add_view(general.unlock, route_name='triggers.user.unlock', permission='loggedin')
    
    # config.add_view(general.human_time_view, route_name='triggers.human_time', renderer='templates/user/human_time.pt', permission='loggedin')
    # config.add_view(general.human_time_test, route_name='triggers.human_time_test', renderer='string')

def log_views(config):
    from .views import logs
    
    config.add_route('triggers.logs.view', 'logs/view/{log_id}')
    config.add_route('triggers.logs.view_for_job', 'logs/view_for_job/{trigger_script_id}')
    config.add_route('triggers.logs.view_for_user', 'logs/view_for_user/{user_id}')
    config.add_route('triggers.logs.view_for_time', 'logs/view_for_time')
    
    config.add_view(logs.view, route_name='triggers.logs.view', renderer='templates/logs/view.pt', permission='loggedin')
    config.add_view(logs.view_for_job, route_name='triggers.logs.view_for_job', renderer='templates/logs/list.pt', permission='loggedin')
    config.add_view(logs.view_for_user, route_name='triggers.logs.view_for_user', renderer='templates/logs/list.pt', permission='loggedin')
    config.add_view(logs.view_for_time, route_name='triggers.logs.view_for_time', renderer='templates/logs/list.pt', permission='triggers.admin')

def admin_views(config):
    from .views import admin
    
    config.add_route('triggers.admin.home', 'admin/home')
    # config.add_route('triggers.admin.job_types', 'admin/job_types')
    
    # config.add_view(admin.home, route_name='triggers.admin.home', renderer='templates/admin/home.pt', permission='triggers.admin')
    # config.add_view(admin.job_types, route_name='triggers.admin.job_types', renderer='templates/admin/job_types.pt', permission='triggers.admin')

def documentation_views(config):
    from . import documentation
    from ...core.documentation import basic_view
    
    config.add_route('triggers.documentation.add', 'documentation/add')
    
    config.add_view(
        basic_view(documentation.Add),
        route_name='triggers.documentation.add',
        renderer="templates/documentation/add.pt",
        permission="developer"
    )

def init_auth():
    from ..system.lib import auth
    
    auth.add("triggers", 'User', set())
    ag = auth.add("triggers", 'Admin', {'admin'})
    auth.add("triggers", 'Super user', ag | {'su'}, rank=4)

def includeme(config):
    dev_views(config)
    user_views(config)
    admin_views(config)
    documentation_views(config)
    # log_views(config)
    
    init_auth()
    
    # 
    from .triggers import (
        dummy_trigger,
    )
    
    from .actions import (
        dummy_action,
    )
    
    from .lib import actions_f, triggers_f
    from ..hooks import append_to_hook
    
    append_to_hook("startup", actions_f.collect_actions)
    append_to_hook("startup", triggers_f.collect_triggers)
    append_to_hook("pre_render", triggers_f.triggers_pre_render)
    
from .documentation import *

# Allows much easier calling to commonly referenced things
from .lib.triggers_f import call_trigger
from .models import Action, Trigger
