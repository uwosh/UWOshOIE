import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Products.UWOshOIE.tests.uwoshoietestcase import UWOshOIETestCase
from Products.CMFCore.WorkflowCore import WorkflowException

class TestStateFacultyReview(UWOshOIETestCase):
    """Ensure product is properly installed"""

    def afterSetUp(self):
        self.acl_users = self.portal.acl_users
        self.portal_workflow = self.portal.portal_workflow
        self.portal_registration = self.portal.portal_registration
        
        self.mockMailHost()
        
        self.createUsers()

    def createFacultyReviewApplication(self):

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
        self.portal_workflow.doActionFor(app, 'sendForFacultyReview')
        self.logout()

        return app
        
    def test_should_be_in_facultyReview_state(self):
        app = self.createFacultyReviewApplication()
        
        self.assertEquals('facultyReview', self.getState(app))
        
    def test_should_be_able_to_addComment(self):
        app = self.createFacultyReviewApplication()

        self.login(self._default_user)
        self.portal_workflow.doActionFor(app, 'addComment')
        self.assertEquals('facultyReview', self.getState(app))
        
    def test_should_be_able_to_facultyApproves(self):
        app = self.createFacultyReviewApplication()
        
        self.login('fac_review')
        self.portal_workflow.doActionFor(app, 'facultyApproves')
        self.assertEquals('facApprovedNeedsProgramManagerReview', self.getState(app))
        
    def test_should_be_able_to_declineFormFacultyReview(self):
        app = self.createFacultyReviewApplication()
        
        self.login('fac_review')
        self.portal_workflow.doActionFor(app, 'declineFromFacultyReview')
        self.assertEquals('declined', self.getState(app))
        
    def test_should_be_able_to_withdraw(self):
        app = self.createFacultyReviewApplication()
        
        self.login(self._default_user)
        self.portal_workflow.doActionFor(app, 'withdraw')
        self.assertEquals('withdrawn', self.getState(app))
        
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestStateFacultyReview))

    return suite
    
if  __name__ == '__main__':
    framework()
