from Products.ATContentTypes.content.topic import ATTopic
from Products.UWOshOIE.config import PROJECTNAME
from Products.ATContentTypes.content.base import registerATCT
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.PloneBatch import Batch
import copy


# Override ATTopic inandoutwidget
UWOshOIESmartFolderSchema = copy.deepcopy(ATTopic.schema)
topic_fields = UWOshOIESmartFolderSchema.fields()

for field in topic_fields:
    if field.getName() == 'customViewFields':
        field.widget.macro = "oie_inandout"
        field.widget.label = "Fields To Select"
    elif field.getName() == 'customView':
        field.default = True

class UWOshOIESmartFolder(ATTopic):
    schema         =  UWOshOIESmartFolderSchema
    
    meta_type      = 'UWOshOIESmartFolder'
    portal_type    = 'UWOshOIESmartFolder'
    archetype_name = 'OIE Smart Folder'
    allowed_content_types = ('UWOshOIESmartFolder',)
    
    default_view = "oie_smart_folder_view"

    #add default OIE Student Application type criteron on creation
    def __init__(self, id):
        self.id = id
        self.addCriterionAndSetValue('Type', 'ATPortalTypeCriterion', 'OIEStudentApplication')
        
    def addCriterionAndSetValue(self, field, criterion_type, value):
        criterion = self.addCriterion(field, criterion_type)
        criterion.value = (u'OIE Student Application',)
        
    #Override queryCatalog method so it checks if they are querying for programName
    def queryCatalog(self, REQUEST=None, batch=False, b_size=None,
                                                full_objects=False, **kw):
        """Invoke the catalog using our criteria to augment any passed
            in query before calling the catalog.
        """
        program_name = False
        operator = "and"

        if REQUEST is None:
            REQUEST = getattr(self, 'REQUEST', {})
        b_start = REQUEST.get('b_start', 0)

        q = self.buildQuery()
        if q is None:
            # empty query - do not show anything
            if batch:
                return Batch([], 20, int(b_start), orphan=0)
            return []
        elif q.has_key('getProgramName'):
            operator = q['getProgramName']['operator']
            program_name = q['getProgramName']['query']
            del(q['getProgramName'])
        
        # Allow parameters to further limit existing criterias
        for k,v in q.items():
            if kw.has_key(k):
                arg = kw.get(k)
                if isinstance(arg, (ListType,TupleType)) and isinstance(v, (ListType,TupleType)):
                    kw[k] = [x for x in arg if x in v]
                elif isinstance(arg, StringType) and isinstance(v, (ListType,TupleType)) and arg in v:
                    kw[k] = [arg]
                else:
                    kw[k]=v
            else:
                kw[k]=v
        #kw.update(q)
        pcatalog = getToolByName(self, 'portal_catalog')
        limit = self.getLimitNumber()
        max_items = self.getItemCount()
        # Batch based on limit size if b_szie is unspecified
        if max_items and b_size is None:
            b_size = int(max_items)
        else:
            b_size = b_size or 20
        if not batch and limit and max_items and self.hasSortCriterion():
            # Sort limit helps Zope 2.6.1+ to do a faster query
            # sorting when sort is involved
            # See: http://zope.org/Members/Caseman/ZCatalog_for_2.6.1
        
            # kw.setdefault('sort_limit', max_items)
            pass
        __traceback_info__ = (self, kw,)
        results = pcatalog.searchResults(REQUEST, **kw)
    
        #if searching per program, limit results
        if program_name:
            newResults = results
            results = []
            for result in newResults:
                if result.getProgramName and result.getProgramName.Title() in program_name:
                    results.append(result)
    
        if full_objects and not limit:
            results = [b.getObject() for b in results]

        if batch:
            batch = Batch(results, b_size, int(b_start), orphan=0)
            return batch
        if limit:
            if full_objects:
                return [b.getObject() for b in results[:max_items]]
            return results[:max_items]
    
        return results


    def get_value(self, value):
        try:
            return value.Title()
        except:
            return value

    def cut_colon_out(self, value):
        value = value.split(':')
        if len(value) > 1:
            return value[1]
        else:
            return value[0]        

registerATCT(UWOshOIESmartFolder, PROJECTNAME)