from ..models import Documentation
from collections import OrderedDict, defaultdict
from functools import lru_cache
from ....core.hooks.lib.funcs import call_hook
import os

_base_path = os.path.abspath(os.path.dirname(__file__)).replace("core/documentation/lib", "")

_docs = {}
_keywords = defaultdict(list)

def document_function(full_file_path, the_function):
    """
    Any calls to this function should be via the "collect_docs" hook
    rather than the "startup" hook.
    """
    file_path = full_file_path.replace(_base_path, "/")
    
    print("\n\n")
    print(file_path)
    print(the_function.__doc__.strip())
    print(dir(the_function))
    # Print this so if we call this function by mistake we know what to search the codebase for
    print("Search code: stdhenrstoidnrs")
    print("\n\n")

def sort_docs(names):
    """
    Given a list of doc names it sorts them based
    on their ordering
    """
    lookup = {_docs[n].oname:n for n in names}
    ordered_sequence = list(lookup.keys())
    ordered_sequence.sort()
    
    return [lookup[oname] for oname in ordered_sequence]

def collect_instances():
    """
    Collects all the instances of Documentation classes, runs some
    grouping stuff on them and places them into _docs
    """
    for d in Documentation.__subclasses__():
        _docs[d.name] = d
        
        # Assign the section automatically
        d.section = d.name.split(".")[0].replace("_", " ").title()
        d.oname = str(d.ordering) + d.title
        
        if not d.indexed: continue
        
        # If the section name isn't in there, add it
        if d.section.lower() not in d.keywords:
            d.keywords = d.keywords + (d.section.lower(),)
        
        for k in d.keywords:
            _keywords[k].append(d.name)
    
    for k in _keywords.keys():
        _keywords[k] = sort_docs(_keywords[k])
    
    call_hook("collect_docs")

@lru_cache(maxsize=64)
def documents_by_tag(tag, *skip):
    # result = defaultdict(list)
    # for k in the_documentation.keywords:
    #     result[k] = tuple(filter(lambda d: d not in skip, _keywords[k]))
    
    result = []
    for dname, the_doc in _docs.items():
        if tag in the_doc.keywords and the_doc.name not in skip:
            result.append(the_doc)
    
    return result

def get_structured_docs(keyword=None):
    """
    Used to pull back the docs (sometimes a subset) in a structured and
    ordered manner
    """
    if keyword is None:
        source = _docs
    else:
        source = {k:_docs[k] for k in _keywords[keyword]}
    
    sections = set()
    by_section = defaultdict(list)
    
    # First pass, collect stuff
    for doc_name, the_doc in source.items():
        if not the_doc.indexed: continue
        
        sections.add(the_doc.section)
        by_section[the_doc.section].append(doc_name)
    
    # Second pass, order it
    sections = list(sections)
    sections.sort()
    
    output = {
        "sections": OrderedDict(),
        "docs": source
    }
    
    for s in sections:
        output['sections'][s] = sort_docs(by_section[s])
    
    # print("\n")
    # print(output)
    # print("\n")
    
    return output
