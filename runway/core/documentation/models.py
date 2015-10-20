class Documentation(object):
    """A documentation page"""
    
    name = ""
    route = ""
    
    title = ""
    brief = ""
    keywords = ()
    
    # A set of related documentation, much like on a normal page
    related_documents = []
    
    icons = ()
    icon_colour = ""
    permissions = []
    
    # Set to False if you don't want it to appear on the documentation
    # index screen or when searching by keyword
    indexed = True
    
    # The ordering value of the documentation item
    # numbers should be between 10 and 99 inclusive
    # It will sort Ascending (Low to high)
    ordering = 50
