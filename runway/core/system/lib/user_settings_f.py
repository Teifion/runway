from ...base import DBSession
from ..models import (
    UserSetting,
)

from collections import namedtuple, defaultdict, OrderedDict
from datetime import datetime
RunwaySettingsCollection = namedtuple("RunwaySettingsCollection", ["system"])

_settings_collection = None
# _server_ini = None

_settings_structure = []
_hidden_settings = {
    # "side_menu": {},
    # "top_menu": {},
    
    # "render.side_menu": [],
    # "render.top_menu": [],
}

def get_setting(user_id, name, default=None):
    r = DBSession.query(UserSetting.value).filter(UserSetting.name == name, UserSetting.user == user_id).first()
    if r == None: return default
    return r[0]

def _get_setting_object(user_id, name):
    return DBSession.query(UserSetting).filter(UserSetting.name == name, UserSetting.user == user_id).first()

def set_setting(user_id, name, value):
    the_setting = _get_setting_object(user_id, name)
    
    if the_setting is None:
        the_setting = UserSetting(user=user_id, name=name, value=value)
    else:
        the_setting.value = value
    
    DBSession.add(the_setting)

def get_settings(user_id, *names):
    r = DBSession.query(
        UserSetting.name,
        UserSetting.value
    ).filter(
        UserSetting.user == user_id,
        UserSetting.name.in_(names)
    ).order_by(
        UserSetting.name
    )
    
    result = OrderedDict()
    for k,v in r: result[k] = v
    
    return result

def get_many_users_settings(user_ids, names):
    if len(user_ids) == 0 or len(names) == 0:
        return defaultdict(dict)
    
    r = DBSession.query(
        UserSetting.user,
        UserSetting.name,
        UserSetting.value,
    ).filter(
        UserSetting.user.in_(user_ids),
        UserSetting.name.in_(names)
    )
    
    result = defaultdict(dict)
    for u,n,v in r:
        result[u][n] = v
    
    return result

def get_settings_like(user_id, name):
    raise Exception("Should this function be removed?")
    r = DBSession.query(UserSetting.name, UserSetting.value).filter(
        UserSetting.name.like(name),
        UserSetting.user == user_id
    ).order_by(UserSetting.name)
    
    result = OrderedDict()
    for k,v in r: result[k] = v
    
    return result

def get_all_settings(user_id):
    r = DBSession.query(
        UserSetting.name,
        UserSetting.value
    ).filter(
        UserSetting.user == user_id
    ).order_by(
        UserSetting.name
    )
    
    result = OrderedDict()
    for k,v in r: result[k] = v
    
    return result

def build_runway_settings_collection():
    raise Exception("Should this function be removed?")
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
    result['system']['name'] = settings.get('runway.system.name', "Venustate")
    
    return RunwaySettingsCollection(**result)

def install_settings(setting_dict):
    raise Exception("Should this function be removed?")
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
    """
    This is called at startup, currently it is just a placeholder incase we need to add something.
    """
    
    pass
