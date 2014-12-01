import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Products.UWOshOIE.tests.uwoshoietestcase import UWOshOIETestCase

class TestWorkflowsInstalled(UWOshOIETestCase):
    """Test all workflows"""
    
    def afterSetUp(self):
        self.workflow = self.portal.portal_workflow['OIEStudentApplicationWorkflow']
    
    def test_added_permissions(self):
        permissions = [ 'list', 
                        'Modify portal content', 
                        'View', 
                        'Access contents information', 
                        'UWOshOIE: Review OIE Application', 
                        'UWOshOIE: Modify revisable fields', 
                        'UWOshOIE: Modify Financial Aid fields', 
                        'UWOshOIE: Modify Office Use Only fields', 
                        'UWOshOIE: Modify normal fields'
                      ]
        for permission in permissions:
            self.failUnless(permission in self.workflow.permissions)
        
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestWorkflowsInstalled))

    return suite

if  __name__ == '__main__':
    framework()
