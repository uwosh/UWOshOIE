import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Products.UWOshOIE.tests.uwoshoietestcase import UWOshOIETestCase, MockMailHost
from Products.CMFCore.WorkflowCore import WorkflowException

class TestStateFAHeldIncomplete(UWOshOIETestCase):
    """ Test Incomplete state
        has transitions addComment, decline, holdForFAIncomplete, recheckForFAHold, waitForPrintedMaterials, withdraw
    """
    
    def afterSetUp(self):
        self.acl_users = self.portal.acl_users
        self.portal_workflow = self.portal.portal_workflow
        self.portal_registration = self.portal.portal_registration
        
        self.mockMailHost()
        
        self.createUsers()
        
    def createFAHeldIncompleteApplication(self):
        
        self.login(self._default_user)
        self.portal.invokeFactory(type_name="OIEStudentApplication", id="testapplication")
    
        app = self.portal['testapplication']
        
        self.fill_out_application(app)
        app.setHoldApplication('HOLD')
        self.portal_workflow.doActionFor(app, 'submit')
    
        return app
        
    def test_should_be_in_FAHeldIncomplete_state(self):
        app = self.createFAHeldIncompleteApplication()
        
        self.assertEquals('FAHeldIncomplete', self.getState(app))
        
    def test_should_be_able_to_addComment(self):
        app = self.createFAHeldIncompleteApplication()
        
        self.login(self._default_user)
        self.portal_workflow.doActionFor(app, 'addComment')
        self.assertEquals('FAHeldIncomplete', self.getState(app))
        self.logout()
        
    def test_should_be_able_to_ApproveForFA(self):
        app = self.createFAHeldIncompleteApplication()
        
        self.login('program_manager')
        self.portal_workflow.doActionFor(app, 'approveForFA')
        self.assertEquals('waitingForPrintMaterials', self.getState(app))
        self.logout()
        
    def test_should_be_able_to_decline(self):
        app = self.createFAHeldIncompleteApplication()
        
        self.login('director')
        self.portal_workflow.doActionFor(app, 'decline')
        self.assertEquals('declined', self.getState(app))
        self.logout()
        
    def test_should_be_able_to_withdraw(self):
        app = self.createFAHeldIncompleteApplication()
        
        self.login(self._default_user)
        self.portal_workflow.doActionFor(app, 'withdraw')
        self.assertEquals('withdrawn', self.getState(app))
        self.logout()
        
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestStateFAHeldIncomplete))

    return suite

if  __name__ == '__main__':
    framework()
