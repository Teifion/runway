"""

Settings are handled in the system.lib.settings_f library

Some settings are visible only to the dev side, the majority are visible in the admin.settings

To add a custom setting to the runway settings list you need to define the settings variable
in your module

    The structure of a group is:
    
    ["Group name", [
        (name, label, type, description),
        (name, label, type, description),
        ...
    ]]

    name -> the name of the setting itself (e.g. runway.users.enable_cron)
    label -> the text which appears to the admin (e.g. Enable Cron jobs)
    type -> the type of data stored
        boolean = checkbox
        str = textbox
        list:a,b,c = Dropdown list, values follow the colon and are comma separated
    description -> the description shown to the admin, HTML is allowed
    
    You can see an example of a settings list in system.__init__.settings



"""