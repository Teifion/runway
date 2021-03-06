from . import site_settings_f
from collections import OrderedDict, namedtuple

def sort_menu(the_menu):
    orders = ["%s|%s" % (str(m['order']).zfill(5), m['id']) for m in the_menu.values()]
    orders.sort()
    
    new_menu = OrderedDict()
    for n in map(lambda v: v.split("|")[1], orders):
        new_menu[n] = the_menu[n]
    
    return new_menu

def order_menus():
    site_settings_f._hidden_settings['site_menu'] = sort_menu(site_settings_f._hidden_settings['site_menu'])


"""
A set of functions for adding render data to the request
"""

_dropdown_menu = namedtuple("dropdown_menu", [
    "label", "style", "icon", "badge_colour", "badge_body", "contents"
])
def dropdown_menu(label, style, icon, badge_colour, badge_body, contents=[]):
    return _dropdown_menu(label, style, icon, badge_colour, badge_body, contents)

_dropdown_menu_item = namedtuple("dropdown_menu_item", [
    "title", "muted_text", "icon", "body", "url", "label_colour", "label_text"
])
def dropdown_menu_item(title, muted_text, icon, body, url, label_colour="", label_text=""):
    return _dropdown_menu_item(title, muted_text, icon, body, url, label_colour, label_text)
