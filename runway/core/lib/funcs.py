"""
Allows us to compose functions
"""
idfunc = lambda x: x
def compose(f1=idfunc, f2=idfunc, *more_funcs):
    # Allows us an unlimited number of functions
    if len(more_funcs) > 0:
        f2 = compose(f2, *more_funcs)
    
    # The magic happens here
    def new_f(*args, **kwards):
        return f1(f2(*args, **kwards))
    return new_f

def keymap(the_dict):
    """Allows you to map over the keys of something"""
    return lambda key: the_dict[key]
