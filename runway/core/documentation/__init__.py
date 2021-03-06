from ..lib import common
from .lib import docs_f

def basic_view(the_documentation):
    def f(request):
        layout      = common.render("viewer")
    
        
        for d in the_documentation.related_documents:
            request.add_documentation(d)
        
        request.is_documentation = True
        request.the_documentation = the_documentation
        
        return dict(
            title            = the_documentation.title,
            layout           = layout,
            
            doc_lookup       = docs_f._docs.get,
            
            the_documentation = the_documentation,
            documents_by_tag = docs_f.documents_by_tag,
            # old_documents_by_tag = docs_f.documents_by_tag(the_documentation, skip=[the_documentation.name]),
        )
    return f

def general_views(config):
    from .views import general
    
    config.add_route('documentation.home', 'home')
    config.add_route('documentation.keyword', 'keyword/{keyword}')
    config.add_route('documentation.doc_list', 'doc_list')
    config.add_route('documentation.raw_doc_list', 'raw_doc_list')
    
    config.add_view(general.home, route_name='documentation.home', renderer='templates/general/home.pt', permission='loggedin')
    config.add_view(general.keyword, route_name='documentation.keyword', renderer='templates/general/keyword.pt', permission='loggedin')
    config.add_view(general.doc_list, route_name='documentation.doc_list', renderer='templates/general/doc_list.pt', permission='developer')
    config.add_view(general.raw_doc_list, route_name='documentation.raw_doc_list', renderer='string', permission='developer')

def documentation_views(config):
    from . import documentation
    
    config.add_route('documentation.help', 'documentation/help')
    config.add_route('documentation.add', 'documentation/add')
    
    config.add_view(
        basic_view(documentation.DocumentationHelp),
        route_name='documentation.help',
        renderer="templates/general/help.pt",
        permission="loggedin"
    )
    
    config.add_view(
        basic_view(documentation.DocumentationQuickAdd),
        route_name='documentation.add',
        renderer="templates/general/add.pt",
        permission="developer"
    )

def includeme(config):
    general_views(config)
    documentation_views(config)
    
    from .lib import docs_f
    from ..hooks import append_to_hook, register_hook
    
    register_hook("collect_docs", "Called when documents are created, any calls to docs_f.document_function should be called via this, not via the startup hook.")
    
    append_to_hook("startup", docs_f.collect_instances)
    
    # from .widgets import (
    #     new_user_widget,
    # )

from .documentation import *
