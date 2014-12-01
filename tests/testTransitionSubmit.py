import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Products.UWOshOIE.tests.uwoshoietestcase import UWOshOIETestCase
from Products.CMFCore.WorkflowCore import WorkflowException

class TestTransitionSubmit(UWOshOIETestCase):
    """Ensure product is properly installed"""

    def createApp(self):
        self.login(self._default_user)

        self.portal.invokeFactory(type_name="OIEStudentApplication", id="testapplication")

        app = self.portal['testapplication']

        self.fill_out_application(app)
        return app

    def test_should_fail_when_trying_to_submit_and_not_filled_out(self):
        self.login(self._default_user)

        self.portal.invokeFactory(type_name="OIEStudentApplication", id="testapplication")
        #should fail since it is not filled out yet.
        try:
            self.portal_workflow.doActionFor(self.portal['testapplication'], "submit")
            self.fail()
        except:
            pass

    def test_should_be_able_submit_if_all_applicable_fields_are_completed(self):
        self.login(self._default_user)

        self.portal.invokeFactory(type_name="OIEStudentApplication", id="testapplication")

        app = self.portal['testapplication']

        self.fill_out_application(app)

        self.portal_workflow.doActionFor(app, 'submit')
    
    def test_should_change_state_to_incomplete_on_submit(self):
        self.login(self._default_user)

        self.portal.invokeFactory(type_name="OIEStudentApplication", id="testapplication")

        app = self.portal['testapplication']

        self.fill_out_application(app)

        self.portal_workflow.doActionFor(app, 'submit')

        self.failUnless("incomplete", self.getState( app))
        
    def test_if_applyForFA_is_YES_then_applicant_is_required_to_fill_in_HOLD_or_PROCESS(self):
        app = self.createApp()
        self.login(self._default_user)
        
        self.fill_out_application(app)
        app.setApplyForAid("Yes")

        self.assertRaises(ValueError, self.portal_workflow.doActionFor, app, 'submit')
        
    def test_should_submit_when_applyForAid_is_set_and_applicant_fills_required(self):
        app = self.createApp()
        self.login(self._default_user)
                
        self.fill_out_application(app)
        app.setApplyForAid("Yes")
        app.setHoldApplication("PROCESS")
        
        self.portal_workflow.doActionFor(app, 'submit')
        
        self.assertEquals('incomplete', self.getState(app))
        
    def test_should_send_correct_email_on_submit(self):
        self.login(self._default_user)

        self.portal.invokeFactory(type_name="OIEStudentApplication", id="testapplication")

        app = self.portal['testapplication']

        self.fill_out_application(app)

        self.portal_workflow.doActionFor(app, 'submit')

        self.assertEquals(['applicant@uwosh.edu', 'oie@uwosh.edu'], self.portal.MailHost.getTo())
        self.assertEquals("student@oie.com", self.portal.MailHost.getFrom())
        self.assertEquals("""\n\nYour UW Oshkosh Office of International Education study abroad application has been updated.\n\nName: John Doe\nProgram Name: test\nProgram Year: 2009\n\nTransition\n\n\n\nYou can view your application here: http://nohost/plone/testapplication\n\nComment: \n\n\n""", self.portal.MailHost.getMessage())
        self.assertEquals("Your study abroad application update (UW Oshkosh Office of International Education)", self.portal.MailHost.getSubject())

        self.assertEquals(1, self.portal.MailHost.getEmailCount())


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestTransitionSubmit))

    return suite
    
if  __name__ == '__main__':
    framework()
