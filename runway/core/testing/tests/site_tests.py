# from ..lib.test_f import RunwayTesterBase
from ..lib.test_f import RunwayTester, DummyRequest
from ...system.lib import errors_f
from ...lib import common

from ... import main
from ...base import DBSession
from ...system.models.user import UserPermissionGroup
import transaction

from pyramid.config import Configurator

# testing_dict = {
#     'pyramid.debug_notfound': 'false',
#     'pyramid.debug_routematch': 'false',
#     'testing_mode': 'True',
#     'pyramid.default_locale_name': 'en',
#     'pyramid.debug_authorization': 'false',
#     # 'pyramid.includes': '\npyramid_tm',
#     # 'sqlalchemy.url': 'postgresql+pypostgresql://venustate:123456@localhost:5432/venustate_testing'
# }

from zope.interface import Interface

from pyramid.interfaces import IRouteRequest
from pyramid.interfaces import IRoutesMapper
from pyramid.interfaces import IViewClassifier
from pyramid.interfaces import IView

from pyramid_debugtoolbar.panels import DebugPanel

_ = lambda x: x



# def __init__(self, request):
#     self.mapper = request.registry.queryUtility(IRoutesMapper)
#     if self.mapper is None:
#         self.has_content = False
#         self.is_active = False
#     else:
#         self.populate(request)

# def nav_title(self):
#     return _('Routes')

# def title(self):
#     return _('Routes')

# def url(self):
#     return ''



"""
Idea is to have something that checks we've got a template file for every view

class SiteTester(RunwayTester):
    def test_routes(self):
        app = self.get_app()
        request = DummyRequest()
        
        self.mapper = request.registry.queryUtility(IRoutesMapper)
        if self.mapper is None:
            self.fail("No mapper attribute to test with")
        else:
            self.populate(request)
        
        print(self.data)
    
    
    def populate(self, request):
        info = []
        mapper = self.mapper
        if mapper is not None:
            registry = request.registry
            routeinfo = getattr(registry, 'debugtoolbar_routeinfo', None)
            if routeinfo is None:
                routes = mapper.get_routes()
                for route in routes:
                    request_iface = registry.queryUtility(IRouteRequest,
                                                          name=route.name)
                    view_callable = None
                    if (request_iface is None) or (route.factory is not
                                                   None):
                        view_callable = '<unknown>'
                    else:
                        view_callable = registry.adapters.lookup(
                            (IViewClassifier, request_iface, Interface),
                            IView, name='', default=None)
                    predicates = []
                    for predicate in route.predicates:
                        text = getattr(predicate, '__text__', repr(predicate))
                        predicates.append(text)
                    info.append({'route':route,
                                 'view_callable':view_callable,
                                 'predicates':', '.join(predicates)})
                registry.debugtoolbar_routeinfo = info

            self.data = {
                'routes': registry.debugtoolbar_routeinfo,
                }    
    
    def old(self):
        pass
        # config = Configurator()
        # main.routes(config)
        
        # intro = config.introspector
        
        # print(intro.get_category('routes'))
        # common.dumps(intro)
        
        # for k, v in config.introspectable.items('routes'):
        #     print(k, v)
        
        # common.dumps(config.introspectable)
        
        # print(config.introspectable)
"""