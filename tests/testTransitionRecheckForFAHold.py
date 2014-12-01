import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Products.UWOshOIE.tests.uwoshoietestcase import UWOshOIETestCase
from Products.CMFCore.WorkflowCore import WorkflowException

class TestTransitionRecheckForFAHold(UWOshOIETestCase):
    """Ensure product is properly installed"""

    def createApplication(self):
        
        self.login(self._default_user)
        self.portal.invokeFactory(type_name="OIEStudentApplication", id="testapplication")
    
        app = self.portal['testapplication']    
        self.fill_out_application(app)
        self.portal_workflow.doActionFor(app, 'submit')
        return app
        
    def test_should_be_fired_when_hold_is_set_on_submit(self):
        app = self.createApplication()
        
        self.login('front_line_advisor')
        app.setHoldApplication('HOLD')
        self.portal_workflow.doActionFor(app, 'recheckForFAHold')
        self.assertEquals('FAHeldIncomplete', self.getState(app))
        
    def test_should_send_email(self):
        app = self.createApplication()
        self.portal.MailHost.clearEmails()
        self.login('front_line_advisor')
        app.setHoldApplication('HOLD')
        self.portal_workflow.doActionFor(app, 'recheckForFAHold')
        self.assertEquals(2, self.portal.MailHost.getEmailCount())

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestTransitionRecheckForFAHold))

    return suite
    
if  __name__ == '__main__':
    framework()
