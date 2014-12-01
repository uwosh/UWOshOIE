## Script (Python) "create-application"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
## Errors:
##  invalid syntax (create-application, line 17)
##
# Import a standard function, and get the HTML request and response objects.
from Products.PythonScripts.standard import html_quote

from Products.CMFCore.utils import getToolByName

request = container.REQUEST
RESPONSE =  request.RESPONSE

pm = context.portal_membership
member = pm.getAuthenticatedMember()
homeFolder = pm.getHomeFolder()
theTime = str(int(context.ZopeTime()))
appId = 'oiestuapp_' + member.getId() + theTime
homeFolder.invokeFactory("OIEStudentApplication", appId)
msg = "A new OIE application has been created for you.  You may now fill in the details by clicking on the purple 'Edit application' button below." 
RESPONSE.redirect("%s/%s?portal_status_message=%s" % (homeFolder.absolute_url(), appId, msg))
