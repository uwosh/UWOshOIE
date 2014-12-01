import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Products.UWOshOIE.tests.uwoshoietestcase import UWOshOIETestCase, MockMailHost
from Products.CMFCore.WorkflowCore import WorkflowException

class TestStatePrivate(UWOshOIETestCase):
    """Test private state"""
    
    def afterSetUp(self):
        self.OIEworkflow = self.portal.portal_workflow['OIEStudentApplicationWorkflow']
        self.acl_users = self.portal.acl_users
        self.portal_workflow = self.portal.portal_workflow
        self.portal_registration = self.portal.portal_registration

        self.mockMailHost()
        
        self.createUsers()
        
    def test_should_not_be_able_to_create_appliaction_if_not_logged_in(self):
        try:
            self.portal.invokeFactory(type_name='OIEStudentApplication', id='testapplication')
            self.fail()
        except Exception, inst:
            pass
        
    def createPrivateApplication(self):
        self.login(self._default_user)

        self.portal.invokeFactory(type_name="OIEStudentApplication", id="testapplication")
        self.logout()

        return self.portal['testapplication']
        
    def test_application_should_be_private_after_creation(self):
        app = self.createPrivateApplication()
        
        self.assertEquals("OIEStudentApplicationWorkflow", self.portal_workflow.getWorkflowsFor(app)[0].id)
        self.assertEquals("private", self.getState(app))
    
    def test_should_be_able_to_addComment(self):
        app = self.createPrivateApplication()
        
        self.login(self._default_user)
        self.portal_workflow.doActionFor(app, 'addComment')
        self.assertEquals('private', self.getState(app))
    
    def test_should_be_able_to_submit(self):
        app = self.createPrivateApplication()
        self.fill_out_application(app)
        self.login(self._default_user)
        self.portal_workflow.doActionFor(app, 'submit')
        self.assertEquals('incomplete', self.getState(app))
        
    def test_should_be_able_to_withdraw(self):
        app = self.createPrivateApplication()
        
        self.login(self._default_user)
        self.portal_workflow.doActionFor(app, 'withdraw')
        self.assertEquals('withdrawn', self.getState(app))
    
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestStatePrivate))

    return suite

if  __name__ == '__main__':
    framework()
