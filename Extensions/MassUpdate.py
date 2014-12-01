from Products.UWOshOIE.content.OIEStudentApplication import OIEStudentApplication

schema = OIEStudentApplication.schema
fields = schema.fields()

def fieldsListToHtml(fieldsList):
    html = '<select name="fieldName">\n'
    for (name, label) in fieldsList:
        html += '<option value="%s">%s</option>\n' % (name, label)

    html += '</select>\n'
    return html

def getFieldSelectionHtmlWidget():
    fieldsList = []
    for field in fields:
        if field.schemata == 'OFFICE USE ONLY':
            name = field.getName()
            label = field.widget.label
            fieldsList.append((name, label))

    return fieldsListToHtml(fieldsList)

def getTypeFromFieldName(fieldName):
    field = schema[fieldName]
    type = field.getType()
    return type.split('.')[-1]

def getLabelFromFieldName(fieldName):
    field = schema[fieldName]
    widget = field.widget
    return widget.label

def getHtmlWidgetFromFieldName(fieldName):
    field = schema[fieldName]
    widget = field.widget
    widgetName = widget.getName()

    html = ''

    if widgetName == 'SelectionWidget':
        html = '<select name="value">'
        for v in field.vocabulary:
            html += '<option value="%s">%s</option>' % (v, v)
        html += '</select>'

    elif widgetName == 'BooleanWidget':
        html = '<input type="checkbox" name="value" value="True" />'

    elif widgetName == 'TextAreaWidget':
        html = '<textarea rows="5" cols="40" name="value"></textarea>'

    elif widgetName == 'CalendarWidget':
        html = '<input type="text" name="value" /><span> (YYYY/MM/DD)</span>'

    else:
        html = '<input type="text" name="value" />'

    return '%s: %s' % (widget.label, html)
