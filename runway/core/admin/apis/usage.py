from ....core.apis import APIHandler
from ..lib import usage_f
import json

class UsageAPI(APIHandler):
    name = "admin.usage"
    group = "admin"
    label = "Usage"
    description = """Gets usage figures for the day so far"""
    documentation = """HTML DOC"""
    location = __file__
    
    permissions = []
    
    def __call__(self, request, test_mode=False):
        results = usage_f.daily_tally()
        
        jresult = {}
        
        for r in results:
            if jresult == {}:
                jresult['today'] = r[1]
            else:
                jresult['yesterday'] = r[1]
        
        return json.dumps(jresult)
