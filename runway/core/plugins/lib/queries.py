from ...base import DBSession
from ..models.plugins import Plugin

def get_plugins():
    return DBSession.query(Plugin).order_by(Plugin.name.asc())
