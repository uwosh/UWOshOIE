import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Products.UWOshOIE.tests.uwoshoietestcase import UWOshOIETestCase
from Products.CMFCore.WorkflowCore import WorkflowException
from Products.UWOshOIE.Extensions.WorkflowScriptHelpers import *
import transaction

class TestUWOshOIEStudentApplication(UWOshOIETestCase):
    """Ensure product is properly installed"""

    def createApp(self):
        self.login(self._default_user)

        self.portal.invokeFactory(type_name="OIEStudentApplication", id="testapplication")

        app = self.portal['testapplication']

        self.fill_out_application(app)
        transaction.commit()

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestUWOshOIEStudentApplication))

    return suite
    
if  __name__ == '__main__':
    framework()
