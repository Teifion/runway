from ...testing.lib.test_f import RunwayTester
from ...base import DBSession
from ...system.models.user import User
import transaction

class AdminTests(RunwayTester):
    def test_general(self):
        return
        app = self.get_app()
        
        self.make_request(
            app,
            "/documentation/home",
            "Error trying to view the Documentation homepage",
        )
    
    def test_all_documentation(self):
        app = self.get_app()
        
        raw_body = self.make_request(
            app,
            "/documentation/raw_doc_list",
            "Error trying to get the raw document list",
        )
        
        raw_list = raw_body.body.decode('utf-8')
        
        for doc_str in raw_list.split("\n"):
            doc_name, doc_path = doc_str.split(",")
            
            self.make_request(
                app,
                doc_path,
                "Error trying to view the documentation '{}' at '{}'".format(
                    doc_name,
                    doc_path,
                ),
            )
        
