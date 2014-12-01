""" Workflow Scripts for: OIEStudentApplicationWorkflow """

# Copyright (c) 2007 by 
#
# Generator: ArchGenXML Version 1.4.0-RC1
#            http://sf.net/projects/archetypes/
#
# GNU General Public Licence (GPL)
# 
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 59 Temple
# Place, Suite 330, Boston, MA  02111-1307  USA
#
__author__    = '''Nathan Van Gheem <vangheem@gmail.com>'''

##code-section workflow-script-header #fill in your manual code here
from zLOG import LOG, INFO, ERROR, WARNING
from Products.CMFCore.utils import getToolByName
from Products.UWOshOIE.Extensions.Exceptions import StateError
from Products.UWOshOIE.config import DEFAULT_NOTIFICATION_EMAIL_ADDRESS
from Products.CMFCore.utils import getToolByName
from Products.UWOshOIE.Extensions.WorkflowScriptHelpers import *

def pre_addComment(self,state_change,**kw):
    pass

def post_addComment(self,state_change,**kw):
    sendTransitionMessage(self, state_change)

def pre_addToWaitlist(self,state_change,**kw):
    return check_for_required_values_by_state (self, state_change, {})

def post_addToWaitlist(self,state_change,**kw):
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)

def pre_approveForFA(self,state_change,**kw):
    return check_for_required_values_by_state (self, state_change, {})

def post_approveForFA(self,state_change,**kw):
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)

def pre_archive(self,state_change,**kw):
    return check_for_required_values_by_state (self, state_change, {})

def post_archive(self,state_change,**kw):
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)

def pre_assignSeat(self,state_change,**kw):
    missingValues = checkProgramSpecificMaterialsStepIII(self, state_change)
    return check_for_required_values_by_state (self, state_change, missingValues)

def post_assignSeat(self,state_change,**kw):
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)

def pre_assertReadyForConditionalAdmit(self,state_change,**kw):
    return check_for_required_values_by_state (self, state_change, {})

def post_assertReadyForConditionalAdmit(self,state_change,**kw):
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)

def pre_assertReadyForConditionalAdmitFromFacultyReview(self,state_change,**kw):
    return check_for_required_values_by_state (self, state_change, {})

def post_assertReadyForConditionalAdmitFromFacultyReview(self,state_change,**kw):
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)

def pre_admitConditionally(self,state_change,**kw):
    return check_for_required_values_by_state (self, state_change, {})

def post_admitConditionally(self,state_change,**kw):
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)

def pre_decline(self,state_change,**kw):
    return check_for_required_values_by_state (self, state_change, {})

def post_decline(self,state_change,**kw):
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)

def pre_declineFromFacultyReview(self,state_change,**kw):
    return check_for_required_values_by_state (self, state_change, {})

def post_declineFromFacultyReview(self,state_change,**kw):
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)

def pre_facultyApproves(self,state_change,**kw):
    return check_for_required_values_by_state (self, state_change, {})

def post_facultyApproves(self,state_change,**kw):
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)

def pre_holdForFAIncomplete(self,state_change,**kw):
    check_for_hold(self, state_change)
    return check_for_required_values_by_state (self, state_change, {})

def post_holdForFAIncomplete(self,state_change,**kw):
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)

def pre_recheckForFAHold(self,state_change,**kw):
    check_for_hold(self, state_change)
    return check_for_required_values_by_state (self, state_change, {})

def attempt_transition_to_FAHeld (self, state_change, **kw):
    if state_change.object.getHoldApplication() == 'HOLD':
        wf_tool = getToolByName (self, "portal_workflow")
        comment = "Automatic transition"
        wf_tool.doActionFor (state_change.object, 'holdForFAIncomplete', comment=comment)

def post_recheckForFAHold(self,state_change,**kw):
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)
    self.attempt_transition_to_FAHeld(state_change)

def pre_manageDeadlines(self,state_change,**kw):
    return check_for_required_values_by_state (self, state_change, {})
    
def post_manageDeadlines(self,state_change,**kw):
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)

def pre_sendForDirectorReview(self,state_change,**kw):
    missingValues = checkProgramSpecificMaterials(self, state_change)
    return check_for_required_values_by_state (self, state_change, missingValues)

def post_sendForDirectorReview(self,state_change,**kw):
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)

def pre_sendForFacultyReview(self,state_change,**kw):
    return check_for_required_values_by_state (self, state_change, {})      

def post_sendForFacultyReview(self,state_change,**kw):
    afterTransition(state_change.object, state_change.new_state.id)
    application = state_change.object
    cc = []
    
    if application.getProgramName() != None:
        cc.extend(application.getProgramName().getFacultyAddresses())
    
    sendTransitionMessage(self, state_change, cc = cc)

def pre_sendForProgramManagerReview(self,state_change,**kw):
    return check_for_required_values_by_state (self, state_change, {})      

def post_sendForProgramManagerReview(self,state_change,**kw):
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)

def pre_submit(self,state_change,**kw):
    obj = state_change.object
    missingValues = {}        
                              
    requiredFields = [] # e.g. ['firstName', 'lastName', 'email', 'localAddr1']
    
    for f in OIEStudentApplication.schema.fields():
        if f.required == 1:
            requiredFields.append(f)

    for f in requiredFields:
        aName = f.getName()
        aValue = getattr(obj, aName, None)
        aType = f.getType()
        must_be = getattr(f, 'must_be', None)
        must_not_be = getattr(f, 'must_not_be', None)
        
        try:
            if str(aValue) == '':       # have to cast to a string to handle Products.Archetypes.Field.TextField values
                intializeMissingValues(missingValues, f.schemata)
                missingValues[f.schemata].append({'expected': must_be or 'Any Value', 
                                      'current_value': aValue, 
                                      'field': f.widget.label, 
                                      'message': 'You are missing this required field'})
        except:
            LOG ("pre_submit", ERROR, "required field '%s', possible Unicode problem: aValue = '%s', aType = '%s', must_be = '%s', must_not_be = '%s'" % (f, aValue, aType, must_be, must_not_be))
        
        if must_be is not None and aValue != must_be:
            intializeMissingValues(missingValues, f.schemata)
            missingValues[f.schemata].append({'expected': must_be, 
                                  'current_value': aValue, 
                                  'field': f.widget.label, 
                                  'message': 'You have entered information that makes the application invalid'})
        if must_not_be is not None and aValue == must_not_be:
            intializeMissingValues(missingValues, f.schemata)
            missingValues[f.schemata].append({'expected': 'NOT  ' + must_not_be, 
                                  'current_value': aValue, 
                                  'field': f.widget.label, 
                                  'message': 'You have entered information that makes the application invalid'})
            
    check_for_required_values_by_state (self, state_change, missingValues)

def post_submit(self,state_change,**kw):
    afterTransition(state_change.object, state_change.new_state.id)
    self.attempt_transition_to_FAHeld (state_change)
    sendTransitionMessage(self, state_change)

def pre_waitForPrintedMaterials(self,state_change,**kw):
    return check_for_required_values_by_state (self, state_change, {})

def post_waitForPrintedMaterials(self,state_change,**kw):
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)

def pre_withdraw(self,state_change,**kw):
    return check_for_required_values_by_state (self, state_change, {})

def post_withdraw(self, state_change, **kw):
    afterTransition(state_change.object, state_change.new_state.id)
    sendTransitionMessage(self, state_change)
