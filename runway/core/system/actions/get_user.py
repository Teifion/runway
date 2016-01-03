from ....core.triggers import Action
from ....core.system.models.user import User
from ....core.system.lib import user_f
from datetime import date

class GetUser(Action):
    name = "system_get_user"
    group = "System"
    label = "Get User"
    description = """Gets user details from the database."""
    documentation = """HTML DOC"""
    location = __file__
    
    inputs = (
        ("user", User, "The User to pull from the database"),
    )
    
    outputs = (
        ("id", int, "User ID"),
        ("username", str, "Username (system name)"),
        ("display_name", str, "Display name"),
        ("email", str, "Email address"),
        ("join_date", date, "Date user joined"),
    )
    
    permissions = ["developer"]
    
    examples = [
        (
            {"user":1},
            {
                "id": 1,
                "username": "johns",
                "display_name": "John Smith",
                "email": "user@site.com",
                "join_date": date.today(),
            }
        ),
    ]
    
    def __call__(self, user, test_mode=False):
        if isinstance(user, int):
            user = user_f.get_user(user)
        
        return {
            "id": user.id,
            "username": user.username,
            "display_name": user.display_name,
            "email": user.email,
            "join_date": user.join_date,
        }
