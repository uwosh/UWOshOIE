## Controller Python Script "MASSEDIT_ACTION"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=
##title=
##
emplids = context.REQUEST.get('emplids')
prevPageUrl = context.REQUEST.get('HTTP_REFERER')
homePageUrl = context.portal_url()

#print "request is %s" % context.REQUEST
emplidList = emplids.split('\r\n')
num = len(emplidList)
print "Here are the %s OIE applications for emplids %s:<br><br>" % (num, emplidList)
print "<table border='1'><tr><th>emplid</th><th>application</th><th>edit</th><th>office use only</th><th>office use only (new window)</th></tr>"

pc = context.portal_catalog
for e in emplidList:
    brains = pc.queryCatalog({'getStudentID':e, })
    for brain in brains:
        obj = brain.getObject()
        url = obj.absolute_url()
        fname = obj.getFirstName()
        lname = obj.getLastName()
        editUrl = url + '/edit'
        editOfficeUseOnlyUrl = url + '/atct_edit?fieldset=OFFICE%20USE%20ONLY'
        link = "<a href='%s'>%s %s</a>" % (url, fname, lname)
        editLink = "<a href='%s'>edit</a>" % editUrl
        editOfficeOnlyLink = "<a href='%s'>office use only</a>" % editOfficeUseOnlyUrl
        editOfficeOnlyNewWindowLink = "<a href='%s' target='#'>office use only (new window)</a>" % editOfficeUseOnlyUrl
        print "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (e, link, editLink, editOfficeOnlyLink, editOfficeOnlyNewWindowLink)
print "</table>"

print "<br><br><a href='%s'>[return to the form]</a>" % prevPageUrl
print "<br><br><a href='%s'>[return to the home page]</a>" % homePageUrl
return printed

# (Optional) set the default next action (this can be overridden
# in the script's actions tab in the ZMI).
#state.setNextAction('redirect_to:python:portal_url')

# Always make sure to return the ControllerState object
#return state