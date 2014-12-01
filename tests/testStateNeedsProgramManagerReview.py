import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Products.UWOshOIE.tests.uwoshoietestcase import UWOshOIETestCase
from Products.CMFCore.WorkflowCore import WorkflowException

class TestStateNeedsProgramManagerReview(UWOshOIETestCase):
    """Ensure product is properly installed"""

    def afterSetUp(self):
        self.acl_users = self.portal.acl_users
        self.portal_workflow = self.portal.portal_workflow
        self.portal_registration = self.portal.portal_registration
        
        self.mockMailHost()
        
        self.createUsers()

    def createProgramManagerReviewApplication(self):

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

    def test_should_be_in_needsProgramManagerReview_state(self):
        app = self.createProgramManagerReviewApplication()
        
        self.assertEquals('needsProgramManagerReview', self.getState(app))

    def test_should_be_able_to_add_comment(self):
        app = self.createProgramManagerReviewApplication()
        
        self.login(self._default_user)
        self.portal_workflow.doActionFor(app, 'addComment')
        self.assertEquals('needsProgramManagerReview', self.getState(app))

    def test_should_be_able_to_addToWaitlist(self):
        app = self.createProgramManagerReviewApplication()
        
        self.login('program_manager')
        self.portal_workflow.doActionFor(app, 'addToWaitlist')
        self.assertEquals('waitlist', self.getState(app))
        
    def test_should_be_able_to_assertReaedyForConditionalAdmit(self):
        app = self.createProgramManagerReviewApplication()
        
        self.login('program_manager')
        self.portal_workflow.doActionFor(app, 'assertReadyForConditionalAdmit')
        self.assertEquals('readyForConditionalAdmit', self.getState(app))
        
    def test_should_be_able_to_decline(self):
        app = self.createProgramManagerReviewApplication()
        
        self.login('program_manager')
        self.portal_workflow.doActionFor(app, 'decline')
        self.assertEquals('declined', self.getState(app))
        
        
    def test_should_be_able_to_sendForFacultyReview(self):
        app = self.createProgramManagerReviewApplication()
        
        self.login('program_manager')
        self.portal_workflow.doActionFor(app, 'sendForFacultyReview')
        self.assertEquals('facultyReview', self.getState(app))
        
    def test_should_be_able_to_withdraw(self):
        app = self.createProgramManagerReviewApplication()
        
        self.login(self._default_user)
        self.portal_workflow.doActionFor(app, 'withdraw')
        self.assertEquals('withdrawn', self.getState(app))
        

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestStateNeedsProgramManagerReview))

    return suite
    
if  __name__ == '__main__':
    framework()
