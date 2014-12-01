from Products.ATContentTypes.content.folder import ATFolder, ATFolderSchema
from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from Products.UWOshOIE.config import PROJECTNAME

class UWOshOIEEmailTemplateFolder(ATFolder):
    security = ClassSecurityInfo()
    __implements__ = (getattr(BaseContent,'__implements__',()),)


    # This name appears in the 'add' box
    archetype_name             = 'OIE Email Template Folder'

    meta_type                  = 'UWOshOIEEmailTemplateFolder'
    portal_type                = 'UWOshOIEEmailTemplateFolder'
    allowed_content_types      = ['UWOshOIEEmailTemplate']
    filter_content_types       = 1
    global_allow               = 1
    allow_discussion           = 0
    immediate_view             = 'emailtemplate_folder_tabular_view'
    default_view               = 'emailtemplate_folder_tabular_view'
    suppl_views                = ()
    typeDescription            = "OIE Email Template Folder"
    typeDescMsgId              = 'description_edit_oieprogram'

    schema = ATFolderSchema
    

registerType(UWOshOIEEmailTemplateFolder,PROJECTNAME)