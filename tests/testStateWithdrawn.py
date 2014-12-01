import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Products.UWOshOIE.tests.uwoshoietestcase import UWOshOIETestCase, MockMailHost
from Products.CMFCore.WorkflowCore import WorkflowException

class TestStateWithdrawn(UWOshOIETestCase):
    """ Test Incomplete state
        has transitions addComment, decline, holdForFAIncomplete, recheckForFAHold, waitForPrintedMaterials, withdraw
    """
    
    def afterSetUp(self):
        self.acl_users = self.portal.acl_users
        self.portal_workflow = self.portal.portal_workflow
        self.portal_registration = self.portal.portal_registration
        
        self.mockMailHost()
        
        self.createUsers()
        
    def createWithdrawnApplication(self):
        
        self.login(self._default_user)
        self.portal.invokeFactory(type_name="OIEStudentApplication", id="testapplication")
    
        app = self.portal['testapplication']
        
        self.fill_out_application(app)

        self.portal_workflow.doActionFor(app, 'withdraw')
    
        self.logout()
    
        return app
        
    def test_should_be_in_the_withdrawn_state(self):
        app = self.createWithdrawnApplication()
        
        self.assertEquals('withdrawn', self.getState(app))
        
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestStateWithdrawn))

    return suite

if  __name__ == '__main__':
    framework()
