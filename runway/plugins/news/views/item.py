
def view(request):
    layout      = common.render("viewer")
    
    return dict(
        title    = "TODO",
        layout   = layout,
    )


def sign(request):
    layout      = common.render("viewer")
    
    return dict(
        title    = "TODO",
        layout   = layout,
    )
