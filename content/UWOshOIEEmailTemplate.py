__author__  = '''Nathan Van Gheem'''
__docformat__ = 'plaintext'


from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from Products.UWOshOIE.config import *
from Products.CMFCore.utils import getToolByName
from zLOG import LOG, INFO, WARNING, ERROR
from time import ctime
from re import sub
import re

transitions_to_use = [
    'addComment',
    'addToWaitlist', 
    'admitConditionally', 
    'approveForFA', 
    'archive', 
    'assertReadyForConditionalAdmit',
    'assignSeat',
    'decline',
    'declineFromFacultyReview',
    'facultyApproves',
    'holdForFAIncomplete',
    'manageDeadlines',
    'recheckForFAHold',
    'sendForDirectorReview',
    'sendForFacultyReview',
    'sendForProgramManagerReview',
    'submit',
    'waitForPrintedMaterials',
    'withdraw'
]

copied_fields = {}
copied_fields['title'] = BaseSchema['title'].copy()
copied_fields['title'].required = 1
copied_fields['title'].searchable = 1
copied_fields['title'].write_permission = "UWOshOIE: Modify Office Use Only fields"
copied_fields['title'].widget.label = "Template Name"

schema=Schema((
    copied_fields['title'],
    
    StringField('transition',
        widget=SelectionWidget(
            label="Transition Name",
            description="Transition that it will send an email on."
        ),
        write_permission="UWOshOIE: Modify Office Use Only fields",
        vocabulary=transitions_to_use
    ),
    
    BooleanField('sendEmail',
        widget=BooleanWidget(
            label="Send Email on Transition",
            description="Check this box to send an email on this transition"
        ),
        default=True,
        write_permission="UWOshOIE: Modify Office Use Only fields"
    ),
    
    BooleanField('sendEmailOnFailure',
        widget=BooleanWidget(
            label="Send Email on Transition Failure Only?",
            description="Check this box to send an email on transition failure only."
        ),
        default=False,
        write_permission="UWOshOIE: Modify Office Use Only fields"
    ),
    
    StringField('ccUsers',
        widget=LinesWidget(
            label="CC users",
            description="Put each username on a new line that you want cc'd.  You can just enter the username or the full email address."
        ),
        write_permission="UWOshOIE: Modify Office Use Only fields",
        multiValued=True,
        default=['oie@uwosh.edu']
    ),
    
    TextField('emailText',
        allowable_content_types = ('text/plain', 'text/structured', 'text/html',),
        default_output_type = 'text/x-html-safe',
        widget=RichWidget(
            label="Email Text",
            description="Text that will display in the email body."
        ),
        write_permission="UWOshOIE: Modify Office Use Only fields"
    ),
))

UWOshOIEEmailTemplate_schema = BaseSchema + schema

class UWOshOIEEmailTemplate(BaseContent):
    security = ClassSecurityInfo()
    __implements__ = (getattr(BaseContent,'__implements__',()),)


    # This name appears in the 'add' box
    archetype_name             = 'OIE Email Template'

    meta_type                  = 'UWOshOIEEmailTemplate'
    portal_type                = 'UWOshOIEEmailTemplate'
    global_allow               = 1
    allow_discussion           = 0
    immediate_view             = 'base_view'
    default_view               = 'base_view'
    suppl_views                = ()
    typeDescription            = "OIE Email Template"

    schema = UWOshOIEEmailTemplate_schema
    
    emailRE = re.compile('^([^@\s]+)@((?:[-a-z0-9]+\.)+[a-z]{2,})$')
    
    def getFormattedEmailText(self):
        text = self.getEmailText().replace('<p>','').replace('</p>','\n\n').replace('<br />', '\n').replace('<br>', '\n').replace('&amp;', '&').replace('</a>','')
        text = sub(r'<a href="[^"]+">', '', text)

        return text
        
    def getCCAddressesAsString(self):
        pm = getToolByName(self, "portal_membership")
        address = ""
        
        for memberName in self.getCcUsers():
            if self.emailRE.match(memberName):
                address += memberName + ';'
            else:
                member = pm.getMemberById (memberName)
                if member:
                    address += member.getProperty('email', '') + ';'

        return address

    def getFormattedCCAddresses(self):
        pm = getToolByName(self, "portal_membership")
        addresses = []
        
        for memberName in self.getCcUsers():
            if self.emailRE.match(memberName):
                addresses.append(memberName)
            else:
                member = pm.getMemberById(memberName)
                if member and member.getProperty('email', None):
                    addresses.append(member.getProperty('email'))

        return addresses

    def canSendEmail(self, isFailure):
        if isFailure == False:
            retval = self.getSendEmail()
            LOG ("canSendEmail", INFO, "isFailure = '%s', returning '%s'" % (isFailure, retval))
            return retval
        else:
            se = self.getSendEmail()
            seof = self.getSendEmailOnFailure()
            retval = se and seof
            LOG ("canSendEmail", INFO, "isFailure = '%s', sendEmail = '%s', sendEmailOnFailure = '%s', returning '%s'" % (isFailure, se, seof, retval))
            return retval
            

registerType(UWOshOIEEmailTemplate,PROJECTNAME)
