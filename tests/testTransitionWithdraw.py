import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Products.UWOshOIE.tests.uwoshoietestcase import UWOshOIETestCase
from Products.CMFCore.WorkflowCore import WorkflowException

class TestTransitionWithdraw(UWOshOIETestCase):
    """Ensure product is properly installed"""

    def test_should_be_withdrawn_after_withdraw_action(self):
        self.login(self._default_user)

        self.portal.invokeFactory(type_name="OIEStudentApplication", id="testapplication")

        app = self.portal['testapplication']

        self.portal_workflow.doActionFor(app, 'withdraw')

        self.failUnless("withdrawn", self.getState( app))
        
    def test_should_send_two_emails_on_withdraw_action(self):
        self.login(self._default_user)

        self.portal.invokeFactory(type_name="OIEStudentApplication", id="testapplication")

        app = self.portal['testapplication']

        self.portal_workflow.doActionFor(app, 'withdraw')

        to = self.portal.MailHost.getToIterator()
        f = self.portal.MailHost.getFromIterator()
        subject = self.portal.MailHost.getSubjectIterator()
        message = self.portal.MailHost.getMessageIterator()

        self.failUnless('test@uwosh.edu;oie@uwosh.edu', to.next())
        self.failUnless('Your study abroad application update (UW Oshkosh Office of International Education)', subject.next())
        self.failUnless("""Your UW Oshkosh Office of International Education study abroad application has been updated.\n\nIts state has changed from 'private' to 'incomplete'.\n\nTransition\n\n\n\nYou can view your application here:  http://nohost/plone/testapplication\n\nComment:""", message.next())
        
        self.failUnless(';oie@uwosh.edu', to.next())
        self.failUnless('Your study abroad application update (UW Oshkosh Office of International Education)', subject.next())
        self.failUnless("""Your UW Oshkosh Office of International Education study abroad application has been updated.\n\nTransition\n\n\n\nYou can view your application here:  http://nohost/plone/testapplication\n\nComment:""", message.next())
        
    def test_other_roles_should_not_be_able_to_withdraw(self):
        self.login(self._default_user)

        self.portal.invokeFactory(type_name="OIEStudentApplication", id="testapplication")

        app = self.portal['testapplication']

        self.fill_out_application(app)

        for user,roles in self._oie_users.iteritems():
            self.logout()
            self.login(user)
            try:
                self.portal_workflow.doActionFor(app, 'withdraw')
                self.fail()
            except:
                pass

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestTransitionWithdraw))

    return suite
    
if  __name__ == '__main__':
    framework()
