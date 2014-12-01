import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Products.UWOshOIE.tests.uwoshoietestcase import UWOshOIETestCase
from Products.CMFCore.WorkflowCore import WorkflowException

class TestTransitionDeclineFromFacultyReview(UWOshOIETestCase):
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
        self.portal_workflow.doActionFor(app, 'sendForFacultyReview')
        self.logout()

        return app
        
    def test_faculty_review_should_should_be_able_to_perform_action(self):
        app = self.createApplication()
        
        self.login('fac_review')
        self.portal_workflow.doActionFor(app, 'declineFromFacultyReview')
        self.assertEquals('declined', self.getState(app))
        
    def test_front_line_advisor_should_should_be_able_to_perform_action(self):
        app = self.createApplication()

        self.login('front_line_advisor')
        self.portal_workflow.doActionFor(app, 'declineFromFacultyReview')
        self.assertEquals('declined', self.getState(app))
        
    def test_program_manager_should_should_be_able_to_perform_action(self):
        app = self.createApplication()

        self.login('program_manager')
        self.portal_workflow.doActionFor(app, 'declineFromFacultyReview')
        self.assertEquals('declined', self.getState(app))

    def test_director_should_should_be_able_to_perform_action(self):
        app = self.createApplication()

        self.login('director')
        self.portal_workflow.doActionFor(app, 'declineFromFacultyReview')
        self.assertEquals('declined', self.getState(app))

    def test_other_should_not_be_able_to_declineFromFacultyReview(self):
        app = self.createApplication()
        accepted_roles = ['fac_review', 'front_line_advisor', 'program_manager']
        
        for user in self._all_users:
            if user not in accepted_roles:
                self.assertRaises(WorkflowException, self.portal_workflow.doActionFor, app, 'declineFromFacultyReview')
                
    def test_should_send_correct_email_from_program_manager(self):
        app = self.createApplication()
        self.portal.MailHost.clearEmails()

        self.login('program_manager')

        self.portal_workflow.doActionFor(app, 'declineFromFacultyReview')

        to = self.portal.MailHost.getTo()
        f = self.portal.MailHost.getFrom()
        subject = self.portal.MailHost.getSubject()
        message = self.portal.MailHost.getMessage()

        self.assertEquals(['applicant@uwosh.edu', 'oie@uwosh.edu'], to)
        self.assertEquals('program_manager@oie.com', f)
        self.assertEquals('Your study abroad application update (UW Oshkosh Office of International Education)', subject)
        self.assertEquals("\n\nYour UW Oshkosh Office of International Education study abroad application has been updated.\n\nName: John Doe\nProgram Name: test\nProgram Year: 2009\n\nTransition\n\n\n\nYou can view your application here: http://nohost/plone/testapplication\n\nComment: \n\n\n", message)

    def test_should_send_correct_email_from_front_line_advisor(self):
        app = self.createApplication()
        self.portal.MailHost.clearEmails()

        self.login('front_line_advisor')

        self.portal_workflow.doActionFor(app, 'declineFromFacultyReview')

        to = self.portal.MailHost.getTo()
        f = self.portal.MailHost.getFrom()
        subject = self.portal.MailHost.getSubject()
        message = self.portal.MailHost.getMessage()

        self.assertEquals(['applicant@uwosh.edu', 'oie@uwosh.edu'], to)
        self.assertEquals('front_line_advisor@oie.com', f)
        self.assertEquals('Your study abroad application update (UW Oshkosh Office of International Education)', subject)
        self.assertEquals("\n\nYour UW Oshkosh Office of International Education study abroad application has been updated.\n\nName: John Doe\nProgram Name: test\nProgram Year: 2009\n\nTransition\n\n\n\nYou can view your application here: http://nohost/plone/testapplication\n\nComment: \n\n\n", message)


    def test_should_send_correct_email_from_director(self):
        app = self.createApplication()
        self.portal.MailHost.clearEmails()

        self.login('director')

        self.portal_workflow.doActionFor(app, 'declineFromFacultyReview')

        to = self.portal.MailHost.getTo()
        f = self.portal.MailHost.getFrom()
        subject = self.portal.MailHost.getSubject()
        message = self.portal.MailHost.getMessage()

        self.assertEquals(['applicant@uwosh.edu', 'oie@uwosh.edu'], to)
        self.assertEquals('director@oie.com', f)
        self.assertEquals('Your study abroad application update (UW Oshkosh Office of International Education)', subject)
        self.assertEquals("\n\nYour UW Oshkosh Office of International Education study abroad application has been updated.\n\nName: John Doe\nProgram Name: test\nProgram Year: 2009\n\nTransition\n\n\n\nYou can view your application here: http://nohost/plone/testapplication\n\nComment: \n\n\n", message)


    def test_should_send_correct_email_from_fac_review(self):
        app = self.createApplication()
        self.portal.MailHost.clearEmails()

        self.login('fac_review')

        self.portal_workflow.doActionFor(app, 'declineFromFacultyReview')

        to = self.portal.MailHost.getTo()
        f = self.portal.MailHost.getFrom()
        subject = self.portal.MailHost.getSubject()
        message = self.portal.MailHost.getMessage()

        self.assertEquals(['applicant@uwosh.edu', 'oie@uwosh.edu'], to)
        self.assertEquals('fac_review@oie.com', f)
        self.assertEquals('Your study abroad application update (UW Oshkosh Office of International Education)', subject)
        self.assertEquals("\n\nYour UW Oshkosh Office of International Education study abroad application has been updated.\n\nName: John Doe\nProgram Name: test\nProgram Year: 2009\n\nTransition\n\n\n\nYou can view your application here: http://nohost/plone/testapplication\n\nComment: \n\n\n", message)

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestTransitionDeclineFromFacultyReview))

    return suite
    
if  __name__ == '__main__':
    framework()
