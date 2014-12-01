
from Products.CMFCore.utils import getToolByName
from Products.UWOshOIE.Extensions.Settings.Vocabularies import *
from Products.UWOshOIE.Extensions.Settings.EmailTemplates import *
from Products.UWOshOIE.Extensions.Settings import Helpers
from Products.UWOshOIE.Extensions.Settings.ProgramsAndFacultyLeaders import *
from Products.UWOshOIE.Extensions.Settings.RolesAndGroups import perms
from zLOG import LOG, INFO, ERROR, WARNING
from Products.UWOshOIE.config import DEFAULT_NOTIFICATION_EMAIL_ADDRESS, OIE_FROM_NAME, PORTAL_TITLE, EXTERNAL_METHODS

def install(self):

    portal = getToolByName(self, 'portal_url').getPortalObject()

    # Set common portal properties
    portal.title = PORTAL_TITLE
    portal.email_from_address = DEFAULT_NOTIFICATION_EMAIL_ADDRESS
    portal.email_from_name = OIE_FROM_NAME
    
    csstool = getToolByName (self, "portal_css")
    csstool.registerStylesheet ('uwoshoie.css')
    
    #Helpers.install_vocabularies(self, Vocabularies)
    #Helpers.add_oie_review_portlet_to_left_slots(portal)

    # XXX: This was commented out. May want to comment out again before releasing?
    # Only potential problem is that it might override something on the server.
    # But this method call is needed to set stuff up. Tests wont run without it!
    Helpers.install_roles_and_permissions(self, perms)
    
    Helpers.install_indexes(self)
    
    #NOT WORKING CORRECTLY!  Overriding settings
    #Helpers.create_settings_documents(settings_folder, portal)

    custom_folder = portal.portal_skins.custom
    for external_method in EXTERNAL_METHODS:
        Helpers.install_external_method(custom_folder, 
                                        external_method['id'], 
                                        external_method['description'], 
                                        external_method['module'], 
                                        external_method['method'])
    
    Helpers.convertBooleansToString(self)
    
def uninstall(self):
    pass
