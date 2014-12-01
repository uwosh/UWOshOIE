import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Products.UWOshOIE.tests.uwoshoietestcase import UWOshOIETestCase
from Products.CMFCore.WorkflowCore import WorkflowException

class TestStateWaitlist(UWOshOIETestCase):
    """Ensure product is properly installed"""

    def createWaitlistApplication(self):

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
        self.portal_workflow.doActionFor(app, 'addToWaitlist')
        self.logout()

        return app

    def test_should_be_in_correct_state(self):
        app = self.createWaitlistApplication()
        
        self.assertEquals('waitlist', self.getState(app))

    def test_should_be_able_to_addComment(self):
        app = self.createWaitlistApplication()
        
        self.login('director')
        self.portal_workflow.doActionFor(app, 'addComment')
        self.assertEquals('waitlist', self.getState(app))
        
    def test_should_be_able_to_assertReadyForConditionalAdmit(self):
        app = self.createWaitlistApplication()
        
        self.login('program_manager')
        self.portal_workflow.doActionFor(app, 'assertReadyForConditionalAdmit')
        self.assertEquals('readyForConditionalAdmit', self.getState(app))
        
    def test_should_be_able_to_decline(self):
        app = self.createWaitlistApplication()
        
        self.login('front_line_advisor')
        self.portal_workflow.doActionFor(app, 'decline')
        self.assertEquals('declined', self.getState(app))
        
    def test_should_be_able_to_withdraw(self):
        app = self.createWaitlistApplication()
        
        self.login(self._default_user)
        self.portal_workflow.doActionFor(app, 'withdraw')
        self.assertEquals('withdrawn', self.getState(app))

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestStateWaitlist))

    return suite
    
if  __name__ == '__main__':
    framework()
