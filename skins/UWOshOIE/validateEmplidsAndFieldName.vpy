## Controller Validator "validateEmplidsAndFieldName"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=
##title=
##
emplids = context.REQUEST.get('emplids', None)
fieldName = context.REQUEST.get('fieldName', None)

if not emplids:
   state.setError('emplids', 'Please enter at least one emplid')
else:   
   emplidsList = emplids.split('\r\n')
   emplidsList = filter(lambda x: x != '', map(lambda x: x.strip(), emplidsList))

   if not emplidsList or (not reduce(lambda x, y: len(y) == 7 and y.isdigit() and x, emplidsList, True)):
      state.setError('emplids', 'All emplids must be 7 digit numbers')

if not fieldName:
   state.setError('fieldName', 'Please select a valid field name')

if state.getErrors():
   state.setStatus('failure')

return state