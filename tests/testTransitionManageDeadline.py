import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Products.UWOshOIE.tests.uwoshoietestcase import UWOshOIETestCase
from Products.CMFCore.WorkflowCore import WorkflowException

class TestTransitionManageDeadline(UWOshOIETestCase):
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

        self.login('program_manager')
        self.portal_workflow.doActionFor(app, 'assertReadyForConditionalAdmit')
        self.portal_workflow.doActionFor(app, 'admitConditionally')
        self.logout()

        return app
                
    def test_front_line_advisor_should_be_able_to_perform_action(self):
        app = self.createApplication()
        
        self.login('front_line_advisor')
        self.portal_workflow.doActionFor(app, 'manageDeadlines')
        self.assertEquals('deadlineManagement', self.getState(app))
        
    def test_program_manager_should_be_able_to_perform_action(self):
        app = self.createApplication()

        self.login('program_manager')
        self.portal_workflow.doActionFor(app, 'manageDeadlines')
        self.assertEquals('deadlineManagement', self.getState(app))

    def test_director_should_be_able_to_perform_action(self):
        app = self.createApplication()

        self.login('director')
        self.portal_workflow.doActionFor(app, 'manageDeadlines')
        self.assertEquals('deadlineManagement', self.getState(app))

    def test_fac_review_should_not_be_able_to_perform_action(self):
        app = self.createApplication()

        self.login('fac_review')
        self.assertRaises(WorkflowException, self.portal_workflow.doActionFor, app, 'manageDeadlines')

    def test_others_should_not_be_allowed_to_perform(self):
        app = self.createApplication()
        allowed = ['front_line_advisor', 'program_manager', 'director', 'fac_review']
        
        for user in self._all_users:
            if user not in allowed:
                self.login(user)
                self.assertRaises(WorkflowException, self.portal_workflow.doActionFor, app, 'manageDeadlines')
        

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestTransitionManageDeadline))

    return suite
    
if  __name__ == '__main__':
    framework()
