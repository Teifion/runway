from ....core.apis import APIHandler
from ..lib import exceptions_f

class ExceptionCount(APIHandler):
    name = "dev.exception_count"
    group = "Developer"
    label = "Exception count"
    description = """A count of the number of unhandled exceptions in the system."""
    documentation = """HTML DOC"""
    location = __file__
    
    permissions = []
    
    def __call__(self, request, test_mode=False):
        return exceptions_f.exception_count(request.user.id).get(None, 0)
