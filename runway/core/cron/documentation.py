from ...core.documentation.models import Documentation

class AddCronJob(Documentation):
    name = "cron.add"
    route = "cron.documentation.add"
    
    title = "Adding cron jobs"
    brief = "Adding cron jobs."
    keywords = ("dev", "cron", "quick-guide")
    
    icons = ("power-off", "add")
    icon_colour = "info"
