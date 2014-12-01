import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Products.UWOshOIE.tests.uwoshoietestcase import UWOshOIETestCase
from Products.CMFCore.WorkflowCore import WorkflowException

class TestTransitionWaitForPrintedMaterials(UWOshOIETestCase):
    """Ensure product is properly installed"""


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestTransitionWaitForPrintedMaterials))

    return suite
    
if  __name__ == '__main__':
    framework()
