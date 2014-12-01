import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Products.UWOshOIE.tests.uwoshoietestcase import UWOshOIETestCase
from Products.CMFCore.WorkflowCore import WorkflowException


class TestStateArchived(UWOshOIETestCase):
    """Ensure product is properly installed"""
        
    def createArchivedApplication(self):

        self.login(self._default_user)
        self.portal.invokeFactory(type_name="OIEStudentApplication", id="testapplication")

        app = self.portal['testapplication']

        self.fill_out_application(app)

        self.portal_workflow.doActionFor(app, 'submit')
        self.portal_workflow.doActionFor(app, 'withdraw')

        self.logout()
        self.login('director')
        self.portal_workflow.doActionFor(app, 'archive')
        self.logout()

        return app
        
    def test_application_should_be_in_archive_state(self):
        app = self.createArchivedApplication()
        
        self.assertEquals("archived", self.getState(app))

    def test_should_be_able_to_add_comment(self):
        app = self.createArchivedApplication()
        
        self.login(self._default_user)
        
        self.portal_workflow.doActionFor(app, 'addComment')
        
        self.assertEquals("archived", self.getState(app))
        
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestStateArchived))

    return suite
    
if  __name__ == '__main__':
    framework()
