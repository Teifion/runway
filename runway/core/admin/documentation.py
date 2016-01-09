from ...core.documentation.models import Documentation

class UserAdministration(Documentation):
    name = "admin.user"
    route = "admin.documentation.user"
    
    title = "User administration"
    brief = "How to manage the users in the application."
    keywords = ("admin", "user", "groups")
    
    icons = ("wrench", "user")
    icon_colour = "warning"

class AddingUsers(Documentation):
    name = "admin.adding_users"
    route = "admin.documentation.adding_users"
    
    title = "Adding users"
    brief = "How to add users to the application."
    keywords = ("admin", "user", "groups")
    
    icons = ("plus", "user")
    icon_colour = "warning"

class Settings(Documentation):
    name = "admin.settings"
    route = "admin.documentation.settings"
    
    title = "Settings administration"
    brief = "An explanation of the settings in the application."
    keywords = ("admin", "settings")
    
    icons = ("wrench", "gears")
    icon_colour = "warning"

class Permissions(Documentation):
    name = "admin.permissions"
    route = "admin.documentation.permissions"
    
    title = "Permissions administration"
    brief = "An explanation of the permissions in the application."
    keywords = ("admin", "permissions")
    
    icons = ("wrench", "gears")
    icon_colour = "warning"
