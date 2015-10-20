from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import get_renderer
from ....core.lib import common
from ....core.system.lib import user_f

from ..lib import (
    db,
    rules,
)

from ..models import (
    WordyGame,
    WordyMove,
    WordyProfile,
    WordyWord,
)


# def home(request):
#     layout      = common.render("viewer")
#     pre_content = common.render("general_menu")
    
#     return dict(
#         title       = "Page title",
#         layout      = layout,
#         pre_content = pre_content,
#     )


def home(request):
    rules.check_allowed(request)
    
    # We call but don't query this so that we can assign a profile
    # if none exists
    db.get_profile(request.user.id)
    
    game_list    = list(db.get_game_list(request.user.id, mode="Our turn"))
    waiting_list = db.get_game_list(request.user.id, mode="Not our turn")
    
    names = []
    for g in game_list:
        names.extend(g.players)
    names = set(names)
    
    layout      = common.render("viewer")
    pre_content = common.render("general_menu")
    
    return dict(
        title        = "Wordy",
        game_list    = list(game_list),
        waiting_list = list(waiting_list),
        names        = db.get_names(names),
        layout       = layout,
        pre_content  = pre_content,
    )

def install(request):
    rules.check_allowed(request)
    
    if db.check_for_install():
        return HTTPFound(location=request.route_url("wordy.home"))
    
    if "wordlist" in request.params:
        f = request.params['wordlist'].file
        
        try:
            words = f.read().decode('latin-1')
        except Exception:
            words = f.read().decode('utf-8')
        
        db.install(words)
        
        # Register the achievements
        # achievement_functions.register(achievements.achievements)
        
        content = "Wordlist inserted correctly<br /><br /><a href='{route}' class='inbutton'>Wordy main menu</a>".format(
            route = request.route_url('wordy.home')
        )
    else:
        content = """
        <form tal:condition="the_doc != None" action="{route}" method="post" accept-charset="utf-8" style="padding:10px;" enctype="multipart/form-data">
            
            <label for="wordlist">Wordlist file:</label>
            <input type="file" name="wordlist" size="40">
            <br />
            
            <input type="submit" name="form.submitted" />
        </form>
        """.format(
            route = request.route_url('wordy.install')
        )
    
    layout      = common.render("viewer")
    pre_content = common.render("general_menu")
    
    return dict(
        title       = "Wordy installation",
        content     = content,
        layout      = layout,
        pre_content = pre_content,
    )

def stats(request):
    rules.check_allowed(request)
    
    stats = db.get_stats(request.user.id)
    
    layout      = common.render("viewer")
    pre_content = common.render("general_menu")
    
    return dict(
        title       = "Wordy stats",
        stats       = stats,
        layout      = layout,
        pre_content = pre_content,
    )

def head_to_head_stats(request):
    rules.check_allowed(request)
    message  = ""
    
    if "opponent_name" in request.params:
        opponent_name = request.params['opponent_name'].strip().upper()
        opponent = db.find_user(opponent_name)
        
    else:
        opponent_id = int(request.params['opponent_id'])
        opponent = db.find_user(opponent_id)
    
    stats = None
        
    if opponent is not None:
        stats = db.get_stats(request.user.id, opponent.id)
    else:
        message = "No opponent could be found"
    
    return dict(
        stats    = stats,
        message  = message,
        opponent = opponent,
    )

def preferences(request):
    rules.check_allowed(request)
    profile = db.get_profile(request.user.id)
    message = None
    
    if "matchmaking" in request.params:
        matchmaking = request.params['matchmaking']
        if matchmaking == "true":
            profile.matchmaking = True
        else:
            profile.matchmaking = False
        
        message = "success", "Changes saved"
    
    layout      = common.render("viewer")
    pre_content = common.render("general_menu")
    
    return dict(
        title       = "Wordy preferences",
        profile     = profile,
        message     = message,
        layout      = layout,
        pre_content = pre_content,
    )

def blocked(request):
    layout      = common.render("modal")
    
    return dict(
        title       = "Wordy is blocked",
        layout      = layout,
    )
