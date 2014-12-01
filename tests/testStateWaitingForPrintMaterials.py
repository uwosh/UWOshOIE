import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Products.UWOshOIE.tests.uwoshoietestcase import UWOshOIETestCase
from Products.CMFCore.WorkflowCore import WorkflowException

class TestStateWaitingForPrintMaterials(UWOshOIETestCase):
    """Ensure product is properly installed"""

    def createWaitingForPrintMaterialsApplication(self):

        self.login(self._default_user)
        self.portal.invokeFactory(type_name="OIEStudentApplication", id="testapplication")

        app = self.portal['testapplication']

        self.fill_out_application(app)

        self.portal_workflow.doActionFor(app, 'submit')

        self.logout()
        self.login('front_line_advisor')
        self.portal_workflow.doActionFor(app, 'waitForPrintedMaterials')
        
        return app

    def test_should_be_in_correct_state(self):
        app = self.createWaitingForPrintMaterialsApplication()
        
        self.assertEquals('waitingForPrintMaterials', self.getState(app))

    def test_should_be_able_to_sendForDirectorReview(self):
        app = self.createWaitingForPrintMaterialsApplication()
        self.login('front_line_advisor')
        app.setWithdrawalRefund(True)
        app.setApplicationFeeOK(True)
        app.setUWSystemStatementOK(True)
        app.setUWOshkoshStatementOK(True)
        app.setTranscriptsOK(True)       

        self.portal_workflow.doActionFor(app, 'sendForDirectorReview')
        self.assertEquals('needsDirectorReview', self.getState(app))

    def test_should_be_able_to_add_comment(self):
        app = self.createWaitingForPrintMaterialsApplication()
        
        self.login('director')
        self.portal_workflow.doActionFor(app, 'addComment')
        self.assertEquals('waitingForPrintMaterials', self.getState(app))

    def test_should_be_able_to_decline(self):
        app = self.createWaitingForPrintMaterialsApplication()
        
        self.login('front_line_advisor')
        self.portal_workflow.doActionFor(app, 'decline')
        self.assertEquals('declined', self.getState(app))
        
    def test_should_be_able_to_withdraw(self):
        app = self.createWaitingForPrintMaterialsApplication()
        
        self.login(self._default_user)
        self.portal_workflow.doActionFor(app, 'withdraw')
        self.assertEquals('withdrawn', self.getState(app))

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestStateWaitingForPrintMaterials))

    return suite
    
if  __name__ == '__main__':
    framework()
