import re
from datetime import datetime
import transaction
from sqlalchemy import func, or_

from ...base import DBSession
from ..models import AuditLog

# from ..models import (
#     UserLog,
#     LogStats,
#     ActionLog,
# )

ignored_filetypes = re.compile(r"(css|js|html|png|jpg|jpeg|ico|gif)$")
section_grep = re.compile(r"(?:/venustate)?/([a-zA-Z0-9_]+?)/")

def audit_log(request, user, action, details, timestamp=None):
    if timestamp is None:
        timestamp = datetime.now()
    
    DBSession.add(AuditLog(
        user = user,
        action = action,
        details = details,
        timestamp = timestamp,
        ip = request.remote_addr if request.remote_addr != None else '',
    ))
