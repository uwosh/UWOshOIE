__author__  = '''Nathan Van Gheem'''
__docformat__ = 'plaintext'


from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from Products.validation.validators import ExpressionValidator
from Products.ATVocabularyManager.namedvocabulary import NamedVocabulary
from Products.UWOshOIE.config import *
from Products.CMFCore.utils import getToolByName
from zLOG import LOG, INFO, WARNING, ERROR
from time import ctime

copied_fields = {}
copied_fields['title'] = BaseSchema['title'].copy()
copied_fields['title'].required = 1
copied_fields['title'].searchable = 1
copied_fields['title'].write_permission = "UWOshOIE: Modify Office Use Only fields"
copied_fields['title'].widget.label = "Program Name"

schema=Schema((
    copied_fields['title'],
    TextField('description',
        allowable_content_types = ('text/plain', 'text/structured', 'text/html',),
        default_output_type = 'text/x-html-safe',
        widget=RichWidget(
            label="Program Description",
            rows=10
        ),
        read_permission="UWOshOIE: Modify revisable fields",
        write_permission="UWOshOIE: Modify Office Use Only fields",
        index='FieldIndex:schema',
        searchable="1"
    ),
    StringField('facultyLeaders',
        widget=LinesWidget(
            label="Faculty Leaders",
            description="Put each Faculty Leader username on a new line",
            label_msgid='UWOshOIE_label_title',
            description_msgid='UWOshOIE_help_title',
            i18n_domain='UWOshOIE'
        ),
        write_permission="UWOshOIE: Modify Office Use Only fields", 
        searchable="1",
        index='FieldIndex:schema',
        multiValued=True
    )
))

UWOshOIEProgram_schema = BaseSchema + schema

class UWOshOIEProgram(BaseContent):
    security = ClassSecurityInfo()
    __implements__ = (getattr(BaseContent,'__implements__',()),)


    # This name appears in the 'add' box
    archetype_name             = 'OIE Program'

    meta_type                  = 'UWOshOIEProgram'
    portal_type                = 'UWOshOIEProgram'
    allowed_content_types      = []
    filter_content_types       = 0
    global_allow               = 1
    allow_discussion           = 0
    immediate_view             = 'base_view'
    default_view               = 'base_view'
    suppl_views                = ()
    typeDescription            = "OIE Program"
    typeDescMsgId              = 'description_edit_oieprogram'

    schema = UWOshOIEProgram_schema
    
    def getFacultyAddresses(self):
        pm = getToolByName(self, "portal_membership")
        emails = []
        
        for mname in self.getFacultyLeaders():
            m = pm.getMemberById (mname)
            if m and m.getProperty('email', None):
                emails.append(m.getProperty('email'))
                
        return emails

registerType(UWOshOIEProgram, PROJECTNAME)