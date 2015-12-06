from ...core.documentation.models import Documentation

class HookDocumentation(Documentation):
    name = "hooks.genearl"
    route = "admin.documentation.user"
    
    title = "User administration"
    brief = "How to manage the users in the application."
    keywords = ("admin", "user", "groups")
    
    icons = ("wrench", "user")
    icon_colour = "warning"

class QuickAddHook(Documentation):
    name = "hooks.add"
    route = "admin.documentation.user"
    
    title = "User administration"
    brief = "How to manage the users in the application."
    keywords = ("admin", "user", "groups")
    
    icons = ("wrench", "user")
    icon_colour = "warning"
