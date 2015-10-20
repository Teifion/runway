from ...core.documentation.models import Documentation

class EditGroup(Documentation):
    name = "user.groups.edit_group"
    route = "user.groups.documentation.edit_group"
    
    title = "Editing groups group"
    brief = "How to edit groups and stuff like that"
    keywords = ("groups",)
    
    icons = ("wrench", "users")
    icon_colour = "danger"

# System widgets
class UserPickerWidget(Documentation):
    name = "system.widgets.user_picker"
    route = "system.widgets.documentation.user_picker"
    
    title = "User picker widget"
    brief = "xyz"
    keywords = ("widgets",)
    
    icons = ("wrench", "users")
    icon_colour = "danger"

class GroupPickerWidget(Documentation):
    name = "system.widgets.group_picker"
    route = "system.widgets.documentation.group_picker"
    
    title = "Group picker widget"
    brief = "xyz"
    keywords = ("widgets",)
    
    icons = ("wrench", "users")
    icon_colour = "danger"

class ComboPickerWidget(Documentation):
    name = "system.widgets.combo_picker"
    route = "system.widgets.documentation.combo_picker"
    
    title = "Combo picker widget"
    brief = "xyz"
    keywords = ("widgets",)
    
    icons = ("wrench", "users")
    icon_colour = "danger"
