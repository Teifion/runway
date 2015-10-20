from ...testing.lib.test_f import RunwayTester
from ...base import DBSession
import transaction

from ..commands import user

class CommandTests(RunwayTester):
    def test_commands(self):
        user.deactivate_user("root")
        user.activate_user("root")
        