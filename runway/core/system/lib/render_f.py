from . import site_settings_f
from collections import OrderedDict

def sort_menu(the_menu):
    orders = ["%s|%s" % (str(m['order']).zfill(5), m['id']) for m in the_menu.values()]
    orders.sort()
    
    new_menu = OrderedDict()
    for n in map(lambda v: v.split("|")[1], orders):
        new_menu[n] = the_menu[n]
    
    return new_menu

def order_menus():
    site_settings_f._hidden_settings['side_menu'] = sort_menu(site_settings_f._hidden_settings['side_menu'])
    site_settings_f._hidden_settings['top_menu'] = sort_menu(site_settings_f._hidden_settings['top_menu'])