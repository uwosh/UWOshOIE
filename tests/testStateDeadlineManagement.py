import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Products.UWOshOIE.tests.uwoshoietestcase import UWOshOIETestCase
from Products.CMFCore.WorkflowCore import WorkflowException

class TestStateDeadlineManagement(UWOshOIETestCase):
    """Ensure product is properly installed"""

    def afterSetUp(self):
        self.acl_users = self.portal.acl_users
        self.portal_workflow = self.portal.portal_workflow
        self.portal_registration = self.portal.portal_registration
        
        self.mockMailHost()
        
        self.createUsers()
        
    def createDeadlineManagementApplication(self):

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
        self.portal_workflow.doActionFor(app, 'manageDeadlines')
        self.logout()

        return app

    def test_should_be_in_deadlineManagement_state(self):
        app = self.createDeadlineManagementApplication()
        
        self.assertEquals('deadlineManagement', self.getState(app))
        
    def test_should_be_able_to_addComment(self):
        app = self.createDeadlineManagementApplication()
        
        self.login(self._default_user)
        self.portal_workflow.doActionFor(app, 'addComment')
        self.assertEquals('deadlineManagement', self.getState(app))
        self.logout()
        
    def test_should_be_able_to_assignSeat(self):
        app = self.createDeadlineManagementApplication()
        
        self.login('front_line_advisor')
        app.setMedicalHealthProblems("None")
        app.setMedicalHealthProblems_takenMedication("NO")
        app.setMedicalHealthProblems_medications("None")
        app.setMedicalHealthProblems_underCare("None")
        app.setMedicalHealthProblems_whatCondition("None")
        app.setMedicalHealthProblems_willingToPrescribe("None")
        app.setMedicalHealthProblems_additionalInfo("None")
        app.setMedicalMentalProblems("No")
        app.setMedicalMentalProblems_takenMedication("None")
        app.setMedicalMentalProblems_medications("None")
        app.setMedicalMentalProblems_currentDose("None")
        app.setMedicalMentalProblems_underCare("None")
        app.setMedicalMentalProblems_enoughMedication("None")
        app.setMedicalMentalProblems_additionalInfo("None")
        app.setMedicalHealthProblems_stable("Yes")
        app.setMedicalMentalProblems_stable("Yes")
        app.setMedicalMentalProblems_condition("None")
        app.setMedicalRegistered("Yes")
        app.setMedicalRegistered_office("None")
        app.setMedicalRegistered_accommodations("None")
        self.portal_workflow.doActionFor(app, 'assignSeat')
        self.assertEquals('seatAssigned', self.getState(app))
        self.logout()
        
    def test_should_be_able_to_decline(self):
        app = self.createDeadlineManagementApplication()
        
        self.login('front_line_advisor')
        self.portal_workflow.doActionFor(app, 'decline')
        self.assertEquals('declined', self.getState(app))
        self.logout()
        
    def test_should_be_able_to_withdraw(self):
        app = self.createDeadlineManagementApplication()
        
        self.login(self._default_user)
        self.portal_workflow.doActionFor(app, 'withdraw')
        self.assertEquals('withdrawn', self.getState(app))
        self.logout()

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestStateDeadlineManagement))

    return suite
    
if  __name__ == '__main__':
    framework()
