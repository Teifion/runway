from collections import defaultdict

hooks = defaultdict(list)

_hook_info = {}

import logging
log = logging.getLogger(__name__)

def register_hook(name, description):
    _hook_info[name] = description

def append_to_hook(hook_name, handler):
    hooks[hook_name].append(handler)

def call_hook(hook_name, **kwargs):
    for handler in hooks[hook_name]:
        try:
            handler(**kwargs)
        except Exception:
            log.debug("Tried to run handler of {}".format(str(handler)))
            raise
        