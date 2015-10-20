"""
Due to the way the import procedure works you need to use the full
namespace path for the import such as:

    from venustate.core.system.tests.user_tests import *

I'm not sure why this is but it's the best I could do for now
"""

# from venustate.core.system.tests.user_tests import *
# from venustate.core.testing.tests.site_tests import *

# from venustate.core.system.tests.form_validation_tests import *

from venustate.plugins.call_audit.tests.lifecycle_tests import *

# from venustate.core.admin.tests.command_tests import *
# from venustate.core.testing.tests.testing_tests import *
