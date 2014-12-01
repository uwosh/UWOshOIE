import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Products.UWOshOIE.tests.uwoshoietestcase import UWOshOIETestCase
from Products.CMFCore.WorkflowCore import WorkflowException

class TestTransitionApproveForFA(UWOshOIETestCase):
    """Ensure product is properly installed"""

    def createApplication(self):
        
        self.login(self._default_user)
        self.portal.invokeFactory(type_name="OIEStudentApplication", id="testapplication")
    
        app = self.portal['testapplication']
        
        self.fill_out_application(app)
        app.setHoldApplication('HOLD')
        self.portal_workflow.doActionFor(app, 'submit')
    
        return app

    def test_program_manager_should_be_able_to_do_action(self):
        app = self.createApplication()
        
        self.login('program_manager')
        self.portal_workflow.doActionFor(app, 'approveForFA')
        self.assertEquals('waitingForPrintMaterials', self.getState(app))
    
    def test_front_line_advisor_should_be_able_to_do_action(self):
        app = self.createApplication()

        self.login('front_line_advisor')
        self.portal_workflow.doActionFor(app, 'approveForFA')
        self.assertEquals('waitingForPrintMaterials', self.getState(app))    
    
    def test_all_other_roles_should_not_be_able_able_to_perform_action(self):
        app = self.createApplication
        
        for user in self._all_users:
            if user != 'program_maanger' and user != 'front_line_advisor':
                self.login(user)
                self.assertRaises(WorkflowException, self.portal_workflow.doActionFor, app, 'approveForFA')
                self.logout()
      
    def test_should_send_email_when_fired(self):
        app = self.createApplication()
        self.portal.MailHost.clearEmails()

        self.login('program_manager')
        self.portal_workflow.doActionFor(app, 'approveForFA')
        self.assertEquals(1, self.portal.MailHost.getEmailCount())

    def test_should_send_correct_email_program_maanger(self):
        app = self.createApplication()
        self.portal.MailHost.clearEmails()

        self.login('program_manager')
        self.portal_workflow.doActionFor(app, 'approveForFA')

        to = self.portal.MailHost.getTo()
        f = self.portal.MailHost.getFrom()
        subject = self.portal.MailHost.getSubject()
        message = self.portal.MailHost.getMessage()

        self.assertEquals(['applicant@uwosh.edu', 'oie@uwosh.edu'], to)
        self.assertEquals('program_manager@oie.com', f)
        self.assertEquals('Your study abroad application update (UW Oshkosh Office of International Education)', subject)
        self.assertEquals("\n\nYour UW Oshkosh Office of International Education study abroad application has been updated.\n\nName: John Doe\nProgram Name: test\nProgram Year: 2009\n\nTransition\n\n\n\nYou can view your application here: http://nohost/plone/testapplication\n\nComment: \n\n\n", message)


    def test_should_send_correct_email_front_line_advisor(self):
        app = self.createApplication()
        self.portal.MailHost.clearEmails()

        self.login('front_line_advisor')
        self.portal_workflow.doActionFor(app, 'approveForFA')

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
    suite.addTest(makeSuite(TestTransitionApproveForFA))

    return suite
    
if  __name__ == '__main__':
    framework()
