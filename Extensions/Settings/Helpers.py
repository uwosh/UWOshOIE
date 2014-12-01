from Products.CMFCore.utils import getToolByName
from Globals import DevelopmentMode
from Products.UWOshOIE.config import DEBUG_MODE
from Products.ATVocabularyManager.config import TOOL_NAME as ATVOCABULARYTOOL
from Products.UWOshOIE.content.OIEStudentApplication import OIEStudentApplication
from zLOG import LOG, INFO
from Products.ExternalMethod.ExternalMethod import manage_addExternalMethod

def create_settings_documents(setting, parent):
    
    result = parent.queryCatalog({'portal_type': setting['type_name'], 'id':setting['id']})

    if len(result) == 0:
        parent.invokeFactory(type_name=setting['type_name'], id=setting['id'])
        
        result = parent[setting['id']]
        
        for key in setting.keys():
            if key not in ['id', 'type_name']:
                setattr(result, key, setting[key])

    else:
        result = result[0].getObject()

    result.indexObject()

    if setting.has_key('children'):
        for child in setting['children']:
            create_settings_documents(child, result)

def install_external_method(folder, id, description, module, function):
    if not hasattr(folder, id):
        try:
            manage_addExternalMethod(folder, id, description, module, function)
        except Exception, inst:
            LOG('UWOshOIE install problem:', INFO,  "Adding external method: type: " + str(type(inst)) + 
                                                    ", args: " + str(inst.args) + 
                                                    ", inst: " + str(inst))
            
def install_roles_and_permissions(self, perms):
    role_manager = self.acl_users.portal_role_manager
    portal_groups = self.acl_users.portal_groups
    current_roles = role_manager.listRoleIds()
    current_groups = portal_groups.listGroupIds()
    userdefined_roles = self.userdefined_roles()
    
    for perm in perms:
        if perm['role'] not in current_roles:
            role_manager.addRole(perm['role'], perm['title'], perm['description'])
        if perm['role'] not in userdefined_roles:
            self._addRole(perm['role'])
        if perm['group'] not in current_groups:
            portal_groups.addGroup(perm['group'], roles=[perm['role'],])
        elif perm['group'] not in role_manager.listAssignedPrincipals(perm['role']):
            role_manager.assignRoleToPrincipal(perm['role'], perm['group'])
            
def install_vocabularies(self, vocabs):
    atvm = getToolByName(self, ATVOCABULARYTOOL)
    
    for vkey in vocabs.keys():
        # create vocabulary if it doesnt exist:
        vocabname = vkey
        if not hasattr(atvm, vocabname):
            #print >>out, "adding vocabulary %s" % vocabname
            atvm.invokeFactory('SimpleVocabulary', vocabname)
        vocab = atvm[vocabname]
        if vocabname == 'UWOshOIEMonths' or vocabname == 'UWOshOIEDayOfMonth':
            # for ATVocabularyManager 1.2 which sorts automatically now
            vocab.setSortMethod('sort_method_folder_order')
        if len(vocab.getFolderContents()) < 2:
            for (ikey, value) in vocabs [vkey]:
                if not hasattr(vocab, ikey):
                    vocab.invokeFactory('SimpleVocabularyTerm', ikey)
                    vocab[ikey].setTitle(value)
                    
def add_oie_review_portlet_to_left_slots(portal):
    lslots = list(getattr(portal, 'left_slots', None))
    portletPath = 'here/portlet_uwoshoie_applications_review/macros/portlet'
    if lslots and portletPath not in lslots:
        lslots.insert(0, portletPath)
        portal.left_slots = tuple(lslots)
        
def set_mail_host(portal):

    if DEBUG_MODE or DevelopmentMode:
        from Products.UWOshSecureMailHost.UWOshSecureMailHost import UWOshSecureMailHost
        portal.MailHost = UWOshSecureMailHost()
    else:
        from Products.SecureMailHost.SecureMailHost import SecureMailHost
        portal.MailHost = SecureMailHost()
        
def get_indexes():
    indexes = []
    existing_indexes = [
        'id', 'Title', 'title', 'description', 'effectiveDate', 'allowDiscussion', 'modification_date',
        'creators', 'contributors', 'creation_date', 'expirationDate', 'language', 'rights', 'subject'
    ]
    
    extra_indexes = ['getProgramNameAsString']

    for field in OIEStudentApplication.schema.fields():
        name = field.getName()        

        if name not in existing_indexes:

            getName = 'get' + name[0].upper() + name[1:]            
            label = field.widget.label
            friendlyName = getattr(field, 'friendlyName', None)
            
            if friendlyName != None:
                label = friendlyName
                
            label = 'OIE ' + field.schemata + ": " + label
            value = {
                'name': getName,
                'friendlyName': label,
                'description': field.widget.description,
                'enabled': True
            }
            indexes.append(value)

    indexes.append({
        'name': 'getTransition',
        'friendlyName': 'Transition Name',
        'description': '',
        'enabled': False
    })
    indexes.append({
        'name': 'getSendEmail',
        'friendlyName': 'Send Email?',
        'description': '',
        'enabled': False
    })
    indexes.append({
        'name': 'getSendEmailOnFailure',
        'friendlyName': 'Send Email On Failure?',
        'description': '',
        'enabled': False
    })
    
    return indexes
    
def install_indexes(self):
    atct = getToolByName(self, 'portal_atct')
    ct = getToolByName(self, 'portal_catalog')

    indexes = get_indexes()
    metadatas = get_indexes()
    
    indexes.sort(lambda x, y: x['friendlyName'].upper() > y['friendlyName'].upper())
    metadatas.sort(lambda x, y: x['friendlyName'].upper() > y['friendlyName'].upper())

    for index in indexes:
        if index['name'] not in ct.indexes():
            LOG('UWOshOIE install:', INFO, "Adding index: " + index['name'])
            ct.addIndex(index['name'], 'FieldIndex')
            atct.addIndex(index['name'])

        atct.updateIndex(index['name'], index['friendlyName'], index['description'], index['enabled'])
    
    for meta in metadatas:
        if meta['name'] not in ct.schema():
            LOG('UWOshOIE update:', INFO, "Adding metadata: " + meta['name'])
            ct.addColumn(meta['name'])
            atct.addMetadata(meta['name'])
            
        atct.updateMetadata(meta['name'], meta['friendlyName'], meta['description'], meta['enabled'])
        
def convertBooleansToString(self):
    apps = self.queryCatalog({'portal_type':'OIEStudentApplication'})

    app_ids = [app.id for app in apps]

    for app in apps:
      app = app.getObject()

      fields = [
        'programSpecificMaterialsRequired',
        'specialStudentFormRequired',
        'creditOverloadFormRequired',
        'programSpecificMaterialsRequiredStepIII',
        'metPassportDeadline',
        'attendedOrientation'
      ]

      for f in fields:
          v = getattr(app, f, None)
          
          if v == True:
              setattr(app, f, "Yes")
          elif v == False:
              setattr(app, f, "")
          elif v in ["Yes", "No", ""]:
              pass
          else:
              setattr(app, f, "")
    
