from Products.CMFCore.utils import getToolByName
from Products.ExternalMethod.ExternalMethod import ExternalMethod
from DateTime import DateTime


def installWorkflows(self, package, out):
    """Install the custom workflows for this product.
    """

    productname = 'UWOshOIE'
    workflowTool = getToolByName(self, 'portal_workflow')

    ourProductWorkflow = ExternalMethod('temp', 'temp',
                         productname+'.'+'OIEStudentApplicationWorkflow',
                         'create_OIEStudentApplicationWorkflow')
    workflow = ourProductWorkflow('OIEStudentApplicationWorkflow')
    workflowTool._setObject('OIEStudentApplicationWorkflow', workflow)
    workflowTool.setChainForPortalTypes(['OIEStudentApplication'], workflow.getId())
    
    ourProductWorkflow = ExternalMethod('temp',
                         'temp',
                         productname+'.'+'UWOshOIEProgramWorkflow',
                         'create_UWOshOIEProgramWorkflow')
    workflow = ourProductWorkflow('UWOshOIEProgramWorkflow')
    workflowTool._setObject('UWOshOIEProgramWorkflow', workflow)
    workflowTool.setChainForPortalTypes(['UWOshOIEProgram'], workflow.getId())
    workflowTool.setChainForPortalTypes(['UWOshOIEEmailTemplate'], workflow.getId())

    return workflowTool
