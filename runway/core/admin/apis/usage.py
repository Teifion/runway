from ....core.apis import APIHandler
from ..lib import usage_f
import json
from datetime import date, timedelta

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
        
        today = date.today() - timedelta(days=1)
        yesterday = date.today() - timedelta(days=2)
        
        jresult = {}
        
        for r in results:
            if r[0] == today:
                jresult['today'] = r[1]
            elif r[0] == yesterday:
                jresult['yesterday'] = r[1]
        
        return json.dumps(jresult)
