from ...core.documentation.models import Documentation

class DevHome(Documentation):
    name = "dev.home"
    route = "dev.documentation.home"
    
    title = "Runway developer documentation"
    brief = "How to use and develop with the Runway framework."
    keywords = ("dev",)
    
    icons = ("power-off",)
    icon_colour = "info"


class Widgets(Documentation):
    name = "dev.widgets"
    route = "dev.documentation.widgets"
    
    title = "Widget documentation"
    brief = "How to use and develop widgets."
    keywords = ("dev", "widgets")
    
    icons = ("gears", "power-off")
    icon_colour = "info"


class Testing(Documentation):
    name = "dev.testing"
    route = "dev.documentation.testing"
    
    title = "Testing documentation"
    brief = "How to use and develop testing."
    keywords = ("dev", "testing")
    
    icons = ("eyedropper", "power-off")
    icon_colour = "info"


class FormValidation(Documentation):
    name = "dev.form_validation"
    route = "dev.documentation.form_validation"
    
    title = "Form validation documentation"
    brief = "How to use and develop form_validation."
    keywords = ("dev", "form_validation")
    
    icons = ("filter", "power-off")
    icon_colour = "info"


class NewModule(Documentation):
    name = "dev.new_module"
    route = "dev.documentation.new_module"
    
    title = "New module checklist"
    brief = "A list of steps to take in creating a new module."
    keywords = ("dev", "new_module")
    
    icons = ("plus", "power-off")
    icon_colour = "info"


class DemoMode(Documentation):
    name = "dev.demo_mode"
    route = "dev.documentation.demo_mode"
    
    title = "Demo mode documentation"
    brief = "How to add a demo mode command to your module."
    keywords = ("dev", "demo_mode")
    
    icons = ("play-circle-o", "power-off")
    icon_colour = "info"
