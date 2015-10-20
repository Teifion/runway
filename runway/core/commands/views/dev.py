from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import get_renderer
from ...lib import common
from ..lib import funcs
from ...cli.lib import cli_f

def list_commands(request):
    layout      = common.render("viewer")
    pre_content = common.render("general_menu")
    
    command_list = list(funcs._command_dict.keys())
    command_list.sort()
    
    return dict(
        title       = "Developer: Commands",
        layout      = layout,
        pre_content = pre_content,
        
        commands    = (funcs._command_dict[c] for c in command_list),
        html_text   = cli_f.html_text
    )
