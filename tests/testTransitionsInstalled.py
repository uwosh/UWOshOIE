import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Products.UWOshOIE.tests.uwoshoietestcase import UWOshOIETestCase
from Products.CMFCore.WorkflowCore import WorkflowException

class TestTransitionsInstalled(UWOshOIETestCase):
    """Test all workflows"""

    def afterSetUp(self):
        self.transitions = self.portal.portal_workflow['OIEStudentApplicationWorkflow']['transitions']
        
    def test_all_were_added(self):
        self.transitionIds = self.transitions.objectIds()
        
        self.failUnless('addComment' in self.transitionIds)
        self.failUnless('addToWaitlist' in self.transitionIds)
        self.failUnless('admitConditionally' in self.transitionIds)
        self.failUnless('approveForFA' in self.transitionIds)
        self.failUnless('archive' in self.transitionIds)
        self.failUnless('assertReadyForConditionalAdmit' in self.transitionIds)
        self.failUnless('assignSeat' in self.transitionIds)
        self.failUnless('decline' in self.transitionIds)
        self.failUnless('declineFromFacultyReview' in self.transitionIds)
        self.failUnless('facultyApproves' in self.transitionIds)
        self.failUnless('holdForFAIncomplete' in self.transitionIds)
        self.failUnless('manageDeadlines' in self.transitionIds)
        self.failUnless('recheckForFAHold' in self.transitionIds)
        self.failUnless('sendForDirectorReview' in self.transitionIds)
        self.failUnless('sendForFacultyReview' in self.transitionIds)
        self.failUnless('submit' in self.transitionIds)
        self.failUnless('waitForPrintedMaterials' in self.transitionIds)
        self.failUnless('withdraw' in self.transitionIds)
        
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()

    suite.addTest(makeSuite(TestTransitionsInstalled))

    return suite
    
if  __name__ == '__main__':
    framework()
