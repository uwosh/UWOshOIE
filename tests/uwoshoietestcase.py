
# Import the base test case classes
from Testing import ZopeTestCase
from Products.CMFPlone.tests import PloneTestCase
from unittest import TestCase, TestSuite, makeSuite, main
from Products.CMFCore.WorkflowCore import WorkflowException
from Products.UWOshOIE.Extensions.Settings.EmailTemplates import *
from Products.UWOshOIE.Extensions.Settings.Helpers import create_settings_documents

# These must install cleanly
ZopeTestCase.installProduct('ATVocabularyManager')
ZopeTestCase.installProduct('UWOshOIE')

# Set up the Plone site used for the test fixture. The PRODUCTS are the products
# to install in the Plone site (as opposed to the products defined above, which
# are all products available to Zope in the test fixture)
PRODUCTS = ['ATVocabularyManager', 'UWOshOIE']
PloneTestCase.setupPloneSite(products=PRODUCTS)

class MockMailHost:
    """
    Fake MailHost so we don't have problem when scripts try to send mail
    """
    def __init__(self, *args, **kwargs):
        self.to = []
        self.fromWho = []
        self.message = []
        self.subject = []
        self.count = 0

    def secureSend(self, mMsg, mTo, mFrom, mSubj):
        self.to.append(mTo)
        self.fromWho.append(mFrom)
        self.message.append(mMsg)
        self.subject.append(mSubj)
        self.count += 1
        
    def getTo(self):
        return self.to[0]
    
    def getFrom(self):
        return self.fromWho[0]
        
    def getMessage(self):
        return self.message[0]
        
    def getSubject(self):
        return self.subject[0]
    
    def getToIterator(self):
        for to in self.to:
            yield to
            
    def getFromIterator(self):
        for f in self.fromWho:
            yield f
            
    def getMessageIterator(self):
        for message in self.message:
            yield message
        
    def getSubjectIterator(self):
        for subject in self.subject:
            yield subject
            
    def getEmailCount(self):
        return self.count
        
    def clearEmails(self):
        self.to = []
        self.fromWho = []
        self.message = []
        self.subject = []
        self.count = 0


