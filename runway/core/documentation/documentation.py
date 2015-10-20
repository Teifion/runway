from .models import Documentation

class DocumentationHelp(Documentation):
    name = "documentation.help"
    route = "documentation.help"
    
    title = "Using the documentation"
    brief = "A brief walkthrough of how documentation works on Venustate."
    keywords = ("documentation", "help")
    
    icons = ("question",)
    icon_colour = "info"

