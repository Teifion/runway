from ....core.commands.lib import funcs
from ....core.system.lib import user_f
import transaction
from ...base import DBSession
from ...system.models.user import (
    User,

)

def activate_user(*user_ids):
    """
    [String|Int] -> IO String
    Taking in usernames and/or user ids. With each valid user it sets them to be active.
    """
    
    ids = map(funcs.int_if_int, user_ids)
    names = []
    
    with transaction.manager:
        for uid in ids:
            the_user = user_f.get_user(uid, allow_groups=False)
            the_user.active = True
            DBSession.add(the_user)
            
            names.append("{} ({})".format(the_user.username, the_user.id))
    
    if len(names) == 1:
        return "{} was activated".format(", ".join(names))
    return "{} were all activated".format(", ".join(names))

def deactivate_user(*user_ids):
    """
    [String|Int] -> IO String
    Taking in usernames and/or user ids. With each valid user it deactivates them.
    """
    
    ids = map(funcs.int_if_int, user_ids)
    names = []
    
    with transaction.manager:
        for uid in ids:
            the_user = user_f.get_user(uid, allow_groups=False)
            the_user.active = False
            DBSession.add(the_user)
            
            names.append("{} ({})".format(the_user.username, the_user.id))
    
    if len(names) == 1:
        return "{} was deactivated".format(", ".join(names))
    return "{} were all deactivated".format(", ".join(names))
