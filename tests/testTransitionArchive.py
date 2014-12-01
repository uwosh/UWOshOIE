import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Products.UWOshOIE.tests.uwoshoietestcase import UWOshOIETestCase
from Products.CMFCore.WorkflowCore import WorkflowException

class TestTransitionArchive(UWOshOIETestCase):
    """Ensure product is properly installed"""



    def createApplication(self):

        self.login(self._default_user)
        self.portal.invokeFactory(type_name="OIEStudentApplication", id="testapplication")

        app = self.portal['testapplication']

        self.fill_out_application(app)

        self.portal_workflow.doActionFor(app, 'submit')
        self.portal_workflow.doActionFor(app, 'withdraw')

        self.logout()

        return app

    def test_owner_should_not_be_able_to_archive(self):
        app = self.createApplication()

        self.login(self._default_user)

        self.assertRaises(WorkflowException, self.portal_workflow.doActionFor, app, 'archive')

    def test_FacultyReviewer_should_not_be_able_to_archive(self):
        app = self.createApplication()

        self.login('fac_review')

        self.assertRaises(WorkflowException, self.portal_workflow.doActionFor, app, 'archive')

    def test_FacultyReviewer_should_not_be_able_to_archive(self):
        app = self.createApplication()

        self.login('financial_aid')

        self.assertRaises(WorkflowException, self.portal_workflow.doActionFor, app, 'archive')

    def test_Director_should_be_able_to_archive(self):
        app = self.createApplication()

        self.login('director')

        self.portal_workflow.doActionFor(app, 'archive')

        self.assertEquals("archived", self.getState(app))

    def test_ProgramManager_should_be_able_to_archive(self):
        app = self.createApplication()

        self.login('program_manager')

        self.portal_workflow.doActionFor(app, 'archive')

        self.assertEquals("archived", self.getState(app))

    def test_ProgramManager_should_be_able_to_archive(self):
        app = self.createApplication()

        self.login('front_line_advisor')

        self.portal_workflow.doActionFor(app, 'archive')

        self.assertEquals("archived", self.getState(app))

    def test_should_send_email_on_archive_action(self):
        app = self.createApplication()

        self.portal.MailHost.clearEmails()
        self.login('director')

        self.portal_workflow.doActionFor(app, 'archive')

        self.assertEquals(1, self.portal.MailHost.getEmailCount())

        to = self.portal.MailHost.getTo()
        f = self.portal.MailHost.getFrom()
        subject = self.portal.MailHost.getSubject()
        message = self.portal.MailHost.getMessage()

        self.assertEquals(['applicant@uwosh.edu', 'oie@uwosh.edu'], to)
        self.assertEquals('director@oie.com', f)
        self.assertEquals('Your study abroad application update (UW Oshkosh Office of International Education)', subject)
        self.assertEquals("\n\nYour UW Oshkosh Office of International Education study abroad application has been updated.\n\nName: John Doe\nProgram Name: test\nProgram Year: 2009\n\nTransition\n\n\n\nYou can view your application here: http://nohost/plone/testapplication\n\nComment: \n\n\n", message)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestTransitionArchive))

    return suite
    
if  __name__ == '__main__':
    framework()
