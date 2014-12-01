from Products.CMFCore.utils import getToolByName
import urllib

def has_faculty_permissions(self):

    pm = self.portal_membership
    member = pm.getAuthenticatedMember()
    roles = member.getRolesInContext(self)
    
    for role in roles:
        permissions = self.permissionsOfRole(role)
        
        for permission in permissions:
            if permission['selected'] and permission['name'] == 'UWOshOIE: Modify Office Use Only fields':
                return True
                
                
    return False
    
    
def get_attributes(self, obj):
    return dir(obj)
    
def url_encode(self, value):
    return urllib.urlencode(value).replace('+', '%20')

def import_default_programs(self):
    from Products.UWOshOIE.Extensions.Settings.ProgramsAndFacultyLeaders import Programs

    programFolderId = self.generateUniqueId()
    self.invokeFactory(type_name='UWOshOIEProgramFolder', id=programFolderId, title='Programs')
    
    programFolder = self[programFolderId]


    for program in Programs.keys():
        programId = programFolder.generateUniqueId()
        programFolder.invokeFactory(type_name='UWOshOIEProgram', id=programId, title=program)

        programFolder[programId].setFacultyLeaders(Programs[program])
        programFolder[programId].setTitle(program)    
        

def get_workflow_state_description(self, state):
    portal = getToolByName(self, 'portal_url').getPortalObject()
    
    wf = portal.portal_workflow['OIEStudentApplicationWorkflow']
    return wf.states[state].description

def get_transition_information(self, action):
    transition = action['transition']
    
    trans = {
        'title': transition.title,
        'id': transition.id,
        'description': transition.description
    }
    
    return trans
    
def get_oie_states_ids(self):
    return self.portal_workflow.OIEStudentApplicationWorkflow.states.objectIds()
    
def get_state_info(self, state_id):
    state = self.portal_workflow.OIEStudentApplicationWorkflow.states[state_id]
    
    info = {
        'title': state.title,
        'url': state.absolute_url(),
        'transitions': state.transitions
    }
    
    return info
    
def get_transition_info(self, transition_id):
    transition = self.portal_workflow.OIEStudentApplicationWorkflow.transitions[transition_id]
    
    info = {
        'title': transition.title,
        'url': transition.absolute_url()
    }
    
    return info
    
def yesorno(self, value):
    if value in ["0", False, 0, "No", "NO", "no"]:
        return "No"
    else:
        return "Yes"