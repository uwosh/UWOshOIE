"""
This file houses all helper functions that the workflow scripts will use
"""

__author__    = '''Nathan Van Gheem <vangheem@gmail.com>'''

from Products.UWOshOIE.content.OIEStudentApplication import OIEStudentApplication
from Products.UWOshOIE.config import DEFAULT_NOTIFICATION_EMAIL_ADDRESS
from Products.CMFCore.utils import getToolByName
from zLOG import LOG, INFO, ERROR, WARNING
from Products.UWOshOIE.Extensions.Exceptions import StateError

#only for debugging
#from Globals import DevelopmentMode
#from Products.UWOshOIE.config import DEBUG_MODE
#from Products.UWOshSecureMailHost.UWOshSecureMailHost import UWOshSecureMailHost
#DEBUG_MAIL_HOST = UWOshSecureMailHost()

"""
Gets the UWOshOIEEmailTemplate for the specified transition
"""
def getEmailMessageTemplate(self, transition, onFailure=False):
    #LOG ("getEmailMessageTemplate", INFO, "called with onFailure='%s'" % (onFailure))
    if onFailure:
        onFailure = True
    else:
        onFailure = False
    #LOG ("getEmailMessageTemplate", INFO, "reinterpreted onFailure='%s'" % (onFailure))
    
    templates = self.queryCatalog({
        'portal_type': 'UWOshOIEEmailTemplate', 
        'getTransition': transition, 
        #'getSendEmailOnFailure': onFailure, # this does NOT work so must filter below
        'sort_on': 'modified'
    })
    # the queryCatalog() does not return correctly based on getSendEmailOnFailure filter value passed in
    retlist = []
    for t in templates:
        obj = t.getObject()
        if obj.getSendEmailOnFailure() == onFailure:
            retlist.append(obj)
    #LOG ("getEmailMessageTemplate", INFO, "templates='%s', length=%s" % (templates, len(templates)))
    
    if len(retlist) > 0:
        retval = retlist[0]
        LOG ("getEmailMessageTemplate", INFO, "returning '%s'" % (retval))
        return retval
    else:
        LOG ("getEmailMessageTemplate", INFO, "returning None")
        return None

def intializeMissingValues(missingValues, key):
    if key not in missingValues:
        missingValues[key] = []

def getCreatorInfo(self, application):
    pmtool = getToolByName(self, 'portal_membership', None)
    creator = application.Creator()
    member = pmtool.getMemberById(creator)
    
    return {
        'member':   member,
        'id':       member.getId(),
        'fullname': member.getProperty('fullname', 'Fullname missing'),
        'email':    member.getProperty('email', None)
    }

def getReviewerInfo(self, application):
    pmtool = getToolByName(self, 'portal_membership', None)
    wftool = getToolByName(self, 'portal_workflow', None)
    
    actorid = wftool.getInfoFor(application, 'actor')
    actor = pmtool.getMemberById(actorid)
    
    reviewer = {
        'member':actor,
        'id':actor.getId(),
        'fullname':actor.getProperty('fullname', 'Fullname missing'),
        'email':actor.getProperty('email', None)
    }
                
    return reviewer

#cc will be faculty on that transition
def getToAddresses(application, emailTemplate, cc=[]):
    addresses = []
    
    #student email
    addresses.append(application.getEmail())
    
    if emailTemplate:
        #custom specified emails sent
        addresses.extend(emailTemplate.getFormattedCCAddresses())
        
    if cc is not None:
        addresses.extend(cc)
    
    return addresses

def assembleEmailMessage(self, application, wftool, emailTemplate, onFailure):

    mMsg = """

Your UW Oshkosh Office of International Education study abroad application has been updated.

Name: %s
Program Name: %s
Program Year: %s

%s

You can view your application here: %s

Comment: %s

%s
""" % ( 
        application.getFirstName() + " " + application.getLastName(),
        application.getProgramNameAsString(),
        application.getProgramYear(),
        emailTemplate.getFormattedEmailText(), 
        application.absolute_url(), 
        wftool.getInfoFor(application, 'comments'),
        getAssembledErrorMessage(onFailure)
    )
    
    return mMsg
    
def sendTransitionMessage(self, state_change, cc=[], onFailure=False):
    portal = getToolByName(self,'portal_url').getPortalObject()
    wftool = getToolByName(self, 'portal_workflow', None)
    
    application = state_change.object
    emailTemplate = getEmailMessageTemplate(self, state_change.transition.id, onFailure)
    history = state_change.getHistory()
    
    old_state_id = state_change.old_state.id
    new_state_id = state_change.new_state.id
    
    creator = getCreatorInfo(self, application)
    reviewer = getReviewerInfo(self, application)

    mTo = getToAddresses(application, emailTemplate, cc)
    mFrom = reviewer['email']
    
    #If the owner is performing action, this will prevent them from sending an email to themselves
    if mFrom in mTo:
        mFrom = DEFAULT_NOTIFICATION_EMAIL_ADDRESS
    
    mSubj = 'Your study abroad application update (UW Oshkosh Office of International Education)'

    state_msg = None
    if old_state_id != new_state_id:
        state_msg = "Its state has changed from '" + old_state_id + "' to '" + new_state_id + "'.\n\n"

    canSendEmail = emailTemplate and emailTemplate.canSendEmail(onFailure)
    if emailTemplate and canSendEmail:
        LOG ("sendTransitionMessage", INFO, "Sending transition email for transition %s to %s, subject '%s', onFailure = '%s', emailTemplate = '%s', canSendEmail = '%s'" % (state_change.transition.id, mTo, mSubj, onFailure, emailTemplate, canSendEmail))
        mMsg = assembleEmailMessage(self, application, wftool, emailTemplate, onFailure)

        #only for debugging
        #if DEBUG_MODE or DevelopmentMode:
        #    DEBUG_MAIL_HOST.secureSend(mMsg, mTo, mFrom, mSubj)
        #else:
        portal.MailHost.secureSend(mMsg, mTo, mFrom, mSubj)
    else:
        LOG ("sendTransitionMessage", INFO, "Not sending transition email for transition %s to %s, subject '%s', onFailure = '%s', emailTemplate = '%s', canSendEmail = '%s'" % (state_change.transition.id, mTo, mSubj, onFailure, emailTemplate, canSendEmail))

        
