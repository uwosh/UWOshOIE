from AccessControl import Unauthorized
from Products.CMFPlone.utils import transaction_note
from Products.CMFPlone import PloneMessageFactory as _
from Products.CMFCore.utils import getToolByName

oie_application_id = context.REQUEST.get('oie_application_id')
transition_id = context.REQUEST.get('transition_id')
#oie_app = context.queryCatalog({'portal_type': 'OIEStudentApplication', 'id': oie_application_id})

oie_app = context[oie_application_id]

if oie_app:
    portal_workflow = getToolByName(context, 'portal_workflow')
    portal_workflow.doActionFor(oie_app, transition_id)
else:
    raise ValueError, "Error trying to perform action '%s' on application id '%s'" %(transition_id, oie_application_id)

state.setNextAction ('redirect_to:string:' + oie_app.absolute_url())

return state
