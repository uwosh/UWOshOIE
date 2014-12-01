#
# Product configuration. This contents of this module will be imported into
# __init__.py and every content type module.
#
# If you wish to perform custom configuration, you may put a file AppConfig.py
# in your product's root directory. This will be included in this file if
# found.
#
from Products.CMFCore.CMFCorePermissions import setDefaultRoles

PROJECTNAME = "UWOshOIE"
DEFAULT_ADD_CONTENT_PERMISSION = "Add portal content"
setDefaultRoles(DEFAULT_ADD_CONTENT_PERMISSION, ('Manager', 'Owner'))
DEFAULT_NOTIFICATION_EMAIL_ADDRESS = "oie@uwosh.edu"
OIE_FROM_NAME = "OIE Portal Administrator"
PORTAL_TITLE = "OIE Portal"
DEBUG_MODE =False 

product_globals=globals()

EXTERNAL_METHODS = [{
    'id': 'has_faculty_permissions', 
    'description': '', 
    'module': 'UWOshOIE.OIE_Utilities', 
    'method': 'has_faculty_permissions' 
    },{
    'id': 'import_default_programs', 
    'description': '', 
    'module': 'UWOshOIE.OIE_Utilities', 
    'method': 'import_default_programs' 
    },{
    'id': 'get_attributes', 
    'description': '', 
    'module': 'UWOshOIE.OIE_Utilities', 
    'method': 'get_attributes' 
    },{
    'id': 'get_workflow_state_description', 
    'description': '', 
    'module': 'UWOshOIE.OIE_Utilities', 
    'method': 'get_workflow_state_description'
    },{
    'id': 'url_encode', 
    'description': '', 
    'module': 'UWOshOIE.OIE_Utilities', 
    'method': 'url_encode'
    },{
    'id': 'get_transition_information', 
    'description': '', 
    'module': 'UWOshOIE.OIE_Utilities', 
    'method': 'get_transition_information'
    },{
    'id': 'get_oie_states_ids', 
    'description': '', 
    'module': 'UWOshOIE.OIE_Utilities', 
    'method': 'get_oie_states_ids'
    },{
    'id': 'get_state_info', 
    'description': '', 
    'module': 'UWOshOIE.OIE_Utilities', 
    'method': 'get_state_info'
    },{
    'id': 'get_transition_info', 
    'description': '', 
    'module': 'UWOshOIE.OIE_Utilities', 
    'method': 'get_transition_info'
    },{
    'id': 'yesorno', 
    'description': '', 
    'module': 'UWOshOIE.OIE_Utilities', 
    'method': 'yesorno'
    },{
    'id': 'getFieldSelectionHtmlWidget', 
    'description': '', 
    'module': 'UWOshOIE.MassUpdate', 
    'method': 'getFieldSelectionHtmlWidget'
    },{
    'id': 'getTypeFromFieldName', 
    'description': '', 
    'module': 'UWOshOIE.MassUpdate', 
    'method': 'getTypeFromFieldName'
    },{
    'id': 'getLabelFromFieldName', 
    'description': '', 
    'module': 'UWOshOIE.MassUpdate', 
    'method': 'getLabelFromFieldName'
    },{
    'id': 'getHtmlWidgetFromFieldName', 
    'description': '', 
    'module': 'UWOshOIE.MassUpdate', 
    'method': 'getHtmlWidgetFromFieldName'
    }
]

try:
    from Products.UWOshOIE.AppConfig import *
except ImportError:
    pass

