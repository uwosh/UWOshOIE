import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Products.UWOshOIE.tests.uwoshoietestcase import UWOshOIETestCase


class TestStateConditionallyAdmitted(UWOshOIETestCase):
    """Ensure product is properly installed"""

    def afterSetUp(self):
        self.acl_users = self.portal.acl_users
        self.portal_workflow = self.portal.portal_workflow
        self.portal_registration = self.portal.portal_registration
        
        self.mockMailHost()
        
        self.createUsers()
        
    def createConditionallyAdmittedApplication(self):

        self.login(self._default_user)
        self.portal.invokeFactory(type_name="OIEStudentApplication", id="testapplication")

        app = self.portal['testapplication']

        self.fill_out_application(app)

        self.portal_workflow.doActionFor(app, 'submit')

        self.logout()
        self.login('front_line_advisor')
        self.portal_workflow.doActionFor(app, 'waitForPrintedMaterials')
        app.setWithdrawalRefund(True)
        app.setApplicationFeeOK(True)
        app.setUWSystemStatementOK(True)
        app.setUWOshkoshStatementOK(True)
        app.setTranscriptsOK(True)
        self.portal_workflow.doActionFor(app, 'sendForDirectorReview')
        self.logout()

        self.login('director')
        self.portal_workflow.doActionFor(app, 'sendForProgramManagerReview')
        self.logout()
        
        self.login('program_manager')
        self.portal_workflow.doActionFor(app, 'assertReadyForConditionalAdmit')
        self.portal_workflow.doActionFor(app, 'admitConditionally')
        self.logout()

        return app
        
    def test_should_be_in_conditionallyAdmitted_state(self):
        app = self.createConditionallyAdmittedApplication()
        
        self.assertEquals('conditionallyAdmitted', self.getState(app))

    def test_should_be_able_to_add_comment(self):
        app = self.createConditionallyAdmittedApplication()
        
        self.login(self._default_user)
        
        self.portal_workflow.doActionFor(app, 'addComment')
        self.assertEquals('conditionallyAdmitted', self.getState(app))
        
        self.logout()
        
    def test_should_be_able_to_decline(self):
        app = self.createConditionallyAdmittedApplication()
        
        self.login('director')
        self.portal_workflow.doActionFor(app, 'decline')
        self.logout()
        
        self.assertEquals('declined', self.getState(app))
        
    def test_should_be_able_to_manageDeadlines(self):
        app = self.createConditionallyAdmittedApplication()
        
        self.login('front_line_advisor')
        self.portal_workflow.doActionFor(app, 'manageDeadlines')
        self.logout()
        
        self.assertEquals('deadlineManagement', self.getState(app))
        
    def test_should_be_able_to_withdraw(self):
        app = self.createConditionallyAdmittedApplication()
        
        self.login(self._default_user)
        self.portal_workflow.doActionFor(app, 'withdraw')
        self.logout()
        
        self.assertEquals('withdrawn', self.getState(app))


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestStateConditionallyAdmitted))

    return suite
    
if  __name__ == '__main__':
    framework()
