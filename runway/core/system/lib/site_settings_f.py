from ...base import DBSession
from ..models import (
    Setting,
)

from collections import namedtuple, defaultdict, OrderedDict
from datetime import datetime
RunwaySettingsCollection = namedtuple("RunwaySettingsCollection", ["modules", "template", "users", "system"])

_settings_collection = None
_server_ini = None

_settings_structure = []
_hidden_settings = {
    "site_menu": {},
    "render.site_menu": [],
}

def get_setting(name, default=None):
    r = DBSession.query(Setting.value).filter(Setting.name == name).first()
    if r == None: return default
    return r[0]

def _get_setting_object(name):
    return DBSession.query(Setting).filter(Setting.name == name).first()

def set_setting(name, value):
    the_setting = _get_setting_object(name)
    
    if the_setting is None:
        the_setting = Setting(name=name, value=value)
    else:
        the_setting.value = value
    
    DBSession.add(the_setting)

def get_settings(*names):
    if len(names) == 0:
        return {}
    
    r = DBSession.query(Setting.name, Setting.value).filter(Setting.name.in_(names)).order_by(Setting.name)
    
    result = OrderedDict()
    for k,v in r: result[k] = v
    
    return result

def get_settings_like(name):
    r = DBSession.query(Setting.name, Setting.value).filter(
        Setting.name.like(name),
    ).order_by(Setting.name)
    
    result = OrderedDict()
    for k,v in r: result[k] = v
    
    return result

def get_all_settings():
    r = DBSession.query(Setting.name, Setting.value).order_by(Setting.name)
    
    result = OrderedDict()
    for k,v in r: result[k] = v
    
    return result

def build_runway_settings_collection():
    settings = get_all_settings()
    
    result = {}
    result['modules'] = defaultdict(lambda: 'False')
    for k,v in settings.items():
        if "runway.modules." == k[:15]:
            result['modules'][k.replace("runway.modules.", "")] = v
    
    result['template'] = defaultdict(lambda: None)
    
    result['users'] = defaultdict(lambda: 'False')
    result['users']['allow_cron'] = settings.get('runway.users.allow_cron', "False")
    result['users']['allow_triggers'] = settings.get('runway.users.allow_triggers', "False")
    result['users']['allow_widgets'] = settings.get('runway.users.allow_widgets', "False")
    result['users']['allow_groups'] = settings.get('runway.users.allow_groups', "False")
    
    result['system'] = defaultdict(lambda: 'False')
    result['system']['name'] = settings.get('runway.system.name', "Runway")
    
    return RunwaySettingsCollection(**result)

def set_last_change():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    set_setting("runway.system.last_change", now)

def reboot_needed():
    changes = get_settings("runway.system.last_startup", "runway.system.last_change")
    
    last_startup = datetime.strptime(changes['runway.system.last_startup'], '%Y-%m-%d %H:%M:%S')
    last_change = datetime.strptime(changes['runway.system.last_change'], '%Y-%m-%d %H:%M:%S')
    
    return last_change > last_startup

def install_settings(setting_dict):
    all_settings = get_all_settings()
    
    for k,v in setting_dict.items():
        if k not in all_settings:
            DBSession.add(Setting(name=k, value=v))

def include_plugin(setting_list):
    group_keys = {v[0]:k for k, v in enumerate(_settings_structure)}
    
    for group_name, group_contents in setting_list:
        if group_name not in group_keys:
            _settings_structure.append([group_name, []])
            index = len(_settings_structure) - 1
        else:
            index = group_keys[group_name]
        
        _settings_structure[index][1].extend(group_contents)

def process_settings():
    _hidden_settings['render.site_menu'] = tuple(_hidden_settings['site_menu'].values())