def check_for_required_values_by_state(self, state_change, alreadyMissingValues={}):
    # Find all values that must exist before we can move into the new state.
    # This is very similar to what we do in pre_submit.
    application = state_change.object
    newState = state_change.new_state.id

    missingValues = {}
    if len(alreadyMissingValues) > 0:
        missingValues = alreadyMissingValues

    requiredFields = [] # e.g. ['firstName', 'lastName', 'email', 'localAddr1']

    for f in OIEStudentApplication.schema.fields():
        states_required = getattr(f, 'required_by_state', None)
        if states_required and newState in states_required:
            requiredFields.append(f)

    for f in requiredFields:
        aName = f.getName()
        aValue = getattr(application, aName, None)
        aType = f.getType()
        must_be = getattr(f, 'must_be', None)
        must_not_be = getattr(f, 'must_not_be', None)

        if aValue == None or str(aValue) == '':       # have to cast to a string to handle Products.Archetypes.Field.TextField values
            if must_be is None:
                must_be = "Any Value"
            intializeMissingValues(missingValues, f.schemata)
            missingValues[f.schemata].append({'expected': must_be, 
                                  'current_value': str(aValue), 
                                  'field': f.widget.label, 
                                  'message': 'You are missing this required field'})
            break

        if must_be is not None and aValue != must_be and (aValue != None or len(str(aValue)) == 0):
            intializeMissingValues(missingValues, f.schemata)
            missingValues[f.schemata].append({'expected': str(must_be), 
                                  'current_value': str(aValue), 
                                  'field': f.widget.label, 
                                  'message': 'You have entered or are missing information that makes the application invalid'})
            break

        if must_not_be is not None and aValue == must_not_be and aValue != None:
            intializeMissingValues(missingValues, f.schemata)
            missingValues[f.schemata].append({'expected': 'NOT  ' + str(must_not_be), 
                                  'current_value': str(aValue), 
                                  'field': f.widget.label, 
                                  'message': 'You are missing or have entered information that makes the application invalid'})

    if len(missingValues) > 0:
        sendTransitionMessage(self, state_change, None, missingValues)

        raise StateError, missingValues

def getAssembledErrorMessage(errorMessage):
    
    if errorMessage:
    
        message = ''
        for key in errorMessage.keys():
            message += '\n\n Section: ' + key + '\n'
            for error in errorMessage[key]:
                message += 'Field: ' + error['field'] + ',\tExplanation: ' + error['message'] + '\n'

        return message
        
    else:
        return ''

def checkProgramSpecificMaterials(self,state_change):
    application = state_change.object
    missingValues = {}
    if getattr(application, 'programSpecificMaterialsRequired', None) == "Yes":
        if getattr(application, 'programSpecificMaterialsOK', None) == "No":
            intializeMissingValues(missingValues, "OFFICE USE ONLY")
            missingValues['OFFICE USE ONLY'].append( 
                    {'expected': "'program-specific materials OK' box to be checked",
                      'current_value': 'unchecked',
                      'field': 'program-specific materials OK',
                      'message': "Can not move to state until this has been fixed"}
                      )
    if getattr(application, 'specialStudentFormRequired', None) == "Yes":
        if getattr(application, 'specialStudentFormOK', None) == "No":
            intializeMissingValues(missingValues, "OFFICE USE ONLY")
            missingValues['OFFICE USE ONLY'].append( 
                    {'expected': "'special student form OK' box to be checked",
                      'current_value': 'unchecked',
                      'field': 'special student form OK',
                      'message': "Can not move to state until this has been fixed"})
    if getattr(application, 'creditOverloadFormRequired', None) == "Yes":
        if getattr(application, 'creditOverloadFormOK', None) == "No":
            intializeMissingValues(missingValues, "OFFICE USE ONLY")
            missingValues['OFFICE USE ONLY'].append( 
                        {'expected': "'credit overload form OK' box to be checked",
                          'current_value': 'unchecked',
                          'field': 'credit overload form OK',
                          'message': "Can not move to state until this has been fixed"})

    return missingValues

def checkProgramSpecificMaterialsStepIII(self,state_change):
    application = state_change.object
    missingValues = {}
    if getattr(application, 'programSpecificMaterialsRequiredStepIII', None) == "Yes":
        if getattr(application, 'programSpecificMaterialsOKStepIII', None) == "No":
            intializeMissingValues(missingValues, "OFFICE USE ONLY")
            missingValues['OFFICE USE ONLY'].append(
                            {'expected': "'program-specific materials specified(Step III)' box to be checked",
                             'current_value': 'unchecked',
                             'field': 'program-specific materials specified',
                             'message': "Can not move to state until this has been fixed"})

    return missingValues
    
    
def check_for_hold (self,state_change):
    val = state_change.object.getHoldApplication()
    LOG ("pre_holdForFAIncomplete", INFO, "The value of the holdApplication field is %s" % val)
    if val <> 'HOLD':
        raise StateError, {'Financial Aid': 
                [{'expected': 'HOLD',
                  'current_value': val,
                  'field': 'Hold Application',
                  'message': "Can not move to state until it is set to 'HOLD'"}]}

def afterTransition(application, state_id):
    pass
