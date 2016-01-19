from ....core.lib import common
from ..lib import docs_f

def home(request):
    layout      = common.render("viewer")
    
    request.add_documentation("documentation.help")
    
    return dict(
        title       = "Documentation: Home",
        layout      = layout,
        
        **docs_f.get_structured_docs()
    )

def raw_doc_list(request):
    output = []
    
    for the_doc in docs_f._docs.values():
        output.append("{},{}".format(the_doc.name, request.route_url(the_doc.route)))
    
    return "\n".join(output)

def keyword(request):
    layout      = common.render("viewer")
    
    return dict(
        title       = "Documentation: Keywords",
        layout      = layout,
        
        **docs_f.get_structured_docs(request.matchdict['keyword'])
    )

def doc_list(request):
    layout      = common.render("viewer")
    
    docs = list(docs_f._docs.keys())
    docs.sort()
    
    return dict(
        title       = "Documentation: Keywords",
        layout      = layout,
        docs        = docs,
    )