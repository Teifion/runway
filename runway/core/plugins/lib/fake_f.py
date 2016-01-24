"""
A set of functions to use if your import fails. They do nothing
and return a value as chosen by you.
"""

def id(i):
    return i

def do_nothing(*args, **kwargs):
    pass

def empty_list(*args, **kwargs):
    return []
