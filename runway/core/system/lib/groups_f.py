from ...system.lib import render_f

def groups_pre_render(request):
    if request.runway_settings.users['allow_groups'] == 'True':
        request.render['user_links'].append(
            render_f.dropdown_menu_item("", "", "users", "Groups", request.route_url('user.groups.list'))
        )
