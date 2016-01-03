from ...core.documentation.models import Documentation

class Add(Documentation):
    name = "triggers.add"
    route = "triggers.documentation.add"
    
    title = "Adding triggers"
    brief = "A reference on how to add triggers"
    
    related_documents = (
        # "triggers.page1",
        # "triggers.page2",
    )
    keywords = ("dev", "hooks", "quick-guide")
    
    icons = ("power-off", "add")
    icon_colour = "info"
