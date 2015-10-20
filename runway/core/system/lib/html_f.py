from random import random

_double_click_template = """
<span style="{label_style}" id="dbc_label_{rnd}" ondblclick="$(dbc_label_{rnd}).hide(); $('#db_form_{rnd}').show(); $('#dbc_input_{rnd}').focus();">{value}</span>

<span id="db_form_{rnd}" style="display:none;">
    <form action="{form_url}" method="post" style="display:inline-block; width:100%;" >
       <input type="text" id="dbc_input_{rnd}" name="{name}" value="{value}" class="form-control" style="display:inline-block;width:100%;" onblur="$('#db_form_{rnd}').hide(); $(dbc_label_{rnd}).show();"/>
    </form>
</span>
"""

# <input style="display:none; margin:-2px;" type="text" name="value" id="%(input)s" size="%(size)s" value="" onblur="$('#%(label)s').load('web.py', {'mode':'edit_one_field','table':'%(table)s','field':'%(field)s','where':'%(where)s','value':$('#%(input)s').val()}, function () {$('#%(label)s').show(); $('#%(input)s').hide();});" />

def doubleclick_text(form_url, name, value, label_style=""):
    """Creates a label that when double clicked turns into a textbox, when the textbox loses focus, it saves itself"""
    
    return _double_click_template.format(
        rnd         = int(random() * 99999999),
        form_url    = form_url,
        label_style = label_style,
        name        = name,
        value       = value,
    )

def build_doubleclick_text(form_url, name, label_style=""):
    def f(url_suffix, value):
        return doubleclick_text(form_url + url_suffix, name, value, label_style)
    return f