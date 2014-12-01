import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Products.UWOshOIE.tests.uwoshoietestcase import UWOshOIETestCase, MockMailHost
from Products.CMFCore.WorkflowCore import WorkflowException

class TestStateIncomplete(UWOshOIETestCase):
    """ Test Incomplete state
        has transitions addComment, decline, holdForFAIncomplete, recheckForFAHold, waitForPrintedMaterials, withdraw
    """
    
    def afterSetUp(self):
        self.acl_users = self.portal.acl_users
        self.portal_workflow = self.portal.portal_workflow
        self.portal_registration = self.portal.portal_registration
        
        self.mockMailHost()
        
        self.createUsers()
        
    def createIncompleteApplication(self):
        
        self.login(self._default_user)
        self.portal.invokeFactory(type_name="OIEStudentApplication", id="testapplication")
    
        app = self.portal['testapplication']
        
        self.fill_out_application(app)

        self.portal_workflow.doActionFor(app, 'submit')
    
        self.logout()
    
        return app
    
    def test_should_be_in_incomplete_state(self):
        app = self.createIncompleteApplication()
        
        self.assertEquals('incomplete', self.getState(app))
        
    def test_should_be_able_to_add_comment(self):
        app = self.createIncompleteApplication()
        
        self.login(self._default_user)
        self.portal_workflow.doActionFor(app, 'addComment')
        self.assertEquals('incomplete', self.getState(app))

    def test_should_be_able_to_decline(self):
        app = self.createIncompleteApplication()
        
        self.login('director')
        self.portal_workflow.doActionFor(app, 'decline')
        self.assertEquals('declined', self.getState(app))
        
    def test_should_be_able_to_recheckForFAHold(self):
        app = self.createIncompleteApplication()
        
        self.login('front_line_advisor')
        app.setHoldApplication('HOLD')
        self.portal_workflow.doActionFor(app, 'recheckForFAHold')
        self.assertEquals('FAHeldIncomplete', self.getState(app))
        
    def test_should_be_able_to_waitForPrintedMaterials(self):
        app = self.createIncompleteApplication()
        
        self.login('front_line_advisor')
        self.portal_workflow.doActionFor(app, 'waitForPrintedMaterials')
        self.assertEquals('waitingForPrintMaterials', self.getState(app))
        
    def test_should_be_able_withdraw(self):
        app = self.createIncompleteApplication()
        
        self.login(self._default_user)
        self.portal_workflow.doActionFor(app, 'withdraw')
        self.assertEquals('withdrawn', self.getState(app))
        
        
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestStateIncomplete))

    return suite

if  __name__ == '__main__':
    framework()
