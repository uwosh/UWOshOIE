import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Products.UWOshOIE.tests.uwoshoietestcase import UWOshOIETestCase, MockMailHost
from Products.CMFCore.WorkflowCore import WorkflowException

class TestStateDeclined(UWOshOIETestCase):
    """ Test Incomplete state
        has transitions addComment, decline, holdForFAIncomplete, recheckForFAHold, waitForPrintedMaterials, withdraw
    """
    
    def afterSetUp(self):
        self.acl_users = self.portal.acl_users
        self.portal_workflow = self.portal.portal_workflow
        self.portal_registration = self.portal.portal_registration
        
        self.mockMailHost()
        
        self.createUsers()
        
    def createDeclinedApplication(self):
        
        self.login(self._default_user)
        self.portal.invokeFactory(type_name="OIEStudentApplication", id="testapplication")
    
        app = self.portal['testapplication']
        
        self.fill_out_application(app)

        self.portal_workflow.doActionFor(app, 'submit')
    
        self.logout()
        self.login('front_line_advisor')
        self.portal_workflow.doActionFor(app, 'decline')
    
        self.logout()
    
        return app
        
    def test_should_be_in_declined_state(self):
        app = self.createDeclinedApplication()
        
        self.assertEquals('declined', self.getState(app))
        
    def test_should_be_able_to_add_comment(self):
        app = self.createDeclinedApplication()
        
        self.login(self._default_user)
        self.portal_workflow.doActionFor(app, 'addComment')
        self.assertEquals('declined', self.getState(app))
        self.logout()
        
    def test_should_be_able_to_archive(self):
        app = self.createDeclinedApplication()
        
        self.login('front_line_advisor')
        self.portal_workflow.doActionFor(app, 'archive')
        self.assertEquals('archived', self.getState(app))
        self.logout()
        

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestStateDeclined))

    return suite

if  __name__ == '__main__':
    framework()
