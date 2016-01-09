from pyramid.httpexceptions import HTTPFound
from pyramid.response import Response
from ...lib.common import GracefulException
from ...lib import common
from ..lib import exceptions_f
from ...system.lib import site_settings_f, errors_f, schema_f
from ...base import Base, DBSession
import os

def home(request):
    layout      = common.render("viewer")
    
    request.add_documentation("dev.home")
    
    return dict(
        title         = "Developer: Home",
        layout        = layout,
        error_count   = exceptions_f.exception_count(request.user.id),
        
        instance_uuid = errors_f._instance_uuid,
        instance_startup = errors_f._startup_time,
    )

def restart(request):
    layout      = common.render("viewer")
    
    request.add_documentation("dev.home")
    
    message = None
    
    if "confirm" in request.params:
        os.system("touch {}".format(site_settings_f._server_ini))
        message = "warning", "Server restarting"
    
    return dict(
        title       = "Developer: Restart",
        layout      = layout,
        message     = message,
        
        ini_file    = site_settings_f._server_ini,
    )

def generate_exception(request):
    exception_type = request.params.get('type', '')
    
    request.add_documentation("dev.home")
    
    if exception_type == "general":
        raise Exception("General Exception")
    
    elif exception_type == "graceful_with_log":
        raise GracefulException("Graceful exception raised", "This is the message accompanying the general exception. Additionally this exception has been logged.", log_anyway=True)
    
    elif exception_type == "graceful":
        # By default raise a graceful
        raise GracefulException("Graceful exception raised", "This is the message accompanying the general exception.")

def installer(request):
    layout      = common.render("viewer")
    
    request.add_documentation("dev.home")
    
    message = None
    
    if "confirm" in request.params:
        engine = DBSession.get_bind()
        Base.metadata.create_all(engine)
        message = "success", "Tables have been installed"
    
    return dict(
        title       = "Developer: Installer",
        layout      = layout,
        message     = message,
    )

def schemas(request):
    layout      = common.render("viewer")
    
    request.add_documentation("dev.home")
    
    return dict(
        title       = "Developer: Schemas",
        layout      = layout,
        schemas     = schema_f.get_versions(),
    )

# here = "/".join(os.path.abspath(os.path.dirname(__file__)).split("/")[0:-3])
# print("\n\n")
# print(here)
# print("\n\n")

def get_backup(request):
    """
    curl -d "username=root" -d "password=password" --cookie-jar /tmp/venu_cookiejar http://my_site.com/login?redirect=cmVkaXJlY3Q6Oi9kZXYvZ2V0X2JhY2t1cA==
    curl --cookie /tmp/venu_cookiejar http://my_site.com/dev/get_backup
    """
    file_path = site_settings_f.get_setting("runway.latest_backup")
    
    with open(file_path) as f:
        data = f.read()
    
    return Response(body=data, content_type='text/plain', content_disposition='attachment; filename="database_backup"')
