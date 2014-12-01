import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Products.UWOshOIE.tests.uwoshoietestcase import UWOshOIETestCase
from Products.CMFCore.WorkflowCore import WorkflowException

class TestTransitionSendForFacultyReview(UWOshOIETestCase):
    """Ensure product is properly installed"""

    def createApplication(self):

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

        return app
        
    def test_program_manager_should_be_able_to_perform_action(self):
        app = self.createApplication()
        
        self.login('program_manager')
        self.portal_workflow.doActionFor(app, 'sendForFacultyReview')
        self.assertEquals('facultyReview', self.getState(app))
        
    def test_other_roles_should_not_be_able_to_perform(self):
        app = self.createApplication()
        
        for user in self._all_users:
            if user != 'program_manager':
                self.login(user)
                self.assertRaises(WorkflowException, self.portal_workflow.doActionFor, app, 'sendForFacultyReview')
                
    def test_should_send_email(self):
        app = self.createApplication()
        self.portal.MailHost.clearEmails()

        self.login('program_manager')
        self.portal_workflow.doActionFor(app, 'sendForFacultyReview')
        self.assertEquals(1, self.portal.MailHost.getEmailCount())
    
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestTransitionSendForFacultyReview))

    return suite
    
if  __name__ == '__main__':
    framework()
