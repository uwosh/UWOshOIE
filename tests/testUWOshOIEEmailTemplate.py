import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Products.UWOshOIE.tests.uwoshoietestcase import UWOshOIETestCase
from Products.CMFCore.WorkflowCore import WorkflowException
from Products.UWOshOIE.Extensions.WorkflowScriptHelpers import *
from Products.UWOshOIE.Extensions.Settings.EmailTemplates import *
from Products.UWOshOIE.Extensions.Settings import Helpers


class TestUWOshOIEEmailTemplate(UWOshOIETestCase):
    """Ensure product is properly installed"""
        
    pass

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestUWOshOIEEmailTemplate))

    return suite
    
if  __name__ == '__main__':
    framework()
