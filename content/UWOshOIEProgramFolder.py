from Products.ATContentTypes.content.folder import ATFolder, ATFolderSchema
from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from Products.UWOshOIE.config import PROJECTNAME

class UWOshOIEProgramFolder(ATFolder):
    security = ClassSecurityInfo()
    __implements__ = (getattr(BaseContent,'__implements__',()),)

    # This name appears in the 'add' box
    archetype_name             = 'OIE Program Folder'

    meta_type                  = 'UWOshOIEProgramFolder'
    portal_type                = 'UWOshOIEProgramFolder'
    allowed_content_types      = ['UWOshOIEProgram']
    filter_content_types       = 1
    global_allow               = 1
    allow_discussion           = 0
    immediate_view             = 'program_folder_tabular_view'
    default_view               = 'program_folder_tabular_view'
    suppl_views                = ()
    typeDescription            = "OIE Program Folder"

    schema = ATFolderSchema
    

registerType(UWOshOIEProgramFolder,PROJECTNAME)