from ....core.lib import common
from ..lib import docs_f

def home(request):
    layout      = common.render("viewer")
    pre_content = common.render("general_menu")
    
    request.add_documentation("documentation.help")
    
    return dict(
        title       = "Documentation: Home",
        layout      = layout,
        pre_content = pre_content,
        
        **docs_f.get_structured_docs()
    )

def keyword(request):
    layout      = common.render("viewer")
    pre_content = common.render("general_menu")
    
    return dict(
        title       = "Documentation: Keywords",
        layout      = layout,
        pre_content = pre_content,
        
        **docs_f.get_structured_docs(request.matchdict['keyword'])
    )

def doc_list(request):
    layout      = common.render("viewer")
    pre_content = common.render("general_menu")
    
    docs = list(docs_f._docs.keys())
    docs.sort()
    
    return dict(
        title       = "Documentation: Keywords",
        layout      = layout,
        pre_content = pre_content,
        docs        = docs,
    )