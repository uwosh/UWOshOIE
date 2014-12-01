import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Products.UWOshOIE.tests.uwoshoietestcase import UWOshOIETestCase
from Products.CMFCore.WorkflowCore import WorkflowException
from Products.UWOshOIE.Extensions.WorkflowScriptHelpers import *

class TestWorkflowHelpers(UWOshOIETestCase):
    """Ensure product is properly installed"""

    def test_getEmailMessageTemplate_should_return_the_correct_template(self):
        
        template = getEmailMessageTemplate(self.portal, 'archive', False)

        self.assertEquals(template.getCcUsers(), ['oie@uwosh.edu'])
        self.assertEquals(template.getEmailText(), 'Transition')
        self.assertEquals(template.getTransition(), 'archive')
        self.assertEquals(template.getSendEmailOnFailure(), False)
        
        template = getEmailMessageTemplate(self.portal, 'manageDeadlines', True)

        self.assertEquals(template.getCcUsers(), ['oie@uwosh.edu'])
        self.assertEquals(template.getEmailText(), 'Transition')
        self.assertEquals(template.getTransition(), 'manageDeadlines')
        self.assertEquals(template.getSendEmailOnFailure(), True)
        
    def test_intializeMissingValues_should_do_as_told(self):
        missingValues = {}
        
        intializeMissingValues(missingValues, 'test')
        
        self.assertEquals(missingValues['test'], [])
        
    def test_getCreatorInfo(self):
        self.login(self._default_user)
        self.portal.invokeFactory(type_name="OIEStudentApplication", id="testapplication0")
        app = self.portal['testapplication0']
        self.fill_out_application(app)
        self.logout()
        
        creatorInfo = getCreatorInfo(self.portal, app)
        
        self.assertEquals(creatorInfo['email'], 'student@oie.com')
        self.assertEquals(creatorInfo['id'], 'student')
        
    def test_getReviewerInfo(self):
        self.login(self._default_user)
        self.portal.invokeFactory(type_name="OIEStudentApplication", id="testapplication1")
        app = self.portal['testapplication1']
        self.fill_out_application(app)
        self.portal_workflow.doActionFor(app, 'submit')
        self.logout()
        self.login('front_line_advisor')
        self.portal_workflow.doActionFor(app, 'waitForPrintedMaterials')
        self.logout()
        
        reviewerInfo = getReviewerInfo(self.portal, app)
        
        self.assertEquals(reviewerInfo['email'], 'front_line_advisor@oie.com')
        self.assertEquals(reviewerInfo['id'], 'front_line_advisor')
        

    def test_getToAddresses(self):
        self.login(self._default_user)
        self.portal.invokeFactory(type_name="OIEStudentApplication", id="testapplication2")
        app = self.portal['testapplication2']
        self.fill_out_application(app)
        self.portal_workflow.doActionFor(app, 'submit')
        self.logout()
        
        template = getEmailMessageTemplate(self.portal, 'waitForPrintedMaterials', False)
        
        toAddresses = getToAddresses(app, template)
        
        self.assertEquals(toAddresses, ['applicant@uwosh.edu', 'oie@uwosh.edu'])
        
        toAddresses = getToAddresses(app, template, 'guy@uwosh.edu;another@uwosh.edu;')
        
        self.assertEquals(toAddresses, 'applicant@uwosh.edu;oie@uwosh.edu;guy@uwosh.edu;another@uwosh.edu;')
        
        

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestWorkflowHelpers))

    return suite
    
if  __name__ == '__main__':
    framework()
