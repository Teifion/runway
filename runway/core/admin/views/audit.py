from pyramid.httpexceptions import HTTPFound
from ...lib import common
from ..lib import audit_f

# from ....core.system.js_widgets import UserPicker
# from ...cron.models import CronJob
# from ...cron.lib import cron_f
# from ...system.lib import site_settings_f
# from ....core.hooks.lib.funcs import call_hook
# from ..lib import stats_f, admin_f
# from datetime import datetime
# from collections import OrderedDict

def list_logs(request):
    layout = common.render("viewer")
    
    # request.add_documentation("admin.user")
    # request.add_documentation("admin.settings")
    
    return dict(
        title  = "Admin: Home",
        layout = layout,
        logs   = audit_f.get_recent_logs(),
    )
