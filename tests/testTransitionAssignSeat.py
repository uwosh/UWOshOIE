import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Products.UWOshOIE.tests.uwoshoietestcase import UWOshOIETestCase
from Products.CMFCore.WorkflowCore import WorkflowException
from Products.UWOshOIE.Extensions.Exceptions import *

class TestTransitionAssignSeat(UWOshOIETestCase):
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
        self.portal_workflow.doActionFor(app, 'manageDeadlines')
        self.logout()
        
        self.login('front_line_advisor')
        
        self.logout()
        
        return app
        
    def fillMedical(self, app):
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
        app.setProgramSpecificMaterialsOK(True)
        app.setProgramSpecificMaterialsRequired(True)

    def test_program_manager_should_not_be_able_to_do_action(self):
        app = self.createApplication()
        
        self.login('fac_review')
        self.fillMedical(app)
        self.assertRaises(WorkflowException, self.portal_workflow.doActionFor, app, 'assignSeat')
        
    def test_all_other_roles_should_not_be_able_able_to_perform_action(self):
        app = self.createApplication
        
        for user in self._all_users:
            if user != 'front_line_advisor':
                self.login(user)
                self.assertRaises(WorkflowException, self.portal_workflow.doActionFor, app, 'assignSeat')
                self.logout()
      
    def test_should_send_email_when_fired(self):
        app = self.createApplication()
        self.portal.MailHost.clearEmails()

        self.login('front_line_advisor')
        self.fillMedical(app)
        self.portal_workflow.doActionFor(app, 'assignSeat')
        self.assertEquals(1, self.portal.MailHost.getEmailCount())

    def test_should_send_correct_email_to_front_line_advisor(self):
           app = self.createApplication()
           self.portal.MailHost.clearEmails()

           self.login('front_line_advisor')
           self.fillMedical(app)
           self.portal_workflow.doActionFor(app, 'assignSeat')

           to = self.portal.MailHost.getTo()
           f = self.portal.MailHost.getFrom()
           subject = self.portal.MailHost.getSubject()
           message = self.portal.MailHost.getMessage()

           self.assertEquals(['applicant@uwosh.edu', 'oie@uwosh.edu'], to)
           self.assertEquals('front_line_advisor@oie.com', f)
           self.assertEquals('Your study abroad application update (UW Oshkosh Office of International Education)', subject)
           self.assertEquals("\n\nYour UW Oshkosh Office of International Education study abroad application has been updated.\n\nName: John Doe\nProgram Name: test\nProgram Year: 2009\n\nTransition\n\n\n\nYou can view your application here: http://nohost/plone/testapplication\n\nComment: \n\n\n", message)

    
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestTransitionAssignSeat))

    return suite
    
if  __name__ == '__main__':
    framework()
