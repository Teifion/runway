route_prefix = "wordy"

site_settings = [
    ["Games", [
        ("wordy.enabled", "admin", "Enabled", "boolean", "True", """Allows easy disabling of Wordy"""),
    ]],
]

site_menu = {
    "id": "wordy",
    "permissions": [],
    "route":"wordy.home",
    "icon": "",
    "text": "Wordy",
    "order": 99,
}

def admin_views(config):
    from .views import admin
    
    config.add_route('empty_module.admin.home', 'admin/home')
    
    config.add_view(admin.home, route_name='empty_module.admin.home', renderer='templates/admin/home.pt', permission='empty_module.admin')

def game_views(config):
    from .views import game
    
    config.add_route('wordy.new_game', '/new_game')
    config.add_route('wordy.rematch', '/rematch/{game_id}')
    
    config.add_route('wordy.view_game', '/game/{game_id}')
    config.add_route('wordy.check_status', '/check_status/{game_id}')
    config.add_route('wordy.check_turn', '/check_turn/{game_id}')
    config.add_route('wordy.make_move', '/make_move/{game_id}')
    config.add_route('wordy.test_move', '/test_move/{game_id}')
    config.add_route('wordy.matchmake', '/matchmake')
    
    config.add_view(game.new_game, route_name='wordy.new_game', renderer='templates/game/new_game.pt', permission='loggedin')
    config.add_view(game.matchmake, route_name='wordy.matchmake', renderer='templates/general/matchmake.pt', permission='loggedin')
    config.add_view(game.view_game, route_name='wordy.view_game', renderer='templates/game/view_game.pt', permission='loggedin')
    
    config.add_view(game.make_move, route_name='wordy.make_move', renderer='string', permission='loggedin')
    config.add_view(game.rematch, route_name='wordy.rematch', renderer='string', permission='loggedin')
    config.add_view(game.check_turn, route_name='wordy.check_turn', renderer='string', permission='loggedin')
    config.add_view(game.check_status, route_name='wordy.check_status', renderer='string', permission='loggedin')

def general_views(config):
    from .views import general
    
    config.add_route('wordy.home', '/home')
    config.add_route('wordy.blocked', '/blocked')
    config.add_route('wordy.stats', '/stats')
    config.add_route('wordy.head_to_head_stats', '/head_to_head_stats')
    config.add_route('wordy.preferences', '/preferences')
    
    config.add_view(general.home, route_name='wordy.home', renderer='templates/general/home.pt', permission='loggedin')
    config.add_view(general.blocked, route_name='wordy.blocked', renderer='templates/general/blocked.pt', permission='loggedin')
    config.add_view(general.stats, route_name='wordy.stats', renderer='templates/general/stats.pt', permission='loggedin')
    config.add_view(general.preferences, route_name='wordy.preferences', renderer='templates/general/preferences.pt', permission='loggedin')
    config.add_view(general.head_to_head_stats, route_name='wordy.head_to_head_stats', renderer='templates/general/head_to_head_stats.pt', permission='loggedin')

# def init_auth():
#     from ..system.lib import auth
#     ag = auth.add("empty_module", 'Admin', {'admin'}, rank=1)

def includeme(config):
    game_views(config)
    general_views(config)
    # admin_views(config)
