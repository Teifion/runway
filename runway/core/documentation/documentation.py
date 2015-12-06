from .models import Documentation

class DocumentationHelp(Documentation):
    name = "documentation.help"
    route = "documentation.help"
    
    title = "Using the documentation"
    brief = "A brief walkthrough of how documentation works on Venustate."
    keywords = ("documentation", "help")
    
    icons = ("question",)
    icon_colour = "info"

class DocumentationQuickAdd(Documentation):
    name = "documentation.add"
    route = "documentation.add"
    
    title = "Adding documentation"
    brief = "A quick step-by-step on how to add new documentation."
    keywords = ("documentation", "quick-guide")
    
    icons = ("power-off", "plus",)
    icon_colour = "info"
