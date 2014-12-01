## Controller Python Script "oieMassUpdateDoUpdates"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=
##title=
##
from DateTime import DateTime

objectIds = context.REQUEST.get('objectIds')
fieldName = context.REQUEST.get('fieldName')
value = context.REQUEST.get('value')

objectIds = [objectIds]

label = context.getLabelFromFieldName(fieldName)
type = context.getTypeFromFieldName(fieldName)

if type == 'BooleanField':
   value = str(value) == 'True'
elif type == 'DateTimeField':
   value = DateTime(value)
else:
   value = str(value)

for objectId in objectIds:
    brains = context.portal_catalog.queryCatalog({'id':objectId, })

    for brain in brains:
        obj = brain.getObject()
	field = obj.getField(fieldName)
        fieldMutator = field.getMutator(obj)
        fieldMutator(value)
	obj.reindexObject()

return state