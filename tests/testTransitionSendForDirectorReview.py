import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Products.UWOshOIE.tests.uwoshoietestcase import UWOshOIETestCase
from Products.CMFCore.WorkflowCore import WorkflowException


class TestTransitionSendForDirectorReview(UWOshOIETestCase):
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
        self.logout()
        
        return app
        
    def test_front_line_advisor_should_be_able_to_do_action_when_required_fields_are_set(self):
        app = self.createApplication()
        
        self.login('front_line_advisor')
        app.setWithdrawalRefund(True)
        app.setApplicationFeeOK(True)
        app.setUWSystemStatementOK(True)
        app.setUWOshkoshStatementOK(True)
        app.setTranscriptsOK(True)
        self.portal_workflow.doActionFor(app, 'sendForDirectorReview')
        self.assertEquals('needsDirectorReview', self.getState(app))
       
    def test_should_throw_exception_is_TranscriptsOK_is_not_set(self):
        app = self.createApplication()

        self.login('front_line_advisor')
        app.setWithdrawalRefund(True)
        app.setApplicationFeeOK(True)
        app.setUWSystemStatementOK(True)
        app.setUWOshkoshStatementOK(True)
        try:
            self.portal_workflow.doActionFor(app, 'sendForDirectorReview')
            self.assertEquals(True, False)
        except:
            pass
            
    def test_should_throw_exception_is_UWOshkoshStatementOK_is_not_set(self):
        app = self.createApplication()

        self.login('front_line_advisor')
        app.setWithdrawalRefund(True)
        app.setApplicationFeeOK(True)
        app.setUWSystemStatementOK(True)
        app.setTranscriptsOK(True)
        
        try:
            self.portal_workflow.doActionFor( app, 'sendForDirectorReview')
            self.assertEquals(True, False)
        except:
            pass
                    
    def test_should_throw_exception_is_UWSystemStatementOK_is_not_set(self):
        app = self.createApplication()

        self.login('front_line_advisor')
        app.setWithdrawalRefund(True)
        app.setApplicationFeeOK(True)
        app.setUWOshkoshStatementOK(True)
        app.setTranscriptsOK(True)
        
        try:
            self.portal_workflow.doActionFor(app, 'sendForDirectorReview')
            self.assertEquals(True, False)
        except:
            pass
        
    def test_should_throw_exception_is_WithdrawalRefund_is_not_set(self):
        app = self.createApplication()
        
        self.login('front_line_advisor')
        app.setApplicationFeeOK(True)
        app.setUWSystemStatementOK(True)
        app.setUWOshkoshStatementOK(True)
        app.setTranscriptsOK(True)
        
        try:
            self.portal_workflow.doActionFor(app, 'sendForDirectorReview')
            self.assertEquals(True, False)
        except:
            pass
    
    def test_should_throw_exception_is_ApplicationFeeOK_is_not_set(self):
        app = self.createApplication()

        self.login('front_line_advisor')
        app.setWithdrawalRefund(True)
        app.setUWSystemStatementOK(True)
        app.setUWOshkoshStatementOK(True)
        app.setTranscriptsOK(True)
        
        try:
            self.portal_workflow.doActionFor( app, 'sendForDirectorReview')
            self.assertEquals(True, False)
        except:
            pass
        
    def test_no_other_roles_should_be_able_to_do_action(self):
        app = self.createApplication()
        self.login('front_line_advisor')
        app.setWithdrawalRefund(True)
        app.setApplicationFeeOK(True)
        app.setUWSystemStatementOK(True)
        app.setUWOshkoshStatementOK(True)
        app.setTranscriptsOK(True)
        self.logout()
        
        for user in self._all_users:
            if user != 'front_line_advisor':
                self.login(user)
                self.assertRaises(WorkflowException, self.portal_workflow.doActionFor, app, 'sendForDirectorReview')
                self.logout()
        
    def test_should_send_email(self):
        app = self.createApplication()
        app.setWithdrawalRefund(True)
        app.setApplicationFeeOK(True)
        app.setUWSystemStatementOK(True)
        app.setUWOshkoshStatementOK(True)
        app.setTranscriptsOK(True)
        self.portal.MailHost.clearEmails()
        
        self.login('front_line_advisor')
        self.portal_workflow.doActionFor(app, 'sendForDirectorReview')
        self.assertEquals(1, self.portal.MailHost.getEmailCount())

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestTransitionSendForDirectorReview))

    return suite
    
if  __name__ == '__main__':
    framework()
