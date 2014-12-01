# A huge thank you to Andreas Jung (lists@zopyx.com)!

import commands
import types
import difflib

from AccessControl import getSecurityManager
from Acquisition import aq_base, aq_inner
from DateTime.DateTime import DateTime
from Products.CMFCore.utils import getToolByName

import transaction
#from logger import CHANGES_LOG as LOG
from zLOG import LOG, INFO, WARNING, ERROR
#from squid import purgeFromCache

# don't autolog changes for these fields
IGNORED_FIELDS = ('modification_date',)

# email address to receive alerts of value changes
DEFAULT_EMAIL_ALERT_RECIPIENT = 'oie@uwosh.edu'

class CommitHandler:
   """ a handler to detect and log changes for AT-related content """

   def __init__(self):
       self.d = {}
       self.instance = None

   def setInstance(self, instance):
       self.instance = instance

       # first we store all 'old' values
       for field in instance.Schema().fields():
           v = getattr(instance, field.accessor)()
           self.d[field.getName()] = v

   def __call__(self, *args, **kw):
       """ this is called before the commit but after the modification
           of the field data
       """

       # Notify only if it's an OIE Student Application in a state other than private and
       #    the changes were done to student-revisable fields.
       typeName = self.instance.archetype_name
       if not typeName or typeName <> 'OIE Student Application':
          return
       wf_tool = getToolByName(self.instance, 'portal_workflow', None)
       if wf_tool:
          state = wf_tool.getInfoFor(self.instance,'review_state',None)
          if state == 'private':
             return

       now = DateTime()
       username = getSecurityManager().getUser().getUserName()

       # look for changes
       changes = []
       for field in self.instance.Schema().fields():

           # skip fields that are not revisable by the student
           if field.getName() in IGNORED_FIELDS or field.write_permission <> 'UWOshOIE: Modify revisable fields':
               continue

           v = getattr(self.instance, field.accessor)()

           if v != self.d[field.getName()]:
               field_name = field.getName()
               field_type = field.getType().split('.')[-1] # dotted name

               if field_type in ('StringField', 'LinesField', 'IntField', 'BooleanField',
                                 'DateTimeField', 'DateRangesField', 'DayInMonthTimeRangeField', 'DayOfWeekTimeRangeField'):
                   changes.append((field_name, self.d[field_name], v))

               elif field_type in ('TextField',):
                   old_lines = self.d[field_name].split('\n')
                   new_lines = v.split('\n')
                   diff_lines = difflib.ndiff(old_lines, new_lines, difflib.IS_LINE_JUNK, difflib.IS_CHARACTER_JUNK)
                   changes.append((field_name, '', '\n'.join(diff_lines)))

               elif field_type in ('ImageField', 'FileField'):
                   continue

               elif field_type in ('ReferenceField',):

                   def _checkListType(inp):
                       if type(inp) not in (types.ListType, types.TupleType):
                           return [inp, ]
                       return inp

                   old_refs = [o.absolute_url(1) for o in _checkListType(self.d[field_name]) if o != None]
                   new_refs = [o.absolute_url(1) for o in _checkListType(v) if o != None]
                   changes.append((field_name, old_refs, new_refs))

               else:
                   #LOG.warn('Unhandled Field: %s %s' % (field, field.getType()))
                   LOG ("CommitHandler", WARNING, 'Unhandled Field: %s %s' % (field, field.getType()))

       if changes:
           #LOG.info('-'*60)
           LOG("CommitHandler", INFO, '-'*60)
           #LOG.info('%s(%s): %s' % (username,
           #                         self.instance.REQUEST.getClientAddr(),
           #                         self.instance.absolute_url(1)))
           LOG ("CommitHandler", INFO, '%s(%s): %s' % (username,
                                    self.instance.REQUEST.getClientAddr(),
                                    self.instance.absolute_url(1)))
           changeString = ""
           for key, old, new in changes:
               #LOG.info('%s: %s -> %s' % (key, old, new))
               changeStringLine = '%s: %s -> %s' % (key, old, new)
               LOG ("CommitHandler", INFO, changeStringLine)
               changeString += changeStringLine + "\n"

           self._sendChangeNotificationMessage(self.instance, changeString)


   def _sendChangeNotificationMessage(self, obj, changeString, **kw):
       portal = getToolByName(obj, 'portal_url').getPortalObject()

       mTo = DEFAULT_EMAIL_ALERT_RECIPIENT
       mFrom = "OIE Portal Change Notifier <%s>" % portal.email_from_address
       mSubj = 'Study abroad application revisable field change notification'

       mMsg = "The study abroad application has had changes to its revisable fields.\n\n"
       mMsg += "You can view the application here:  " + obj.absolute_url() + "\n\n"
       mMsg += "The following changes were made:\n\n" + changeString

       portal.MailHost.secureSend(mMsg, mTo, mFrom, mSubj)


################################################################
# AT/ATCT monkeys
################################################################

def post_validate(self, REQUEST, errors):
   """ hook into AT(CT) to intercept edit operations to provide
       logging for changed data.
   """

   T = transaction.get()
   CH = CommitHandler()
   CH.setInstance(self)
   T.beforeCommitHook(CH)

   return self._post_validate(REQUEST, errors)


from Products.ATContentTypes.content.base import ATCTContent, ATCTFileContent
ATCTFileContent._post_validate = ATCTFileContent.post_validate
ATCTFileContent.post_validate = post_validate

ATCTContent._post_validate = ATCTContent.post_validate
ATCTContent.post_validate = post_validate

from Products.Archetypes.public import OrderedBaseFolder, BaseContent
OrderedBaseFolder._post_validate = OrderedBaseFolder.post_validate
OrderedBaseFolder.post_validate = post_validate
BaseContent._post_validate = BaseContent.post_validate
BaseContent.post_validate = post_validate
