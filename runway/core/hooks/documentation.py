from ...core.documentation.models import Documentation

class AddHook(Documentation):
    name = "hooks.add"
    route = "hooks.documentation.add"
    
    title = "Adding hooks"
    brief = "Adding hooks."
    keywords = ("dev", "hooks", "quick-guide")
    
    icons = ("power-off", "add")
    icon_colour = "info"
