# def dev_views(config):
#     from .views import dev
    
#     config.add_route('cron.dev.home', 'dev/home')
#     config.add_view(dev.home, route_name='cron.dev.home', renderer='templates/dev/home.pt', permission='cron.dev')

def user_views(config):
    from .views import general
    
    config.add_route('cron.user.control_panel', 'user/control_panel')
    config.add_route('cron.user.create', 'user/create')
    config.add_route('cron.user.edit', 'user/edit/{job_id}')
    config.add_route('cron.user.delete', 'user/delete/{job_id}')
    
    config.add_route('cron.user.run', 'user/run/{job_id}')
    config.add_route('cron.user.run_now', 'user/run_now/{job_id}')
    # config.add_route('cron.user.check', 'user/check/{job_id}')
    config.add_route('cron.user.pause', 'user/pause/{job_id}')
    config.add_route('cron.user.resume', 'user/resume/{job_id}')
    config.add_route('cron.user.unlock', 'user/unlock/{job_id}')
    
    config.add_route('cron.human_time', 'human_time')
    config.add_route('cron.human_time_test', 'human_time_test')
    
    config.add_view(general.control_panel, route_name='cron.user.control_panel', renderer='templates/user/control_panel.pt', permission='loggedin')
    config.add_view(general.create, route_name='cron.user.create', renderer='templates/user/create.pt', permission='loggedin')
    config.add_view(general.edit, route_name='cron.user.edit', renderer='templates/user/edit.pt', permission='loggedin')
    config.add_view(general.delete, route_name='cron.user.delete', renderer='templates/user/delete.pt', permission='loggedin')
    config.add_view(general.run, route_name='cron.user.run', renderer='templates/user/run.pt', permission='loggedin')
    config.add_view(general.run_now, route_name='cron.user.run_now', renderer='templates/user/run_now.pt', permission='loggedin')
    # config.add_view(general.check, route_name='cron.user.check', renderer='string', permission='loggedin')
    config.add_view(general.pause, route_name='cron.user.pause', permission='loggedin')
    config.add_view(general.resume, route_name='cron.user.resume', permission='loggedin')
    config.add_view(general.unlock, route_name='cron.user.unlock', permission='loggedin')
    
    config.add_view(general.human_time_view, route_name='cron.human_time', renderer='templates/user/human_time.pt', permission='loggedin')
    config.add_view(general.human_time_test, route_name='cron.human_time_test', renderer='string')

def log_views(config):
    from .views import logs
    
    config.add_route('cron.logs.view', 'logs/view/{log_id}')
    config.add_route('cron.logs.view_for_job', 'logs/view_for_job/{job_id}')
    config.add_route('cron.logs.view_for_user', 'logs/view_for_user/{user_id}')
    config.add_route('cron.logs.view_for_time', 'logs/view_for_time')
    
    config.add_view(logs.view, route_name='cron.logs.view', renderer='templates/logs/view.pt', permission='loggedin')
    config.add_view(logs.view_for_job, route_name='cron.logs.view_for_job', renderer='templates/logs/list.pt', permission='loggedin')
    config.add_view(logs.view_for_user, route_name='cron.logs.view_for_user', renderer='templates/logs/list.pt', permission='loggedin')
    config.add_view(logs.view_for_time, route_name='cron.logs.view_for_time', renderer='templates/logs/list.pt', permission='cron.admin')

def admin_views(config):
    from .views import admin
    
    config.add_route('cron.admin.home', 'admin/home')
    config.add_route('cron.admin.job_types', 'admin/job_types')
    
    config.add_view(admin.home, route_name='cron.admin.home', renderer='templates/admin/home.pt', permission='cron.admin')
    config.add_view(admin.job_types, route_name='cron.admin.job_types', renderer='templates/admin/job_types.pt', permission='cron.admin')

def init_auth():
    from ..system.lib import auth
    
    auth.add("cron", 'User', set())
    ag = auth.add("cron", 'Admin', {'admin'})
    auth.add("cron", 'Super user', ag | {'su'}, rank=4)

def includeme(config):
    # dev_views(config)
    user_views(config)
    admin_views(config)
    log_views(config)
    
    init_auth()
    
    # 
    from .jobs import (
        dummy_job,
    )
    
    from .lib import cron_f
    from ...core.hooks import append_to_hook
    
    append_to_hook("startup", cron_f.collect_instances)
    
    from ...core.commands import register_commands
    from .commands import cron
    
    register_commands(cron)
    
    
    

