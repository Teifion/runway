from ...core.documentation.models import Documentation

class AddAPIHandler(Documentation):
    name = "api.add_handler"
    route = "api.documentation.add_handler"
    
    title = "Adding API Handlers"
    brief = "Adding API Handlers."
    keywords = ("dev", "api", "quick-guide")
    
    icons = ("power-off", "add")
    icon_colour = "info"
