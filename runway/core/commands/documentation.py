from ...core.documentation.models import Documentation

class CommandsAdd(Documentation):
    name = "commands.add"
    route = "commands.documentation.add"
    
    title = "Adding commands"
    brief = "A quick step-by-step on how to add new commands."
    keywords = ("commands", "quick-guide")
    
    # related_documents = (
    #     "commands.page1",
    #     "commands.page2",
    # )
    
    icons = ("power-off", "plus",)
    icon_colour = "info"
    
    ordering = 10
