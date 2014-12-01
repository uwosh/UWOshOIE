import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Products.UWOshOIE.tests.uwoshoietestcase import UWOshOIETestCase
from Products.CMFCore.WorkflowCore import WorkflowException

class TestStatesInstalled(UWOshOIETestCase):
    """Test all workflows"""
    
    def afterSetUp(self):
        self.states = self.portal.portal_workflow['OIEStudentApplicationWorkflow']['states']
    
    def test_FAHeldIncomplete(self):
        self.failUnless('FAHeldIncomplete' in self.states.objectIds())
        state = self.states['FAHeldIncomplete']

        self.hasTheseTransitions(state, ['addComment', 'approveForFA', 'decline', 'withdraw',  ])
    
    def test_FAHeldIncomplete_permissions(self):
        state = self.states['FAHeldIncomplete']
        
        self.hasPermissionRoles(state, 'list', ['Owner', 'UWOshOIEDirector', 'UWOshOIEFacReview', 'UWOshOIEFinAid', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        self.hasPermissionRoles(state, 'Modify portal content', ['Owner', 'UWOshOIEDirector', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        self.hasPermissionRoles(state, 'View', ['Owner', 'UWOshOIEDirector', 'UWOshOIEFacReview', 'UWOshOIEFinAid', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        self.hasPermissionRoles(state, 'Access contents information', ['Owner', 'UWOshOIEDirector', 'UWOshOIEFacReview', 'UWOshOIEFinAid', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        self.hasPermissionRoles(state, 'UWOshOIE: Reivew OIE Application', ['UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        self.hasPermissionRoles(state, 'UWOshOIE: Modify revisable fields', ['Owner', 'UWOshOIEDirector', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        self.hasPermissionRoles(state, 'UWOshOIE: Modify Financial Aid fields', ['UWOshOIEDirector', 'UWOshOIEFinAid', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        self.hasPermissionRoles(state, 'UWOshOIE: Modify Office Use Only fields', ['UWOshOIEDirector', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        self.hasPermissionRoles(state, 'UWOshOIE: Modify normal fields', ['UWOshOIEDirector', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
    
    def test_archived(self):
        self.failUnless('archived' in self.states.objectIds())
        state = self.states['archived']
        
        self.hasTheseTransitions(state, ['addComment'])
        
    def test_archived_permissions(self):
        state = self.states['archived']
    
        self.hasPermissionRoles(state, 'list', ['Owner', 'UWOshOIEDirector', 'UWOshOIEExtReview', 'UWOshOIEFacReview', 'UWOshOIEFinAid', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        self.assertEqual(len(state.getPermissionInfo('Modify portal content')['roles']), 0)
        self.hasPermissionRoles(state, 'View', ['Owner', 'UWOshOIEDirector', 'UWOshOIEExtReview', 'UWOshOIEFacReview', 'UWOshOIEFinAid', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        self.hasPermissionRoles(state, 'Access contents information', ['Owner', 'UWOshOIEDirector', 'UWOshOIEExtReview', 'UWOshOIEFacReview', 'UWOshOIEFinAid', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        self.assertEqual(len(state.getPermissionInfo('UWOshOIE: Review OIE Application')['roles']), 0)
        self.assertEqual(len(state.getPermissionInfo('UWOshOIE: Modify revisable fields')['roles']), 0)
        self.assertEqual(len(state.getPermissionInfo('UWOshOIE: Modify Financial Aid fields')['roles']), 0)
        self.assertEqual(len(state.getPermissionInfo('UWOshOIE: Modify Office Use Only fields')['roles']), 0)
        self.assertEqual(len(state.getPermissionInfo('UWOshOIE: Modify normal fields')['roles']), 0)
    
    def test_conditionallyAdmitted(self):
        self.failUnless('conditionallyAdmitted' in self.states.objectIds())
        state = self.states['conditionallyAdmitted']

        self.hasTheseTransitions(state, ['addComment', 'decline', 'manageDeadlines', 'withdraw'])
        
    def test_conditionallyAdmitted_permissions(self):
        state = self.states['conditionallyAdmitted']
        
        self.hasPermissionRoles(state, 'list', ['Owner', 'UWOshOIEDirector', 'UWOshOIEFacReview', 'UWOshOIEFinAid', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        self.hasPermissionRoles(state, 'Modify portal content', ['Owner', 'UWOshOIEDirector', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        self.hasPermissionRoles(state, 'View', ['Owner', 'UWOshOIEDirector', 'UWOshOIEFacReview', 'UWOshOIEFinAid', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        self.hasPermissionRoles(state, 'Access contents information', ['Owner', 'UWOshOIEDirector', 'UWOshOIEFacReview', 'UWOshOIEFinAid', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        self.hasPermissionRoles(state, 'UWOshOIE: Review OIE Application', ['UWOshOIEDirector', 'UWOshOIEFacReview', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        self.hasPermissionRoles(state, 'UWOshOIE: Modify revisable fields', ['Owner', 'UWOshOIEDirector', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        self.hasPermissionRoles(state, 'UWOshOIE: Modify Financial Aid fields', ['UWOshOIEDirector', 'UWOshOIEFinAid', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        self.hasPermissionRoles(state, 'UWOshOIE: Modify Office Use Only fields', ['UWOshOIEDirector', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        self.hasPermissionRoles(state, 'UWOshOIE: Modify normal fields', ['UWOshOIEDirector', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
               
    def test_deadlineManagement(self):
        self.failUnless('deadlineManagement' in self.states.objectIds())
        state = self.states['deadlineManagement']

        self.hasTheseTransitions(state, ['addComment', 'assignSeat', 'decline', 'withdraw'])
        
    def test_deadlineManagement_permissions(self):
        state = self.states['deadlineManagement']
        
        self.hasPermissionRoles(state, 'list', ['Owner', 'UWOshOIEDirector', 'UWOshOIEFacReview', 'UWOshOIEFinAid', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        self.hasPermissionRoles(state, 'Modify portal content', ['Owner', 'UWOshOIEDirector', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        self.hasPermissionRoles(state, 'View',['Owner', 'UWOshOIEDirector', 'UWOshOIEFacReview', 'UWOshOIEFinAid', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        self.hasPermissionRoles(state, 'Access contents information', ['Owner', 'UWOshOIEDirector', 'UWOshOIEFacReview', 'UWOshOIEFinAid', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        self.hasPermissionRoles(state, 'UWOshOIE: Review OIE Application', ['UWOshOIEFacReview', 'UWOshOIEFrontLineAdvisor'])
        self.hasPermissionRoles(state, 'UWOshOIE: Modify revisable fields', ['Owner', 'UWOshOIEDirector', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        self.hasPermissionRoles(state, 'UWOshOIE: Modify Financial Aid fields', ['UWOshOIEDirector', 'UWOshOIEFinAid', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        self.hasPermissionRoles(state, 'UWOshOIE: Modify Office Use Only fields', ['UWOshOIEDirector', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        self.hasPermissionRoles(state, 'UWOshOIE: Modify normal fields', ['UWOshOIEDirector', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
            
    def test_declined_workflow(self):
        self.failUnless('declined' in self.states.objectIds())
        state = self.states['declined']

        self.hasTheseTransitions(state, ['addComment', 'archive'])
        
    def test_declined_permissions(self):
        state = self.states['declined']
        
        self.hasPermissionRoles(state, 'list', ['Owner', 'UWOshOIEDirector', 'UWOshOIEExtReview', 'UWOshOIEFacReview', 'UWOshOIEFinAid', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        self.assertEquals(len(state.getPermissionInfo('Modify portal content')['roles']), 0)
        self.hasPermissionRoles(state, 'View', ['Owner', 'UWOshOIEDirector', 'UWOshOIEExtReview', 'UWOshOIEFacReview', 'UWOshOIEFinAid', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        self.hasPermissionRoles(state, 'Access contents information', ['Owner', 'UWOshOIEDirector', 'UWOshOIEExtReview', 'UWOshOIEFacReview', 'UWOshOIEFinAid', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        self.assertEquals(len(state.getPermissionInfo('UWOshOIE: Review OIE Application')['roles']), 0)
        self.assertEquals(len(state.getPermissionInfo('UWOshOIE: Modify revisable fields')['roles']), 0)
        self.assertEquals(len(state.getPermissionInfo('UWOshOIE: Modify Financial Aid fields')['roles']), 0)
        self.assertEquals(len(state.getPermissionInfo('UWOshOIE: Modify Office Use Only fields')['roles']), 0)
        self.assertEquals(len(state.getPermissionInfo('UWOshOIE: Modify normal fields')['roles']), 0)
                
    def test_facApprovedNeedsProgramManagerReview_workflow(self):
        self.failUnless('facApprovedNeedsProgramManagerReview' in self.states.objectIds())
        state = self.states['facApprovedNeedsProgramManagerReview']

        self.hasTheseTransitions(state, ['addComment', 'addToWaitlist', 'assertReadyForConditionalAdmit', 'decline', 'withdraw'])
        
    def test_facApprovedNeedsProgramManagerReview_permissions(self):
        state = self.states['facApprovedNeedsProgramManagerReview']
        
        self.hasPermissionRoles(state, 'list', ['Owner', 'UWOshOIEDirector', 'UWOshOIEFacReview', 'UWOshOIEFinAid', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        self.hasPermissionRoles(state, 'Modify portal content', ['Owner', 'UWOshOIEDirector', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        self.hasPermissionRoles(state, 'View', ['Owner', 'UWOshOIEDirector', 'UWOshOIEFacReview', 'UWOshOIEFinAid', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        self.hasPermissionRoles(state, 'Access contents information', ['Owner', 'UWOshOIEDirector', 'UWOshOIEFacReview', 'UWOshOIEFinAid', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        self.hasPermissionRoles(state, 'UWOshOIE: Reivew OIE Application', ['UWOshOIEProgramManager'])
        self.hasPermissionRoles(state, 'UWOshOIE: Modify revisable fields', ['Owner', 'UWOshOIEDirector', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        self.hasPermissionRoles(state, 'UWOshOIE: Modify Financial Aid fields', ['UWOshOIEDirector', 'UWOshOIEFinAid', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        self.hasPermissionRoles(state, 'UWOshOIE: Modify Office Use Only fields', ['UWOshOIEDirector', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        self.hasPermissionRoles(state, 'UWOshOIE: Modify normal fields', ['UWOshOIEDirector', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        
    def test_facultyReview(self):
        self.failUnless('facultyReview' in self.states.objectIds())
        state = self.states['facultyReview']
        
        self.hasTheseTransitions(state, ['addComment', 'declineFromFacultyReview', 'facultyApproves', 'withdraw'])        
        
    def test_facultyReview_permissions(self):
        state = self.states['facultyReview']
    
        self.hasPermissionRoles(state, 'list', ['Owner', 'UWOshOIEDirector', 'UWOshOIEFacReview', 'UWOshOIEFinAid', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        self.hasPermissionRoles(state, 'Modify portal content', ['Owner', 'UWOshOIEDirector', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        self.hasPermissionRoles(state, 'View', ['Owner', 'UWOshOIEDirector', 'UWOshOIEFacReview', 'UWOshOIEFinAid', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        self.hasPermissionRoles(state, 'Access contents information', ['Owner', 'UWOshOIEDirector', 'UWOshOIEFacReview', 'UWOshOIEFinAid', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        self.hasPermissionRoles(state, 'UWOshOIE: Review OIE Application', ['UWOshOIEFacReview'])
        self.hasPermissionRoles(state, 'UWOshOIE: Modify revisable fields', ['Owner', 'UWOshOIEDirector', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        self.hasPermissionRoles(state, 'UWOshOIE: Modify Financial Aid fields', ['UWOshOIEDirector', 'UWOshOIEFinAid', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        self.hasPermissionRoles(state, 'UWOshOIE: Modify Office Use Only fields', ['UWOshOIEDirector', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        self.hasPermissionRoles(state, 'UWOshOIE: Modify normal fields', ['UWOshOIEDirector', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])

    def test_incomplete(self):
        self.failUnless('incomplete' in self.states.objectIds())
        state = self.states['incomplete']
        
        self.hasTheseTransitions(state, [  'addComment', 'decline', 'holdForFAIncomplete', 'recheckForFAHold', 'waitForPrintedMaterials', 'withdraw'])
        
    def test_incomplete_permissions(self):
        state = self.states['incomplete']
        
        self.hasPermissionRoles(state, 'list', ['Owner', 'UWOshOIEDirector', 'UWOshOIEFacReview', 'UWOshOIEFinAid', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        self.hasPermissionRoles(state, 'Modify portal content', ['Owner', 'UWOshOIEDirector', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        self.hasPermissionRoles(state, 'View', ['Owner', 'UWOshOIEDirector', 'UWOshOIEFacReview', 'UWOshOIEFinAid', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        self.hasPermissionRoles(state, 'Access contents information', ['Owner', 'UWOshOIEDirector', 'UWOshOIEFacReview', 'UWOshOIEFinAid', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        self.hasPermissionRoles(state, 'UWOshOIE: Review OIE Application', ['UWOshOIEFrontLineAdvisor'])                   
        self.hasPermissionRoles(state, 'UWOshOIE: Modify revisable fields', ['Owner', 'UWOshOIEDirector', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        self.hasPermissionRoles(state, 'UWOshOIE: Modify Financial Aid fields', ['UWOshOIEDirector', 'UWOshOIEFinAid', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        self.hasPermissionRoles(state, 'UWOshOIE: Modify Office Use Only fields', ['UWOshOIEDirector', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        self.hasPermissionRoles(state, 'UWOshOIE: Modify normal fields', ['UWOshOIEDirector', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        
    def test_needsDirectorReview(self):
        self.failUnless('needsDirectorReview' in self.states.objectIds())
        state = self.states['needsDirectorReview']
        
        self.hasTheseTransitions(state, [  'addComment', 'decline', 'sendForProgramManagerReview', 'withdraw'])
        
    def test_needsDirectorReview_permissions(self):
        state = self.states['needsDirectorReview']
        
        self.hasPermissionRoles(state, 'list', ['Owner', 'UWOshOIEDirector', 'UWOshOIEFacReview', 'UWOshOIEFinAid', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        self.hasPermissionRoles(state, 'Modify portal content', ['Owner', 'UWOshOIEDirector', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        self.hasPermissionRoles(state, 'View', ['Owner', 'UWOshOIEDirector', 'UWOshOIEFacReview', 'UWOshOIEFinAid', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        self.hasPermissionRoles(state, 'Access contents information', ['Owner', 'UWOshOIEDirector', 'UWOshOIEFacReview', 'UWOshOIEFinAid', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        self.hasPermissionRoles(state, 'UWOshOIE: Reivew OIE Application', ['UWOshOIEDirector'])
        self.hasPermissionRoles(state, 'UWOshOIE: Modify revisable fields', ['Owner', 'UWOshOIEDirector', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        self.hasPermissionRoles(state, 'UWOshOIE: Modify Financial Aid fields', ['UWOshOIEDirector', 'UWOshOIEFinAid', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        self.hasPermissionRoles(state, 'UWOshOIE: Modify Office Use Only fields', ['UWOshOIEDirector', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        self.hasPermissionRoles(state, 'UWOshOIE: Modify normal fields', ['UWOshOIEDirector', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
                
    def test_needsProgramManagerReview(self):
        self.failUnless('needsProgramManagerReview' in self.states.objectIds())
        state = self.states['needsProgramManagerReview']
        
        self.hasTheseTransitions(state, [  'addComment', 'addToWaitlist', 'assertReadyForConditionalAdmit', 'decline', 'sendForFacultyReview', 'withdraw'])
    
    def test_needsProgramManagerReview_permissions(self):
        state = self.states['needsProgramManagerReview']
        
        self.hasPermissionRoles(state, 'list', ['Owner', 'UWOshOIEDirector', 'UWOshOIEFacReview', 'UWOshOIEFinAid', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        self.hasPermissionRoles(state, 'Modify portal content', ['Owner', 'UWOshOIEDirector', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        self.hasPermissionRoles(state, 'View', ['Owner', 'UWOshOIEDirector', 'UWOshOIEFacReview', 'UWOshOIEFinAid', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        self.hasPermissionRoles(state, 'Access contents information', ['Owner', 'UWOshOIEDirector', 'UWOshOIEFacReview', 'UWOshOIEFinAid', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        self.hasPermissionRoles(state, 'UWOshOIE: Review OIE Application', ['UWOshOIEProgramManager'])
        self.hasPermissionRoles(state, 'UWOshOIE: Modify revisable fields', ['Owner', 'UWOshOIEDirector', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        self.hasPermissionRoles(state, 'UWOshOIE: Modify Financial Aid fields', ['UWOshOIEDirector', 'UWOshOIEFinAid', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        self.hasPermissionRoles(state, 'UWOshOIE: Modify Office Use Only fields', ['UWOshOIEDirector', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        self.hasPermissionRoles(state, 'UWOshOIE: Modify normal fields', ['UWOshOIEDirector', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
    
    def test_private(self):
        self.failUnless('private' in self.states.objectIds())
        state = self.states['private']
        
        self.hasTheseTransitions(state, [ 'addComment', 'submit', 'withdraw'])
        
    def test_private_permissions(self):
        state = self.states['private']
        
        permissions = ['list', 'Modify portal content', 'Access contents information', 'UWOshOIE: Modify revisable fields', 'UWOshOIE: Modify normal fields']
                        
        for permission in permissions:
            self.failUnless('Owner' in state.getPermissionInfo(permission)['roles'])
            self.assertEquals(len(state.getPermissionInfo(permission)['roles']), 1)
        
        self.assertEquals(len(state.getPermissionInfo('UWOshOIE: Modify Office Use Only fields')['roles']), 0)
        self.assertEquals(len(state.getPermissionInfo('UWOshOIE: Modify Financial Aid fields')['roles']), 0)
        self.assertEquals(len(state.getPermissionInfo('UWOshOIE: Review OIE Application')['roles']), 0)
                
    def test_readyForConditionalAdmit(self):
        self.failUnless('readyForConditionalAdmit' in self.states.objectIds())
        state = self.states['readyForConditionalAdmit']
        
        self.hasTheseTransitions(state, [  'addComment', 'admitConditionally', 'decline', 'withdraw'])
        
    def test_readyForConditionalAdmit_permsissions(self):
        state = self.states['readyForConditionalAdmit']
        
        self.hasPermissionRoles(state, 'list', ['Owner', 'UWOshOIEDirector', 'UWOshOIEFacReview', 'UWOshOIEFinAid', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        self.hasPermissionRoles(state, 'Modify portal content', ['Owner', 'UWOshOIEDirector', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        self.hasPermissionRoles(state, 'View', ['Owner', 'UWOshOIEDirector', 'UWOshOIEFacReview', 'UWOshOIEFinAid', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        self.hasPermissionRoles(state, 'Access contents information', ['Owner', 'UWOshOIEDirector', 'UWOshOIEFacReview', 'UWOshOIEFinAid', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        self.hasPermissionRoles(state, 'UWOshOIE: Review OIE Application', ['UWOshOIEProgramManager'])
        self.hasPermissionRoles(state, 'UWOshOIE: Modify revisable fields', ['Owner', 'UWOshOIEDirector', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        self.hasPermissionRoles(state, 'UWOshOIE: Modify Financial Aid fields', ['UWOshOIEDirector', 'UWOshOIEFinAid', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        self.hasPermissionRoles(state, 'UWOshOIE: Modify Office Use Only fields', ['UWOshOIEDirector', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        self.hasPermissionRoles(state, 'UWOshOIE: Modify normal fields', ['UWOshOIEDirector', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        
    def test_seatAssigned(self):
        self.failUnless('seatAssigned' in self.states.objectIds())
        state = self.states['seatAssigned']
        
        self.hasTheseTransitions(state, [  'addComment', 'archive', 'decline', 'withdraw'])
        
    def test_seatAssigned_permissions(self):
        state = self.states['seatAssigned']
        
        self.hasPermissionRoles(state, 'list', ['Owner', 'UWOshOIEDirector', 'UWOshOIEFacReview', 'UWOshOIEFinAid', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        self.hasPermissionRoles(state, 'Modify portal content',['Owner', 'UWOshOIEDirector', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        self.hasPermissionRoles(state, 'View', ['Owner', 'UWOshOIEDirector','UWOshOIEFacReview', 'UWOshOIEFinAid', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        self.hasPermissionRoles(state, 'Access contents information', ['Owner', 'UWOshOIEDirector', 'UWOshOIEFacReview', 'UWOshOIEFinAid', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        self.hasPermissionRoles(state, 'UWOshOIE: Review OIE Application', ['UWOshOIEFrontLineAdvisor'])
        self.hasPermissionRoles(state, 'UWOshOIE: Modify revisable fields', ['Owner', 'UWOshOIEDirector', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        self.hasPermissionRoles(state, 'UWOshOIE: Modify Financial Aid fields', ['UWOshOIEDirector', 'UWOshOIEFinAid', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        self.hasPermissionRoles(state, 'UWOshOIE: Modify Office Use Only fields', ['UWOshOIEDirector', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        self.hasPermissionRoles(state, 'UWOshOIE: Modify normal fields', ['UWOshOIEDirector', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        
    def test_waitingForPrintMaterials(self):
        self.failUnless('waitingForPrintMaterials' in self.states.objectIds())
        state = self.states['waitingForPrintMaterials']
        
        self.hasTheseTransitions(state, [  'addComment', 'decline', 'sendForDirectorReview', 'withdraw'])
        
    def test_waitForPrintMaterials_permissions(self):
        state = self.states['waitingForPrintMaterials']
        
        self.hasPermissionRoles(state, 'list', ['Owner', 'UWOshOIEDirector', 'UWOshOIEFacReview', 'UWOshOIEFinAid', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        self.hasPermissionRoles(state, 'Modify portal content', ['Owner', 'UWOshOIEDirector', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        self.hasPermissionRoles(state, 'View', ['Owner', 'UWOshOIEDirector', 'UWOshOIEFacReview', 'UWOshOIEFinAid', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        self.hasPermissionRoles(state, 'Access contents information', ['Owner', 'UWOshOIEDirector', 'UWOshOIEFacReview', 'UWOshOIEFinAid', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        self.hasPermissionRoles(state, 'UWOshOIE: Review OIE Application', ['UWOshOIEFrontLineAdvisor'])
        self.hasPermissionRoles(state, 'UWOshOIE: Modify revisable fields', ['Owner', 'UWOshOIEDirector', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        self.hasPermissionRoles(state, 'UWOshOIE: Modify Financial Aid fields', ['UWOshOIEDirector', 'UWOshOIEFinAid', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        self.hasPermissionRoles(state, 'UWOshOIE: Modify Office Use Only fields', ['UWOshOIEDirector', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        self.hasPermissionRoles(state, 'UWOshOIE: Modify normal fields', ['UWOshOIEDirector', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        
    def test_waitlist(self):
        self.failUnless('waitlist' in self.states.objectIds())
        state = self.states['waitlist']
        
        self.hasTheseTransitions(state, [  'addComment', 'assertReadyForConditionalAdmit', 'decline', 'withdraw'])
        
    def test_waitlist_permissions(self):
        state = self.states['waitlist']
        
        self.hasPermissionRoles(state, 'list', ['Owner', 'UWOshOIEDirector', 'UWOshOIEFacReview', 'UWOshOIEFinAid', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        self.hasPermissionRoles(state, 'Modify portal content', ['Owner', 'UWOshOIEDirector', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        self.hasPermissionRoles(state, 'View', ['Owner', 'UWOshOIEDirector', 'UWOshOIEFacReview', 'UWOshOIEFinAid', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        self.hasPermissionRoles(state, 'Access contents information', ['Owner', 'UWOshOIEDirector','UWOshOIEFacReview', 'UWOshOIEFinAid', 'UWOshOIEFrontLineAdvisor','UWOshOIEProgramManager'])
        self.hasPermissionRoles(state, 'UWOshOIE: Review OIE Application', ['UWOshOIEProgramManager'])
        self.hasPermissionRoles(state, 'UWOshOIE: Modify revisable fields', ['Owner',  'UWOshOIEDirector', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        self.hasPermissionRoles(state, 'UWOshOIE: Modify Financial Aid fields', ['UWOshOIEDirector', 'UWOshOIEFinAid', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        self.hasPermissionRoles(state, 'UWOshOIE: Modify Office Use Only fields', ['UWOshOIEDirector', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        self.hasPermissionRoles(state, 'UWOshOIE: Modify normal fields', ['UWOshOIEDirector', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        
    def test_withdrawn(self):
        self.failUnless('withdrawn' in self.states.objectIds())
        state = self.states['withdrawn']
        
        self.hasTheseTransitions(state, [  'addComment', 'archive'])

    def test_withdrawn_permissions(self):
        state = self.states['withdrawn']
        
        self.hasPermissionRoles(state, 'list', ['Owner', 'UWOshOIEDirector', 'UWOshOIEFacReview', 'UWOshOIEFinAid', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        self.assertEquals(len(state.getPermissionInfo('Modify portal content')['roles']), 0)
        self.hasPermissionRoles(state, 'View', ['Owner', 'UWOshOIEDirector', 'UWOshOIEFacReview', 'UWOshOIEFinAid', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        self.hasPermissionRoles(state, 'Access contents information', ['Owner', 'UWOshOIEDirector', 'UWOshOIEFacReview', 'UWOshOIEFinAid', 'UWOshOIEFrontLineAdvisor', 'UWOshOIEProgramManager'])
        self.assertEquals(len(state.getPermissionInfo('UWOshOIE: Review OIE Application')['roles']), 0)
        self.assertEquals(len(state.getPermissionInfo('UWOshOIE: Modify revisable fields')['roles']), 0)
        self.assertEquals(len(state.getPermissionInfo('UWOshOIE: Modify Financial Aid fields')['roles']), 0)
        self.assertEquals(len(state.getPermissionInfo('UWOshOIE: Modify Office Use Only fields')['roles']), 0)
        self.assertEquals(len(state.getPermissionInfo('UWOshOIE: Modify normal fields')['roles']), 0)
        
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestStatesInstalled))

    return suite

if  __name__ == '__main__':
    framework()
