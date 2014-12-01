import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Products.UWOshOIE.tests.uwoshoietestcase import UWOshOIETestCase
from Products.CMFCore.WorkflowCore import WorkflowException
from Products.UWOshOIE.Extensions.WorkflowScriptHelpers import *

class TestUWOshOIEProgram(UWOshOIETestCase):
    """Ensure product is properly installed"""

    def create_program(self):
        self.login()
        self.setRoles(('Manager', 'Owner'))
    
        programId = self.portal.invokeFactory(  type_name='UWOshOIEProgram', 
                                                        id=self.portal.generateUniqueId(), 
                                                        title="test", 
                                                        facultyLeaders=['front_line_advisor', 'program_manager'])
    

        self.logout()
        
        return self.portal[programId]
        

    def test_getFacultyAddresses(self):
        
        program = self.create_program()
        
        self.assertEquals(program.getFacultyAddresses(), ['front_line_advisor@oie.com', 'program_manager@oie.com'])
        

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestUWOshOIEProgram))

    return suite
    
if  __name__ == '__main__':
    framework()
