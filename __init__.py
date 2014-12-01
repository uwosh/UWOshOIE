#
# Initialise the product's module. There are three ways to inject custom code
# here:
#
#   - To set global configuration variables, create a file AppConfig.py. This
#       will be imported in config.py, which in turn is imported in each
#       generated class and in this file.
#   - To perform custom initialisation after types have been registered, use
#       the protected code section at the bottom of initialize().
#   - To register a customisation policy, create a file CustomizationPolicy.py
#       with a method register(context) to register the policy
#

from zLOG import LOG, INFO

LOG('UWOshOIE',INFO, 'Installing Product')

try:
    import CustomizationPolicy
except ImportError:
    CustomizationPolicy=None

from Globals import package_home
from Products.CMFCore import utils, CMFCorePermissions, DirectoryView
from Products.CMFPlone.PloneUtilities import ToolInit
from Products.Archetypes.public import *
from Products.Archetypes import listTypes
from Products.Archetypes.utils import capitalize
import os, os.path
from Products.UWOshOIE.config import *
from Products.UWOshOIE import validators

DirectoryView.registerDirectory('skins', product_globals)
DirectoryView.registerDirectory('skins/UWOshOIE', product_globals)


def initialize(context):
    # imports packages and types for registration
    from Products.validation import validation
    validation.register(validators.ReferenceValidator('ReferenceValidator'))
    validation.register(validators.isValidYearValidator('isValidYearValidator'))
    validation.register(validators.isDifficultToWalkValidator('isDifficultToWalkValidator'))
    validation.register(validators.orientationSession2hoursValidator('orientationSession2hoursValidator'))
    validation.register(validators.orientationSession2DateValidator('orientationSession2DateValidator'))
    validation.register(validators.orientationConflictDateValidator('orientationConflictDateValidator'))
    validation.register(validators.financialAidValidator('financialAidValidator'))
    
    import content

    # initialize portal content
    content_types, constructors, ftis = process_types(
        listTypes(PROJECTNAME),
        PROJECTNAME)

    utils.ContentInit(
        PROJECTNAME + ' Content',
        content_types      = content_types,
        permission         = DEFAULT_ADD_CONTENT_PERMISSION,
        extra_constructors = constructors,
        fti                = ftis,
        ).initialize(context)

    # apply customization-policy, if theres any
    if CustomizationPolicy and hasattr(CustomizationPolicy, 'register'):
        CustomizationPolicy.register(context)
        print 'Customization policy for UWOshOIE installed'

