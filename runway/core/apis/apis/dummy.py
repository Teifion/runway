from ....core.apis import APIHandler

class UsageAPI(APIHandler):
    name = "apis.dummy"
    group = "apis"
    label = "usage"
    description = """Dummy API, returns a string of 'Hello world'"""
    documentation = """HTML DOC"""
    location = __file__
    
    permissions = []
    
    def __call__(self, request, test_mode=False):
        return "Hello world"