class UWOshOIETestCase(PloneTestCase.PloneTestCase):
    """
    Base
    """
    _oie_users = {'director':['UWOshOIEDirector'],  'front_line_advisor':['UWOshOIEFrontLineAdvisor'], 
                    'program_manager':['UWOshOIEProgramManager'], 'fac_review':['UWOshOIEFacReview'], 'financial_aid':['UWOshOIEFinAid']}
    _default_user = 'student'
    
    _all_users = _oie_users.keys() + [_default_user]
    _default_program = None
    
    def afterSetUp(self):
        self.acl_users = self.portal.acl_users
        self.portal_workflow = self.portal.portal_workflow
        self.portal_registration = self.portal.portal_registration
        
        self.mockMailHost()
        self.setDefaultProgram()
        self.createUsers()
        
        self.login()
        self.setRoles(('Manager', 'Owner'))
        create_settings_documents(settings_folder, self.portal)
        self.logout()
        
    def setDefaultProgram(self):
        self.login()
        self.setRoles(('Manager', 'Owner'))
        
        programId = self.portal.invokeFactory(  type_name='UWOshOIEProgram', 
                                                            id=self.portal.generateUniqueId(), 
                                                            title="test", 
                                                            facultyLeaders=['someone', 'another'])
        
        self._default_program = self.portal[programId]
        self.logout()
    
    def createUsers(self):
        self.login()
        self.setRoles(('Manager', 'Owner'))
         
        self.portal.acl_users._doAddUser(self._default_user, 'password', ['Member', 'Owner'], [])
        self.portal.portal_membership.getMemberById(self._default_user).setMemberProperties({'email': self._default_user + '@oie.com'})
        
        for user, roles in self._oie_users.iteritems():
            self.portal.acl_users._doAddUser(user, 'password', roles, [])
            self.portal.portal_membership.getMemberById(user).setMemberProperties({'email': user + '@oie.com'})
        
        self.logout()
        
    def mockMailHost(self):
         self.portal.MailHost = MockMailHost()
        
    def assertHasTheseRoles(self, transition, roles):
        map(lambda role: self.failUnless(role in roles ), transition.getGuard().roles)
        self.failUnless(len(roles) == len(transition.getGuard().roles))
        
    def hasTheseTransitions(self, state, desiredTransitions):
        map(lambda transition: self.failUnless(transition in desiredTransitions ), state.getTransitions())
        self.failUnless(len(desiredTransitions) == len(state.getTransitions()))

    def hasPermissionRoles(self, state, permission, desired_roles):
        for role in state.getPermissionInfo(permission)['roles']:
            self.failUnless(role in desired_roles)
    
    def fill_out_application(self, app):
        app.setFirstName("John")
        app.setLastName("Doe")
        app.setEmail("applicant@uwosh.edu")
        app.setLocalAddr1("1234 address")
        app.setLocalPhone("555-555-5555")
        app.setHomePhone("555-555-5555")
        app.setHomeAddr1("Some Home Address")
        app.setHomeCity("Oshkosh")
        app.setHomeState("WI")
        app.setHomeZip("54115")
        app.setCitizenship("U.S. Citizen")
        app.setStateResidency("Wisconsin")
        app.setDateOfBirth_month("December")
        app.setDateOfBirth_day(2)
        app.setPlaceOfBirth("Oshkosh")
        app.setQuestionAcadCareerPlan("Some Plane")
        app.setQuestionLangCulturalSkills("Cultural Skills")
        app.setQuestionPrevTravel("Previous Travel")
        app.setQuestionWorkExp("Work Exp")
        app.setDoctorLastname("Jones")
        app.setDoctorFirstname("Bob")
        app.setDoctorPhone("546-567-6575")
        app.setMedicalInsuranceCompany("Company")
        app.setMedicalPolicyHolder("policy holder")
        app.setMedicalPolicyGroupNumber("group number")
        app.setHasDifficultyWalking("Yes")
        app.setMedicalReadStatement("Yes")
        app.setMedicalAccessOK("Yes")
        app.setSmokingPreferred("NO")
        app.setIsVegetarian("NO")
        app.setEmerg1name("nam")
        app.setEmerg1addr1("address")
        app.setEmerg1state("state")
        app.setCertification("Yes")
        app.setEmerg1city("city")
        app.setEmerg1zip("45345")
        app.setEmerg1country("USA")
        app.setEmerg1homePhone("555-555-5555")
        app.setProgramName(self._default_program)
        app.setProgramSemester("Semester")
        app.setStudentType("Type")
        app.setWillTakeBus("Yes")
        app.setWillFlyWithGroup("Yes")
        app.setAgreeToCosts("Yes")
        app.setOrientationConflict("NO")
        app.setSubject1("English")
        app.setCourse1("Course")
        app.setApplyForAid("NO")
        app.setQuestionExpectations("lsdkfnsdk")
        app.setAwareOfAllMaterials("Yes")
        app.setUWOshkoshRelease("Yes")
        app.setGraduationMonth(4)
        app.setOrientationDate1("2009-01-01")
        app.setOrientationHours1("9am - 1pm")
        app.setMedicalOK(True)
        app.setPassportOK(True)
        app.setDepositOnTime(True)
        app.setCompletionDate('2009-10-10')
        app.setProgramYear(2009)
        app.setProgramSpecificMaterialsRequired('No')
        app.setSpecialStudentFormRequired('No')
        app.setCreditOverloadFormRequired('No')
   
    def getState(self, obj):
        return self.portal_workflow.getInfoFor(obj, 'review_state', None)
        
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(UWOshOIETestCase))
    return suite
    
if __name__ == '__main__':
    framework()
