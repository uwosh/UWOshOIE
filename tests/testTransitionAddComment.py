import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Products.UWOshOIE.tests.uwoshoietestcase import UWOshOIETestCase
from Products.CMFCore.WorkflowCore import WorkflowException

class TestTransitionAddComment(UWOshOIETestCase):
    """Ensure product is properly installed"""

    def createApplication(self):
        self.login(self._default_user)

        self.portal.invokeFactory(type_name="OIEStudentApplication", id="testapplication")
        self.logout()

        return self.portal['testapplication']

    def test_should_be_able_to_add_comment_and_remain_in_state(self):
        app = self.createApplication()

        self.login(self._default_user)
        self.portal_workflow.doActionFor(app, 'addComment')
        self.failUnless('private', self.getState( app))

    def test_should_send_email_after_comment_added(self):
        app = self.createApplication()
        self.login(self._default_user)

        self.portal_workflow.doActionFor(app, 'addComment')
        self.assertEquals(1, self.portal.MailHost.getEmailCount())

    def test_should_send_correct_email_message(self):
        app = self.createApplication()
        self.fill_out_application(app)
        self.login(self._default_user)

        self.portal_workflow.doActionFor(app, 'addComment')

        to = self.portal.MailHost.getTo()
        f = self.portal.MailHost.getFrom()
        subject = self.portal.MailHost.getSubject()
        message = self.portal.MailHost.getMessage()

        self.assertEquals(['applicant@uwosh.edu', 'oie@uwosh.edu'], to)
        self.assertEquals('student@oie.com', f)
        self.assertEquals('Your study abroad application update (UW Oshkosh Office of International Education)', subject)
        self.assertEquals("\n\nYour UW Oshkosh Office of International Education study abroad application has been updated.\n\nName: John Doe\nProgram Name: test\nProgram Year: 2009\n\nTransition\n\n\n\nYou can view your application here: http://nohost/plone/testapplication\n\nComment: \n\n\n", message)

    def test_every_role_should_be_able_to_add_comment(self):
        app = self.createApplication()
        
        for user in self._oie_users.keys():
            self.login(user)
            self.portal_workflow.doActionFor(app, 'addComment')
            self.assertEquals('private', self.getState(app))
            self.logout()
            
        self.login(self._default_user)
        self.portal_workflow.doActionFor(app, 'addComment')
        self.assertEquals('private', self.getState(app))

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestTransitionAddComment))

    return suite
    
if  __name__ == '__main__':
    framework()
