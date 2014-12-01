## Controller Validator "validateValueField"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=
##title=
##
fieldName = context.REQUEST.get('fieldName', None)
value = context.REQUEST.get('value', None)

type = context.getTypeFromFieldName(fieldName)

if type == 'DateTimeField':
   if value and value.count('/') == 2:
      (year, month, day) = value.split('/')
      if not (year.isdigit() and month.isdigit() and day.isdigit() and int(year) > 1900 and (1 <= int(month) <= 12) and (1 <= int(day) <= 31)):
         state.setError('value', 'Please enter a date formatted as: YYYY/MM/DD')
   else:
      state.setError('value', 'Please enter a date formatted as: YYYY/MM/DD')

elif type == 'IntegerField':
   if not value or not value.isdigit():
      state.setError('value', 'Please enter an integer')

elif type == 'FloatField':
   try:
      float(value)
   except:
      state.setError('value', 'Please enter a decimal number')

if state.getErrors():
   state.setStatus('failure')

return state