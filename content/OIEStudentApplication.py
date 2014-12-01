# File: OIEStudentApplication.py
# 
# Copyright (c) 2007 by 
# Generator: ArchGenXML Version 1.4.0-RC1 
#            http://plone.org/products/archgenxml
#
# GNU General Public Licence (GPL)
# 
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 59 Temple
# Place, Suite 330, Boston, MA  02111-1307  USA
#
__author__  = '''Nathan Van Gheem'''
__docformat__ = 'plaintext'


from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from Products.validation.validators import ExpressionValidator
from Products.ATVocabularyManager.namedvocabulary import NamedVocabulary
from Products.UWOshOIE.config import *
from Products.CMFCore.utils import getToolByName
from zLOG import LOG, INFO, WARNING, ERROR
from time import ctime
from Products.UWOshOIE import validators
from Products.ATContentTypes.content.base import ATCTContent
from Products.ATContentTypes.lib.historyaware import HistoryAwareMixin
from Acquisition import aq_inner
from Acquisition import aq_parent
from Products.UWOshOIE.widgets import YesNoField, YesNoWidget

schema=Schema((
    StringField('title',
        widget=StringWidget(
            label="Application Title",
            description="optional",
            label_msgid='UWOshOIE_label_title',
            description_msgid='UWOshOIE_help_title',
            i18n_domain='UWOshOIE',
        ),
        read_permission="UWOshOIE: Modify Office Use Only fields",
        write_permission="Manage portal",
        accessor="Title"
    ),

    StringField('description',
        widget=StringWidget(
            visible=0,
            label='Description',
            label_msgid='UWOshOIE_label_description',
            description_msgid='UWOshOIE_help_description',
            i18n_domain='UWOshOIE',
        ),
        accessor="Description",
        searchable=True
    ),

    StringField('studentID',
        widget=StringWidget(
            description="(if applicable)",
            label="UW Oshkosh Student ID",
            label_msgid='UWOshOIE_label_studentID',
            description_msgid='UWOshOIE_help_studentID',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify normal fields",
        searchable=True,
        validators=[u"inNumericRange(value, 0, 9999999)"]
    ),

    StringField('firstName',
        widget=StringWidget(
            label="First Name",
            label_msgid='UWOshOIE_label_firstName',
            description_msgid='UWOshOIE_help_firstName',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify normal fields",
        required=1,
        searchable=True
    ),

    StringField('middleName',
        widget=StringWidget(
            label="Middle Name",
            label_msgid='UWOshOIE_label_middleName',
            description_msgid='UWOshOIE_help_middleName',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify normal fields",
        searchable=True
    ),

    StringField('lastName',
        widget=StringWidget(
            label="Last Name",
            label_msgid='UWOshOIE_label_lastName',
            description_msgid='UWOshOIE_help_lastName',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify normal fields",
        required=1,
        searchable=True
    ),

    StringField('email',
        widget=StringWidget(
            label="Email Address",
            description="UW Oshkosh students must use a @uwosh.edu email address.  Acceptable email addresses for other applicants include school and company addresses.",
            label_msgid='UWOshOIE_label_email',
            description_msgid='UWOshOIE_help_email',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify normal fields",
        required=1,
        searchable=True,
        validators=[u'isEmail'],
        default_method="getMemberEmail",
    ),

    StringField('localAddr1',
        widget=StringWidget(
            label="Local Address Line 1",
            label_msgid='UWOshOIE_label_localAddr1',
            description_msgid='UWOshOIE_help_localAddr1',
            i18n_domain='UWOshOIE',
        ),
        required=1,
        write_permission="UWOshOIE: Modify revisable fields",
        schemata="Addresses",
        searchable=True
    ),
    
    StringField('localAddr2',
        widget=StringWidget(
            label="Local Address Line 2",
            label_msgid='UWOshOIE_label_localAddr2',
            description_msgid='UWOshOIE_help_localAddr2',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify revisable fields",
        schemata="Addresses",
        searchable=True
    ),

    StringField('localCity',
        default="Oshkosh",
        widget=StringWidget(
            label="Local City",
            label_msgid='UWOshOIE_label_localCity',
            description_msgid='UWOshOIE_help_localCity',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify revisable fields",
        schemata="Addresses",
        required=1,
        searchable=True
    ),

    StringField('localState',
        default="WI",
        widget=StringWidget(
            label="Local State",
            label_msgid='UWOshOIE_label_localState',
            description_msgid='UWOshOIE_help_localState',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify revisable fields",
        schemata="Addresses",
        required=1,
        searchable=True
    ),

    StringField('localZip',
        default="54901",
        widget=StringWidget(
            label="Local Zip Code",
            label_msgid='UWOshOIE_label_localZip',
            description_msgid='UWOshOIE_help_localZip',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify revisable fields",
        schemata="Addresses",
        required=1,
        searchable=True
    ),

    StringField('localCountry',
        default="USA",
        widget=StringWidget(
            label="Local Country",
            label_msgid='UWOshOIE_label_localCountry',
            description_msgid='UWOshOIE_help_localCountry',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify revisable fields",
        schemata="Addresses",
        required=1,
        searchable=True
    ),

    StringField('localPhone',
        widget=StringWidget(
            label="Local Telephone",
            description="Please include country code (if outside US) and area code",
            label_msgid='UWOshOIE_label_localPhone',
            description_msgid='UWOshOIE_help_localPhone',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify revisable fields",
        schemata="Addresses",
        required=1,
        searchable=True
    ),

    StringField('mobilePhone',
        widget=StringWidget(
            label="Mobile (cell) phone",
            description="Please include country code (if outside US) and area code",
            label_msgid='UWOshOIE_label_mobilePhone',
            description_msgid='UWOshOIE_help_mobilePhone',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify revisable fields",
        schemata="Addresses",
        searchable=True
    ),

    StringField('homeAddr1',
        widget=StringWidget(
            label="Home Address Line 1",
            label_msgid='UWOshOIE_label_homeAddr1',
            description_msgid='UWOshOIE_help_homeAddr1',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify revisable fields",
        schemata="Addresses",
        required=1,
        searchable=True
    ),

    StringField('homeAddr2',
        widget=StringWidget(
            label="Home Address Line 2",
            label_msgid='UWOshOIE_label_homeAddr2',
            description_msgid='UWOshOIE_help_homeAddr2',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify revisable fields",
        schemata="Addresses",
        searchable=True
    ),

    StringField('homeCity',
        widget=StringWidget(
            label="Home City",
            label_msgid='UWOshOIE_label_homeCity',
            description_msgid='UWOshOIE_help_homeCity',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify revisable fields",
        schemata="Addresses",
        required=1,
        searchable=True
    ),

    StringField('homeState',
        widget=StringWidget(
            label="Home State",
            label_msgid='UWOshOIE_label_homeState',
            description_msgid='UWOshOIE_help_homeState',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify revisable fields",
        schemata="Addresses",
        required=1,
        searchable=True
    ),

    StringField('homeZip',
        widget=StringWidget(
            label="Home Zip Code",
            label_msgid='UWOshOIE_label_homeZip',
            description_msgid='UWOshOIE_help_homeZip',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify revisable fields",
        schemata="Addresses",
        required=1,
        searchable=True
    ),

    StringField('homeCountry',
        default="USA",
        widget=StringWidget(
            label="Home Country",
            label_msgid='UWOshOIE_label_homeCountry',
            description_msgid='UWOshOIE_help_homeCountry',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify revisable fields",
        schemata="Addresses",
        required=1,
        searchable=True
    ),

    StringField('homePhone',
        widget=StringWidget(
            label="Home Telephone",
            description="Please include country code (if outside US) and area code",
            label_msgid='UWOshOIE_label_homePhone',
            description_msgid='UWOshOIE_help_homePhone',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify revisable fields",
        schemata="Addresses",
        required=1,
        searchable=True
    ),

    StringField('citizenship',
        widget=SelectionWidget(
            label='Citizenship',
            label_msgid='UWOshOIE_label_citizenship',
            description_msgid='UWOshOIE_help_citizenship',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify normal fields",
        required=1,
        schemata="Demographics",
        vocabulary=['U.S. Citizen','Permanent U.S. Resident','Other Citizenship'],
        searchable=True
    ),

    StringField('citizenshipOther',
        widget=StringWidget(
            label="Enter country of citizenship if you selected Other",
            label_msgid='UWOshOIE_label_citizenshipOther',
            description_msgid='UWOshOIE_help_citizenshipOther',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify normal fields",
        schemata="Demographics",
        searchable=True,
        friendlyName="Other Citizenship Country"
    ),

    StringField('stateResidency',
        widget=SelectionWidget(
            label="State Residency",
            label_msgid='UWOshOIE_label_stateResidency',
            description_msgid='UWOshOIE_help_stateResidency',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify normal fields",
        schemata="Demographics",
        searchable=True,

        vocabulary=['Wisconsin','Minnesota','Other'],
        required=1,
    ),

    StringField('stateResidencyOther',
        widget=StringWidget(
            label="Enter state of residency if you selected Other",
            label_msgid='UWOshOIE_label_stateResidencyOther',
            description_msgid='UWOshOIE_help_stateResidencyOther',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify normal fields",
        schemata="Demographics",
        searchable=True,
        friendlyName="Other State Residency"
    ),

    IntegerField('dateOfBirth_year',
        widget=IntegerWidget(
            label="Birthday (Year, YYYY)",
            label_msgid='UWOshOIE_label_dateOfBirth_year',
            description_msgid='UWOshOIE_help_dateOfBirth_year',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify normal fields",
        searchable=True,
        required=1,
        schemata="Demographics",
        validators=[validators.isValidYearValidator()]
    ),

    StringField('dateOfBirth_month',
        widget=SelectionWidget(
            label="Birthday (Month)",
            label_msgid='UWOshOIE_label_dateOfBirth_month',
            description_msgid='UWOshOIE_help_dateOfBirth_month',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify normal fields",
        required=1,
        schemata="Demographics",
        vocabulary=NamedVocabulary("""UWOshOIEMonths"""),
        searchable=True
    ),

    StringField('dateOfBirth_day',
        widget=SelectionWidget(
            label="Birthday (Day)",
            label_msgid='UWOshOIE_label_dateOfBirth_day',
            description_msgid='UWOshOIE_help_dateOfBirth_day',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify normal fields",
        required=1,
        schemata="Demographics",
        vocabulary=NamedVocabulary("""UWOshOIEDayOfMonth"""),
        searchable=True
    ),

    StringField('placeOfBirth',
        widget=StringWidget(
            label="Place of Birth",
            description="Enter city, state, and country",
            label_msgid='UWOshOIE_label_placeOfBirth',
            description_msgid='UWOshOIE_help_placeOfBirth',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify normal fields",
        required=1,
        schemata="Demographics",
        searchable=True
    ),

    StringField('gender',
        widget=SelectionWidget(
            label='Gender',
            label_msgid='UWOshOIE_label_gender',
            description_msgid='UWOshOIE_help_gender',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify normal fields",
        schemata="Demographics",

        vocabulary=['Male','Female']
    ),

    StringField('marriageStatus',
        widget=SelectionWidget(
            label="Marital Status",
            label_msgid='UWOshOIE_label_marriageStatus',
            description_msgid='UWOshOIE_help_marriageStatus',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify normal fields",
        schemata="Demographics",
        vocabulary=['Married','Single'],
        searchable=True
    ),

    StringField('ethnicity',
        widget=SelectionWidget(
            label='Ethnicity',
            label_msgid='UWOshOIE_label_ethnicity',
            description_msgid='UWOshOIE_help_ethnicity',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify normal fields",
        schemata="Demographics",
        vocabulary=['no answer','Caucasian','African-American','Hispanic','Native American','Asian/Pacific Islander','Other'],
        searchable=True
    ),

    StringField('ethnicityOther',
        widget=StringWidget(
            label="Enter ethnicity if you selected Other",
            label_msgid='UWOshOIE_label_ethnicityOther',
            description_msgid='UWOshOIE_help_ethnicityOther',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify normal fields",
        schemata="Demographics",
        searchable=True,
        friendlyName="Other Ethnicity"
    ),

    StringField('passportName',
        widget=StringWidget(
            label="Full Name",
            description="Enter your full name EXACTLY as it appears on your passport or passport application",
            label_msgid='UWOshOIE_label_passportName',
            description_msgid='UWOshOIE_help_passportName',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify revisable fields",
        schemata="Passport",
        friendlyName="Passport Full Name",
        searchable=True
    ),

    StringField('passportNumber',
        widget=StringWidget(
            label="Passport Number",
            label_msgid='UWOshOIE_label_passportNumber',
            description_msgid='UWOshOIE_help_passportNumber',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify revisable fields",
        schemata="Passport",
        searchable=True
    ),

    StringField('passportIssueOffice',
        widget=StringWidget(
            label="Passport Issuing Office",
            description="E.g. New Orleans or U.S. Department of State",
            label_msgid='UWOshOIE_label_passportIssueOffice',
            description_msgid='UWOshOIE_help_passportIssueOffice',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify revisable fields",
        schemata="Passport",
        searchable=True
    ),

    IntegerField('passportExpDate_year',
        widget=IntegerWidget(
            label="Passport Expiry Year",
            label_msgid='UWOshOIE_label_passportExpDate_year',
            description_msgid='UWOshOIE_help_passportExpDate_year',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify revisable fields",
        schemata="Passport",
        searchable=True,
        validators=[validators.isValidYearValidator()]
    ),

    StringField('passportExpDate_month',
        widget=SelectionWidget(
            label="Passport Expiry Month",
            label_msgid='UWOshOIE_label_passportExpDate_month',
            description_msgid='UWOshOIE_help_passportExpDate_month',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify revisable fields",
        schemata="Passport",
        vocabulary=NamedVocabulary("""UWOshOIEMonths"""),
        searchable=True
    ),

    StringField('passportExpDate_day',
        widget=SelectionWidget(
            label="Passport Expiry Day",
            label_msgid='UWOshOIE_label_passportExpDate_day',
            description_msgid='UWOshOIE_help_passportExpDate_day',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify revisable fields",
        schemata="Passport",
        vocabulary=NamedVocabulary("""UWOshOIEDayOfMonth"""),
        searchable=True
    ),

    TextField('questionAcadCareerPlan',
        allowable_content_types=('text/plain',),
        widget=TextAreaWidget(
            label="Academic and Career Plan",
            description="a) Briefly, what are your short- and long-term academic and career goals? <br> b) Why would you like to participate in this program? <br> c) What do you expect to gain from your experience?",
            label_msgid='UWOshOIE_label_questionAcadCareerPlan',
            description_msgid='UWOshOIE_help_questionAcadCareerPlan',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify normal fields",
        required=1,
        schemata="Additional Questions",
        searchable=True,
        default_output_type='text/plain'
    ),

    TextField('questionLangCulturalSkills',
        allowable_content_types=('text/plain',),
        widget=TextAreaWidget(
            description="a) Have you studied a foreign language? If so, what is your level of fluency? <br> b) Have you completed any University-level courses on the culture or history of your destination? If so, explain. <br> c) Have you ever been immersed in a language and/or culture abroad? If so, please explain. <br> d) Do you plan to use a foreign language in a professional setting? If yes, please explain.",
            label="Language and Cultural Skills",
            label_msgid='UWOshOIE_label_questionLangCulturalSkills',
            description_msgid='UWOshOIE_help_questionLangCulturalSkills',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify normal fields",
        required=1,
        schemata="Additional Questions",
        searchable=True,
        default_output_type='text/plain'
    ),

    TextField('questionPrevTravel',
        allowable_content_types=('text/plain',),
        widget=TextAreaWidget(
            description="Have you traveled abroad? If so, list the places to which you have traveled along with the dates and purpose.",
            label="Previous Travel Experience",
            label_msgid='UWOshOIE_label_questionPrevTravel',
            description_msgid='UWOshOIE_help_questionPrevTravel',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify normal fields",
        required=1,
        schemata="Additional Questions",
        searchable=True,
        default_output_type='text/plain'
    ),

    TextField('questionWorkExp',
        allowable_content_types=('text/plain',),
        widget=TextAreaWidget(
            description="a) Who is your current employer? <br> b) If relevant to your study abroad program, list and describe your responsibilities from current and previous jobs.",
            label="Work Experience",
            label_msgid='UWOshOIE_label_questionWorkExp',
            description_msgid='UWOshOIE_help_questionWorkExp',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify normal fields",
        required=1,
        schemata="Additional Questions",
        searchable=True,
        default_output_type='text/plain'
    ),

    TextField('questionEuroBizTravSem',
        allowable_content_types=('text/plain',),
        widget=TextAreaWidget(
            description="Include the name of the company(ies) you are currently working for and your title(s).",
            label="European Business Travel Seminar Only",
            label_msgid='UWOshOIE_label_questionEuroBizTravSem',
            description_msgid='UWOshOIE_help_questionEuroBizTravSem',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify normal fields",
        schemata="Additional Questions",
        searchable=True,
        default_output_type='text/plain',
    ),

    TextField('questionStuExchComp',
        allowable_content_types=('text/plain',),
        widget=TextAreaWidget(
            label="Student Exchange and Competitive Programs Only",
            description="Add anything else you think we should consider when reviewing your application.",
            label_msgid='UWOshOIE_label_questionStuExchComp',
            description_msgid='UWOshOIE_help_questionStuExchComp',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify normal fields",
        schemata="Additional Questions",
        searchable=True,
        default_output_type='text/plain',
    ),

    StringField('doctorLastname',
        widget=StringWidget(
            label="Last Name of your Family Doctor",
            label_msgid='UWOshOIE_label_doctorLastname',
            description_msgid='UWOshOIE_help_doctorLastname',
            i18n_domain='UWOshOIE',
        ),
        required=1,
        write_permission="UWOshOIE: Modify revisable fields",
        schemata="Medical",
        searchable=True,
        friendlyName="Family Doctor Last Name",
    ),

    StringField('doctorFirstname',
        widget=StringWidget(
            label="First Name of your Family Doctor",
            label_msgid='UWOshOIE_label_doctorFirstname',
            description_msgid='UWOshOIE_help_doctorFirstname',
            i18n_domain='UWOshOIE',
        ),
        required=1,
        write_permission="UWOshOIE: Modify revisable fields",
        schemata="Medical",
        searchable=True,
        friendlyName="Family Doctor First Name",
    ),

    StringField('doctorPhone',
        widget=StringWidget(
            label="Doctor's Phone Number",
            description="Please include country code (if outside US) and area code",
            label_msgid='UWOshOIE_label_doctorPhone',
            description_msgid='UWOshOIE_help_doctorPhone',
            i18n_domain='UWOshOIE',
        ),
        required=1,
        write_permission="UWOshOIE: Modify revisable fields",
        schemata="Medical",
        searchable=True
    ),

    StringField('medicalInsuranceCompany',
        widget=StringWidget(
            label="Name of Insurance Company",
            label_msgid='UWOshOIE_label_medicalInsuranceCompany',
            description_msgid='UWOshOIE_help_medicalInsuranceCompany',
            i18n_domain='UWOshOIE',
        ),
        required=1,
        write_permission="UWOshOIE: Modify revisable fields",
        schemata="Medical",
        searchable=True
    ),

    StringField('medicalPolicyHolder',
        widget=StringWidget(
            label="Name of Policy Holder",
            label_msgid='UWOshOIE_label_medicalPolicyHolder',
            description_msgid='UWOshOIE_help_medicalPolicyHolder',
            i18n_domain='UWOshOIE',
        ),
        required=1,
        write_permission="UWOshOIE: Modify revisable fields",
        schemata="Medical",
        searchable=True
    ),

    StringField('medicalPolicyGroupNumber',
        widget=StringWidget(
            label="Policy / Group Number",
            label_msgid='UWOshOIE_label_medicalPolicyGroupNumber',
            description_msgid='UWOshOIE_help_medicalPolicyGroupNumber',
            i18n_domain='UWOshOIE',
        ),
        required=1,
        write_permission="UWOshOIE: Modify revisable fields",
        schemata="Medical",
        searchable=True
    ),

    TextField('foodAllergies',
        widget=TextAreaWidget(
            label="List any allergies (food, pet, etc.)",
            label_msgid='UWOshOIE_label_foodAllergies',
            description_msgid='UWOshOIE_help_foodAllergies',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify revisable fields",
        schemata="Medical",
        searchable=True,
        friendlyName="Alergies"
    ),

    StringField('hasDifficultyWalking',
        widget=SelectionWidget(
            label="Do you have a condition which would make it difficult to walk long distances?",
            label_msgid='UWOshOIE_label_hasDifficultyWalking',
            description_msgid='UWOshOIE_help_hasDifficultyWalking',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify revisable fields",
        schemata="Medical",
        vocabulary=['Yes','No'],
        required=1,
        enforceVocabulary=1,
        searchable=True,
        friendlyName="Has Difficulty Walking",
        validators=[validators.isDifficultToWalkValidator()]
    ),

    IntegerField('maxWalkingDistance',
        widget=IntegerWidget(
            label="If so, what is the maximum number of minutes you can walk?",
            label_msgid='UWOshOIE_label_maxWalkingDistance',
            description_msgid='UWOshOIE_help_maxWalkingDistance',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify revisable fields",
        schemata="Medical",
        friendlyName="Max Walking Distance"
    ),

    StringField('medicalReadStatement',
        widget=SelectionWidget(
            label="I have read the statement below and understand.",
            description="""Pre-existing medical and mental health conditions are often intensified by travel to or living in a foreign environment.  Before committing to a study abroad program, consider how your new environment may affect your personal health both physically and mentally.  For example, your new environment may introduce you to new diseases, such as malaria or yellow fever, or new stresses which may cause additional complications for a person with a preexisting condition.<br> <br> The OIE strongly recommends that you have a physical, talk with a medical provider about any preexisting conditions and recommended and/or required immunizations, talk with a psychiatrist or counselor about any preexisting conditions and take care of any dental work before departure.<br> <br> If you choose not to complete this section before program acceptance, you must forward information related to the following to the OIE within one week of the application deadline for your program.  Failure to disclose medical or mental health conditions will make it extremely difficult for staff at UW Oshkosh and abroad to assist you in an emergency and may cause health professionals abroad to take actions which could lead to serious medical consequences, including death.<br> <br> NOTE ON MEDICATIONS: You are responsible for ensuring that your medications can be carried into the foreign country.  If your medical status changes after completing this application, you must inform the OIE.""",
            label_msgid='UWOshOIE_label_medicalReadStatement',
            description_msgid='UWOshOIE_help_medicalReadStatement',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify normal fields",
        schemata="Medical II",
        vocabulary=['Yes','No'],
        required=1,
        must_be='Yes',
        friendlyName="Read Medical Read Statement",
        searchable=1
    ),

    TextField('medicalHealthProblems',
        widget=TextAreaWidget(
            label="List and describe any recent (within the past five years) or continuing health problems, including physical disabilities or medical conditions; learning disabilities; drug, plant, food, animal, or insect sting allergies (include information pertaining to reactions); and/or surgeries that should be brought to the attention of the lead faculty members, liaison abroad and/or host family abroad.  ",
            description="Complete this section now or by the Friday following the application deadline.  Write 'n/a' in blanks where appropriate.",
            label_msgid='UWOshOIE_label_medicalHealthProblems',
            description_msgid='UWOshOIE_help_medicalHealthProblems',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify revisable fields",
        required_by_state=['seatAssigned'],
        schemata="Medical III",
        searchable=True,
        friendlyName="Health Problems"
    ),

    StringField('medicalHealthProblems_takenMedication',
        widget=SelectionWidget(
            label="Are you taking or have you ever taken medication related to your physical health?",
            label_msgid='UWOshOIE_label_medicalHealthProblems_takenMedication',
            description_msgid='UWOshOIE_help_medicalHealthProblems_takenMedication',
            i18n_domain='UWOshOIE',
        ),
        vocabulary=['Yes','No'],
        write_permission="UWOshOIE: Modify revisable fields",
        required_by_state=['seatAssigned'],
        schemata="Medical III",
        friendlyName="Has Taken Medication"
    ),

    TextField('medicalHealthProblems_medications',
        widget=TextAreaWidget(
            label="If so, list the medications you have taken over the past year",
            description="Write 'n/a' in blanks where appropriate.",
            label_msgid='UWOshOIE_label_medicalHealthProblems_medications',
            description_msgid='UWOshOIE_help_medicalHealthProblems_medications',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify revisable fields",
        required_by_state=['seatAssigned'],
        schemata="Medical III",
        searchable=True,
        friendlyName="Medication List"
    ),

    StringField('medicalHealthProblems_stable',
        widget=SelectionWidget(
            label="Are you stable on this medication?",
            label_msgid='UWOshOIE_label_medicalHealthProblems_stable',
            description_msgid='UWOshOIE_help_medicalHealthProblems_stable',
            i18n_domain='UWOshOIE',
        ),
        vocabulary=['Yes','No', 'n/a'],
        write_permission="UWOshOIE: Modify revisable fields",
        required_by_state=['seatAssigned'],
        schemata="Medical III",
        friendlyName="Is Stable On Medication"
    ),

    StringField('medicalHealthProblems_underCare',
        widget=SelectionWidget(
            label="Are you currently under the care of a doctor or other health care professional?",
            label_msgid='UWOshOIE_label_medicalHealthProblems_underCare',
            description_msgid='UWOshOIE_help_medicalHealthProblems_underCare',
            i18n_domain='UWOshOIE',
        ),
        vocabulary=['Yes','No'],
        write_permission="UWOshOIE: Modify revisable fields",
        required_by_state=['seatAssigned'],
        schemata="Medical III",
        friendlyName="Is Under Care of Doctor"
    ),

    TextField('medicalHealthProblems_whatCondition',
        widget=TextAreaWidget(
            label="If you are currently under the care of a doctor or other health care professional, for what condition?",
            description="Write 'n/a' in blanks where appropriate.",
            label_msgid='UWOshOIE_label_medicalHealthProblems_whatCondition',
            description_msgid='UWOshOIE_help_medicalHealthProblems_whatCondition',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify revisable fields",
        required_by_state=['seatAssigned'],
        schemata="Medical III",
        searchable=True,
        friendlyName="Medical Care Conditions"
    ),

    StringField('medicalHealthProblems_willingToPrescribe',
        widget=SelectionWidget(
            label="Is your current physician willing to prescribe enough medication to last throughout your planned program abroad?",
            label_msgid='UWOshOIE_label_medicalHealthProblems_willingToPrescribe',
            description_msgid='UWOshOIE_help_medicalHealthProblems_willingToPrescribe',
            i18n_domain='UWOshOIE',
        ),
        vocabulary=['Yes','No', 'n/a'],
        write_permission="UWOshOIE: Modify revisable fields",
        required_by_state=['seatAssigned'],
        schemata="Medical III",
        friendlyName="Physician Willing To Prescribe"
    ),

    TextField('medicalHealthProblems_additionalInfo',
        widget=TextAreaWidget(
            label="Is there any additional information related to your physical health which may be helpful for program organizers, liaisons and host families to know?",
            label_msgid='UWOshOIE_label_medicalHealthProblems_additionalInfo',
            description_msgid='UWOshOIE_help_medicalHealthProblems_additionalInfo',
            i18n_domain='UWOshOIE',
            description="Write 'none' in blank if appropriate.",
        ),
        write_permission="UWOshOIE: Modify revisable fields",
        required_by_state=['seatAssigned'],
        schemata="Medical III",
        searchable=True,
        friendlyName="Additional Health Info"
    ),

    TextField('medicalMentalProblems',
        widget=TextAreaWidget(
            label="List and describe any recent or continuing mental health problems, including anxiety, depression, bipolar disorder, substance abuse (alcohol or drugs), eating disorders (anorexia/bulimia), etc. that should be brought to the attention of the lead faculty members, liaison abroad and/or host family abroad.  Include the following information: diagnosis, dates of treatment, names & locations of treating professionals, and recovery status.",
            description="Complete this section now or by the Friday following the application deadline.  Write 'n/a' in blanks where appropriate.",
            label_msgid='UWOshOIE_label_medicalMentalProblems',
            description_msgid='UWOshOIE_help_medicalMentalProblems',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify revisable fields",
        required_by_state=['seatAssigned'],
        schemata="Medical III",
        searchable=True,
        friendlyName="Mental Health Problem List"
    ),

    StringField('medicalMentalProblems_takenMedication',
        widget=SelectionWidget(
            label="Are you taking/have you ever taken medication related to your mental health?  ",
            label_msgid='UWOshOIE_label_medicalMentalProblems_takenMedication',
            description_msgid='UWOshOIE_help_medicalMentalProblems_takenMedication',
            i18n_domain='UWOshOIE',
        ),
        vocabulary=['Yes','No'],
        write_permission="UWOshOIE: Modify revisable fields",
        required_by_state=['seatAssigned'],
        schemata="Medical III",
        searchable=True,
        friendlyName="Has Taken Mental Health Medication"
    ),

    TextField('medicalMentalProblems_medications',
        widget=TextAreaWidget(
            label="If so, list the medications taken over the past year.  ",
            label_msgid='UWOshOIE_label_medicalMentalProblems_medications',
            description_msgid='UWOshOIE_help_medicalMentalProblems_medications',
            i18n_domain='UWOshOIE',
            description="Write 'n/a' in blanks where appropriate.",
        ),
        write_permission="UWOshOIE: Modify revisable fields",
        required_by_state=['seatAssigned'],
        schemata="Medical III",
        searchable=True,
        friendlyName="Mental Health Medication List"
    ),

    TextField('medicalMentalProblems_currentDose',
        widget=TextAreaWidget(
            label="What is the current dose?",
            description="Write 'n/a' in text area when appropriate.",
            label_msgid='UWOshOIE_label_medicalMentalProblems_currentDose',
            description_msgid='UWOshOIE_help_medicalMentalProblems_currentDose',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify revisable fields",
        required_by_state=['seatAssigned'],
        schemata="Medical III",
        searchable=True,
        friendlyName="Mental Health Medication Dose"
    ),

    StringField('medicalMentalProblems_stable',
        widget=SelectionWidget(
            label="Are you stable on this medication?",
            label_msgid='UWOshOIE_label_medicalMentalProblems_stable',
            description_msgid='UWOshOIE_help_medicalMentalProblems_stable',
            i18n_domain='UWOshOIE',
        ),
        vocabulary=['Yes','No', 'n/a'],
        write_permission="UWOshOIE: Modify revisable fields",
        required_by_state=['seatAssigned'],
        schemata="Medical III",
        searchable=True,
        friendlyName="Is Stable on Mental Health Meds"
    ),

    StringField('medicalMentalProblems_underCare',
        widget=SelectionWidget(
            label="Are you currently or have you ever been under the care of a psychiatrist or other medical provider, substance abuse counselor or other mental health professional?",
            label_msgid='UWOshOIE_label_medicalMentalProblems_underCare',
            description_msgid='UWOshOIE_help_medicalMentalProblems_underCare',
            i18n_domain='UWOshOIE',
        ),
        vocabulary=['Yes','No'],
        write_permission="UWOshOIE: Modify revisable fields",
        required_by_state=['seatAssigned'],
        schemata="Medical III",
        searchable=True,
        friendlyName="Has Been Under Care of Psychiatrist"
    ),

    TextField('medicalMentalProblems_condition',
        widget=TextAreaWidget(
            label="If yes, for what condition?",
            description="Write 'n/a' in text area when appropriate.",
            label_msgid='UWOshOIE_label_medicalMentalProblems_condition',
            description_msgid='UWOshOIE_help_medicalMentalProblems_condition',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify revisable fields",
        required_by_state=['seatAssigned'],
        schemata="Medical III",
        searchable=True,
        friendlyName="Psychiatrist Care Condition"
    ),

    StringField('medicalMentalProblems_enoughMedication',
        widget=SelectionWidget(
            label="Is your current medical provider willing to prescribe enough medication to last for the duration of your planned program abroad?",
            label_msgid='UWOshOIE_label_medicalMentalProblems_enoughMedication',
            description_msgid='UWOshOIE_help_medicalMentalProblems_enoughMedication',
            i18n_domain='UWOshOIE',
        ),
        vocabulary=['Yes','No', 'n/a'],
        write_permission="UWOshOIE: Modify revisable fields",
        required_by_state=['seatAssigned'],
        schemata="Medical III",
        friendlyName="Is Willing To Provide Mental Health Meds"
    ),

    TextField('medicalMentalProblems_additionalInfo',
        widget=TextAreaWidget(
            label="Is there any additional information related to your mental health which may be helpful for program organizers, liaisons and host families to know?",
            label_msgid='UWOshOIE_label_medicalMentalProblems_additionalInfo',
            description_msgid='UWOshOIE_help_medicalMentalProblems_additionalInfo',
            i18n_domain='UWOshOIE',
            description="Write 'none' in text area if there isn't any.",
        ),
        write_permission="UWOshOIE: Modify revisable fields",
        required_by_state=['seatAssigned'],
        schemata="Medical III",
        searchable=True,
        friendlyName="Additional Mental Health Info"
    ),

    StringField('medicalRegistered',
        widget=SelectionWidget(
            label="Are you currently registered with the University of Wisconsin Oshkosh (with offices such as the Dean of Students office or Project Success) or with your university for medical or mental-health related accommodations?",
            label_msgid='UWOshOIE_label_medicalRegistered',
            description_msgid='UWOshOIE_help_medicalRegistered',
            i18n_domain='UWOshOIE',
        ),
        vocabulary=['Yes','No'],
        write_permission="UWOshOIE: Modify revisable fields",
        required_by_state=['seatAssigned'],
        schemata="Medical III",
        friendlyName="Is Medically Registered With UW O"
    ),

    StringField('medicalRegistered_office',
        widget=StringWidget(
            label="If so, with which office have you registered?",
            label_msgid='UWOshOIE_label_medicalRegistered_office',
            description_msgid='UWOshOIE_help_medicalRegistered_office',
            i18n_domain='UWOshOIE',
            description="Write 'none' in text area if you have not registered.",
        ),
        write_permission="UWOshOIE: Modify revisable fields",
        required_by_state=['seatAssigned'],
        schemata="Medical III",
        searchable=True,
        friendlyName="Medical Registration Office"
    ),

    TextField('medicalRegistered_accommodations',
        widget=TextAreaWidget(
            label="What accommodations have been authorized for you?",
            label_msgid='UWOshOIE_label_medicalRegistered_accommodations',
            description_msgid='UWOshOIE_help_medicalRegistered_accommodations',
            i18n_domain='UWOshOIE',
            description="Write 'n/a' in text area when appropriate.",
        ),
        write_permission="UWOshOIE: Modify revisable fields",
        required_by_state=['seatAssigned'],
        schemata="Medical III",
        searchable=True,
        friendlyName="Medical Authorized Accomodations"
    ),

    StringField('medicalAccessOK',
        widget=SelectionWidget(
            label="""I understand and agree that this information will be accessed by the following people: faculty leader(s) (for faculty-led programs), exchange liaison(s) abroad (for student exchange programs), program organizers outside of UW Oshkosh, my host family, staff in the OIE, and staff in the Dean of Students Office.""",
            label_msgid='UWOshOIE_label_medicalAccessOK',
            description_msgid='UWOshOIE_help_medicalAccessOK',
            i18n_domain='UWOshOIE',
        ),
        vocabulary=['Yes','No'],
        write_permission="UWOshOIE: Modify revisable fields",
        schemata="Medical III",
        friendlyName="Medical Access Granted",
        required=1,
        must_be='Yes'
    ),

    StringField('smokingPreferred',
        widget=SelectionWidget(
            label="Smoking Preference",
            label_msgid='UWOshOIE_label_smokingPreferred',
            description_msgid='UWOshOIE_help_smokingPreferred',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify revisable fields",
        schemata="Preferences",
        default= 'No Preference',
        vocabulary=['Smoking','Non-smoking','No Preference'],
        searchable=True,
        friendlyName="Smoking Preference"
    ),

    StringField('isVegetarian',
        widget=SelectionWidget(
            label="Are you vegetarian?",
            label_msgid='UWOshOIE_label_isVegetarian',
            description_msgid='UWOshOIE_help_isVegetarian',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify revisable fields",
        schemata="Preferences",
        vocabulary=['Yes','No'],
        enforceVocabulary=1,
        default="No",
        friendlyName="Is Vegetarian"
    ),

    TextField('additionalNeeds',
        widget=TextAreaWidget(
            label="Is there anything else your host families or the OIE should know about your accommodation needs?",
            label_msgid='UWOshOIE_label_additionalNeeds',
            description_msgid='UWOshOIE_help_additionalNeeds',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify revisable fields",
        schemata="Preferences",
        searchable=True,
        friendlyName="Additional Needs"
    ),

    StringField('emerg1name',
        widget=StringWidget(
            label="Emergency Contact 1 Name",
            label_msgid='UWOshOIE_label_emerg1name',
            description_msgid='UWOshOIE_help_emerg1name',
            i18n_domain='UWOshOIE',
        ),
        required=1,
        write_permission="UWOshOIE: Modify revisable fields",
        schemata="Emergency Contacts",
        searchable=True
    ),

    StringField('emerg1addr1',
        widget=StringWidget(
            label="Emergency Contact 1 Address Line 1",
            label_msgid='UWOshOIE_label_emerg1addr1',
            description_msgid='UWOshOIE_help_emerg1addr1',
            i18n_domain='UWOshOIE',
        ),
        required=1,
        write_permission="UWOshOIE: Modify revisable fields",
        schemata="Emergency Contacts",
        searchable=True
    ),

    StringField('emerg1addr2',
        widget=StringWidget(
            label="Emergency Contact 1 Address Line 2",
            label_msgid='UWOshOIE_label_emerg1addr2',
            description_msgid='UWOshOIE_help_emerg1addr2',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify revisable fields",
        schemata="Emergency Contacts",
        searchable=True
    ),

    StringField('emerg1city',
        widget=StringWidget(
            label="Emergency Contact 1 City",
            label_msgid='UWOshOIE_label_emerg1city',
            description_msgid='UWOshOIE_help_emerg1city',
            i18n_domain='UWOshOIE',
        ),
        required=1,
        write_permission="UWOshOIE: Modify revisable fields",
        schemata="Emergency Contacts",
        searchable=True
    ),

    StringField('emerg1state',
        widget=StringWidget(
            label="Emergency Contact 1 State",
            label_msgid='UWOshOIE_label_emerg1state',
            description_msgid='UWOshOIE_help_emerg1state',
            i18n_domain='UWOshOIE',
        ),
        required=1,
        write_permission="UWOshOIE: Modify revisable fields",
        schemata="Emergency Contacts",
        searchable=True
    ),

    StringField('emerg1zip',
        widget=StringWidget(
            label="Emergency Contact 1 Zip Code",
            label_msgid='UWOshOIE_label_emerg1zip',
            description_msgid='UWOshOIE_help_emerg1zip',
            i18n_domain='UWOshOIE',
        ),
        required=1,
        write_permission="UWOshOIE: Modify revisable fields",
        schemata="Emergency Contacts",
        searchable=True
    ),

    StringField('emerg1country',
        widget=StringWidget(
            label="Emergency Contact 1 Country",
            label_msgid='UWOshOIE_label_emerg1country',
            description_msgid='UWOshOIE_help_emerg1country',
            i18n_domain='UWOshOIE',
        ),
        required=1,
        write_permission="UWOshOIE: Modify revisable fields",
        schemata="Emergency Contacts",
        searchable=True
    ),

    StringField('emerg1homePhone',
        widget=StringWidget(
            label="Emergency Contact 1 Home Phone",
            description="Please include country code (if outside US) and area code",
            label_msgid='UWOshOIE_label_emerg1homePhone',
            description_msgid='UWOshOIE_help_emerg1homePhone',
            i18n_domain='UWOshOIE',
        ),
        required=1,
        write_permission="UWOshOIE: Modify revisable fields",
        schemata="Emergency Contacts",
        searchable=True
    ),

    StringField('emerg1workPhone',
        widget=StringWidget(
            label="Emergency Contact 1 Work Phone",
            description="Strongly recommended.  Please include country code (if outside US) and area code",
            label_msgid='UWOshOIE_label_emerg1workPhone',
            description_msgid='UWOshOIE_help_emerg1workPhone',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify revisable fields",
        schemata="Emergency Contacts",
        searchable=True
    ),

    StringField('emerg1mobilePhone',
        widget=StringWidget(
            label="Emergency Contact 1 Mobile Phone",
            description="Strongly recommended.  Please include country code (if outside US) and area code",
            label_msgid='UWOshOIE_label_emerg1mobilePhone',
            description_msgid='UWOshOIE_help_emerg1mobilePhone',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify revisable fields",
        schemata="Emergency Contacts",
        searchable=True
    ),

    StringField('emerg1email',
        widget=StringWidget(
            label="Emergency Contact 1 Email",
            description="Strongly recommended",
            label_msgid='UWOshOIE_label_emerg1email',
            description_msgid='UWOshOIE_help_emerg1email',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify revisable fields",
        schemata="Emergency Contacts",
        searchable=True,
        validators=[u'isEmail']
    ),

    StringField('emerg2name',
        widget=StringWidget(
            label="Emergency Contact 2 Name",
            label_msgid='UWOshOIE_label_emerg2name',
            description_msgid='UWOshOIE_help_emerg2name',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify revisable fields",
        schemata="Emergency Contacts",
        searchable=True
    ),

    StringField('emerg2addr1',
        widget=StringWidget(
            label="Emergency Contact 2 Address Line 1",
            label_msgid='UWOshOIE_label_emerg2addr1',
            description_msgid='UWOshOIE_help_emerg2addr1',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify revisable fields",
        schemata="Emergency Contacts",
        searchable=True
    ),

    StringField('emerg2addr2',
        widget=StringWidget(
            label="Emergency Contact 2 Address Line 2",
            label_msgid='UWOshOIE_label_emerg2addr2',
            description_msgid='UWOshOIE_help_emerg2addr2',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify revisable fields",
        schemata="Emergency Contacts",
        searchable=True
    ),

    StringField('emerg2city',
        widget=StringWidget(
            label="Emergency Contact 2 City",
            label_msgid='UWOshOIE_label_emerg2city',
            description_msgid='UWOshOIE_help_emerg2city',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify revisable fields",
        schemata="Emergency Contacts",
        searchable=True
    ),

    StringField('emerg2state',
        widget=StringWidget(
            label="Emergency Contact 2 State",
            label_msgid='UWOshOIE_label_emerg2state',
            description_msgid='UWOshOIE_help_emerg2state',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify revisable fields",
        schemata="Emergency Contacts",
        searchable=True
    ),

    StringField('emerg2zip',
        widget=StringWidget(
            label="Emergency Contact 2 Zip Code",
            label_msgid='UWOshOIE_label_emerg2zip',
            description_msgid='UWOshOIE_help_emerg2zip',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify revisable fields",
        schemata="Emergency Contacts",
        searchable=True
    ),

    StringField('emerg2country',
        widget=StringWidget(
            label="Emergency Contact 2 Country",
            label_msgid='UWOshOIE_label_emerg2country',
            description_msgid='UWOshOIE_help_emerg2country',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify revisable fields",
        schemata="Emergency Contacts",
        searchable=True
    ),

    StringField('emerg2homePhone',
        widget=StringWidget(
            label="Emergency Contact 2 Home Phone",
            description="Please include country code (if outside US) and area code",
            label_msgid='UWOshOIE_label_emerg2homePhone',
            description_msgid='UWOshOIE_help_emerg2homePhone',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify revisable fields",
        schemata="Emergency Contacts",
        searchable=True
    ),

    StringField('emerg2workPhone',
        widget=StringWidget(
            label="Emergency Contact 2 Work Phone",
            description="Please include country code (if outside US) and area code",
            label_msgid='UWOshOIE_label_emerg2workPhone',
            description_msgid='UWOshOIE_help_emerg2workPhone',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify revisable fields",
        schemata="Emergency Contacts",
        searchable=True
    ),

    StringField('emerg2mobilePhone',
        widget=StringWidget(
            label="Emergency Contact 2 Mobile Phone",
            description="Please include country code (if outside US) and area code",
            label_msgid='UWOshOIE_label_emerg2mobilePhone',
            description_msgid='UWOshOIE_help_emerg2mobilePhone',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify revisable fields",
        schemata="Emergency Contacts",
        searchable=True
    ),

    StringField('emerg2email',
        widget=StringWidget(
            label="Emergency Contact 2 Email",
            label_msgid='UWOshOIE_label_emerg2email',
            description_msgid='UWOshOIE_help_emerg2email',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify revisable fields",
        schemata="Emergency Contacts",
        searchable=True,
        validators=[u'isEmail']
    ),

    StringField('emerg3name',
        widget=StringWidget(
            label="Emergency Contact 3 Name",
            label_msgid='UWOshOIE_label_emerg3name',
            description_msgid='UWOshOIE_help_emerg3name',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify revisable fields",
        schemata="Emergency Contacts",
        searchable=True
    ),

    StringField('emerg3addr1',
        widget=StringWidget(
            label="Emergency Contact 3 Address Line 1",
            label_msgid='UWOshOIE_label_emerg3addr1',
            description_msgid='UWOshOIE_help_emerg3addr1',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify revisable fields",
        schemata="Emergency Contacts",
        searchable=True
    ),

    StringField('emerg3addr2',
        widget=StringWidget(
            label="Emergency Contact 3 Address Line 2",
            label_msgid='UWOshOIE_label_emerg3addr2',
            description_msgid='UWOshOIE_help_emerg3addr2',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify revisable fields",
        schemata="Emergency Contacts",
        searchable=True
    ),

    StringField('emerg3city',
        widget=StringWidget(
            label="Emergency Contact 3 City",
            label_msgid='UWOshOIE_label_emerg3city',
            description_msgid='UWOshOIE_help_emerg3city',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify revisable fields",
        schemata="Emergency Contacts",
        searchable=True
    ),

    StringField('emerg3state',
        widget=StringWidget(
            label="Emergency Contact 3 State",
            label_msgid='UWOshOIE_label_emerg3state',
            description_msgid='UWOshOIE_help_emerg3state',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify revisable fields",
        schemata="Emergency Contacts",
        searchable=True
    ),

    StringField('emerg3zip',
        widget=StringWidget(
            label="Emergency Contact 3 Zip Code",
            label_msgid='UWOshOIE_label_emerg3zip',
            description_msgid='UWOshOIE_help_emerg3zip',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify revisable fields",
        schemata="Emergency Contacts",
        searchable=True
    ),

    StringField('emerg3country',
        widget=StringWidget(
            label="Emergency Contact 3 Country",
            label_msgid='UWOshOIE_label_emerg3country',
            description_msgid='UWOshOIE_help_emerg3country',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify revisable fields",
        schemata="Emergency Contacts",
        searchable=True
    ),

    StringField('emerg3homePhone',
        widget=StringWidget(
            label="Emergency Contact 3 Home Phone",
            description="Please include country code (if outside US) and area code",
            label_msgid='UWOshOIE_label_emerg3homePhone',
            description_msgid='UWOshOIE_help_emerg3homePhone',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify revisable fields",
        schemata="Emergency Contacts",
        searchable=True
    ),

    StringField('emerg3workPhone',
        widget=StringWidget(
            label="Emergency Contact 3 Work Phone",
            description="Please include country code (if outside US) and area code",
            label_msgid='UWOshOIE_label_emerg3workPhone',
            description_msgid='UWOshOIE_help_emerg3workPhone',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify revisable fields",
        schemata="Emergency Contacts",
        searchable=True
    ),

    StringField('emerg3mobilePhone',
        widget=StringWidget(
            label="Emergency Contact 3 Mobile Phone",
            description="Please include country code (if outside US) and area code",
            label_msgid='UWOshOIE_label_emerg3mobilePhone',
            description_msgid='UWOshOIE_help_emerg3mobilePhone',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify revisable fields",
        schemata="Emergency Contacts",
        searchable=True
    ),

    StringField('emerg3email',
        widget=StringWidget(
            label="Emergency Contact 3 Email",
            label_msgid='UWOshOIE_label_emerg3email',
            description_msgid='UWOshOIE_help_emerg3email',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify revisable fields",
        schemata="Emergency Contacts",
        searchable=True,
        validators=[u'isEmail']
    ),

    ReferenceField('programName',
        widget=ReferenceWidget(
            label="Program Name",
            label_msgid='UWOshOIE_label_programName',
            description_msgid='UWOshOIE_help_programName',
            i18n_domain='UWOshOIE'
        ),
        write_permission="UWOshOIE: Modify normal fields", 
        relationship="WorksWith",
        vocabulary_display_path_bound=-1,
        allowed_types=('UWOshOIEProgram',),
        vocabulary_custom_label="b.getObject().title_or_id()",
        validators = [validators.ReferenceValidator()]
    ),

    IntegerField('programYear',
        widget=IntegerWidget(
            label="Program Year",
            description="Enter the year you will actually be attending the program (YYYY)",
            label_msgid='UWOshOIE_label_programYear',
            description_msgid='UWOshOIE_help_programYear',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify normal fields",
        searchable=True,
        required=1,
        schemata="default",
        validators=[validators.isValidYearValidator()],
    ),

    StringField('programSemester',
        widget=SelectionWidget(
            label="Semester",
            label_msgid='UWOshOIE_label_programSemester',
            description_msgid='UWOshOIE_help_programSemester',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify normal fields",
        required=1,
        schemata="default",
        vocabulary=['Fall','Fall Interim','Spring','Spring Interim','Summer'],
        searchable=True
    ),

    StringField('studentType',
        widget=SelectionWidget(
            label="Student Type",
            label_msgid='UWOshOIE_label_studentType',
            description_msgid='UWOshOIE_help_studentType',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify normal fields",
        schemata="Education",
        vocabulary=['UW Oshkosh Freshman','UW Oshkosh Sophomore','UW Oshkosh Junior','UW Oshkosh Senior','UW Oshkosh Graduate Student','Student at another University (please complete and submit the "Special Student" form)','I am not a Student (please complete and submit the "Special Student" form)'],
        required=1,
        searchable=True
    ),

    StringField('universityEnrolled',
        widget=StringWidget(
            label="Name of other university",
            description="No abbreviations please",
            label_msgid='UWOshOIE_label_universityEnrolled',
            description_msgid='UWOshOIE_help_universityEnrolled',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify normal fields",
        schemata="Education",
        searchable=True
    ),

    StringField('graduationMonth',
        widget=SelectionWidget(
            label="Expected Graduation Month",
            label_msgid='UWOshOIE_label_graduationMonth',
            description_msgid='UWOshOIE_help_graduationMonth',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify normal fields",
        schemata="Education",
        vocabulary=NamedVocabulary("""UWOshOIEGraduationMonths"""),
        searchable=True,
        required=1
    ),

    IntegerField('graduationYear',
        widget=IntegerWidget(
            label="Expected Graduation Year",
            description="YYYY(Use '0000' if not a student)",
            label_msgid='UWOshOIE_label_graduationYear',
            description_msgid='UWOshOIE_help_graduationYear',
            i18n_domain='UWOshOIE',
        ),
        required=1,
        write_permission="UWOshOIE: Modify normal fields",
        validators=[validators.isValidYearValidator()],
        schemata="Education",
        searchable=True
    ),

    FloatField('cumulativeGPA',
        widget=DecimalWidget(
            label="Cumulative GPA",
            description="out of 4.0(Use 0.0 if not a student)",
            label_msgid='UWOshOIE_label_cumulativeGPA',
            description_msgid='UWOshOIE_help_cumulativeGPA',
            i18n_domain='UWOshOIE',
        ),
        required=1,
        write_permission="UWOshOIE: Modify normal fields",
        validators=[u"ExpressionValidator('python:value >= 0')"],
        schemata="Education",
        searchable=True
    ),

    StringField('major1',
        widget=SelectionWidget(
            label="First Major",
            label_msgid='UWOshOIE_label_major1',
            description_msgid='UWOshOIE_help_major1',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify normal fields",
        vocabulary=NamedVocabulary("""UWOshOIEMajors"""),
        searchable=True,
        schemata="Education"
    ),

    StringField('major2',
        widget=SelectionWidget(
            label="Second Major",
            label_msgid='UWOshOIE_label_major2',
            description_msgid='UWOshOIE_help_major2',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify normal fields",
        vocabulary=NamedVocabulary("""UWOshOIEMajors"""),
        searchable=True,
        schemata="Education"
    ),

    StringField('minor1',
        widget=StringWidget(
            label="Minor 1",
            label_msgid='UWOshOIE_label_minor1',
            description_msgid='UWOshOIE_help_minor1',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify normal fields",
        vocabulary=NamedVocabulary("""UWOshOIEMinors"""),
        searchable=True,
        schemata="Education"
    ),

    StringField('minor2',
        widget=StringWidget(
            label="Minor 2",
            label_msgid='UWOshOIE_label_minor2',
            description_msgid='UWOshOIE_help_minor2',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify normal fields",
        vocabulary=NamedVocabulary("""UWOshOIEMinors"""),
        searchable=True,
        schemata="Education"
    ),

    StringField('emphasis1',
        widget=StringWidget(
            label="Emphasis/Licensure 1",
            label_msgid='UWOshOIE_label_emphasis1',
            description_msgid='UWOshOIE_help_emphasis1',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify normal fields",
        schemata="Education",
        searchable=True
    ),

    StringField('emphasis2',
        widget=StringWidget(
            label="Emphasis/Licensure 2",
            label_msgid='UWOshOIE_label_emphasis2',
            description_msgid='UWOshOIE_help_emphasis2',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify normal fields",
        schemata="Education",
        searchable=True
    ),

    StringField('willTakeBus',
        widget=SelectionWidget(
            label="Bus",
            description="Please note: while a group bus is an option for most programs, not all programs offer this option.",
            label_msgid='UWOshOIE_label_willTakeBus',
            description_msgid='UWOshOIE_help_willTakeBus',
            i18n_domain='UWOshOIE',
        ),
        required=1,
        write_permission="UWOshOIE: Modify revisable fields",
        schemata="Transportation",
        vocabulary=['I will take the group bus from Oshkosh to the airport',
                    'I will arrange for my own transportation from Oshkosh to the airport.'],
        searchable=True
    ),

    StringField('willFlyWithGroup',
        widget=SelectionWidget(
            label="Flights",
            label_msgid='UWOshOIE_label_willFlyWithGroup',
            description_msgid='UWOshOIE_help_willFlyWithGroup',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify normal fields",
        required=1,
        schemata="Transportation",
        vocabulary=['I will fly with the group','I will deviate from the group itinerary'],
        searchable=True
    ),

    DateTimeField('departureDate',
        widget=CalendarWidget(
            show_hm="0",
            label="Planned Departure Date",
            description="Specify if you are deviating from the group itinerary.",
            label_msgid='UWOshOIE_label_departureDate',
            description_msgid='UWOshOIE_help_departureDate',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify normal fields",
        schemata="Transportation",
        searchable=True
    ),

    DateTimeField('returnDate',
        widget=CalendarWidget(
            show_hm="0",
            description="Specify if you are deviating from the group itinerary.",
            label="Planned Return Date",
            label_msgid='UWOshOIE_label_returnDate',
            description_msgid='UWOshOIE_help_returnDate',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify normal fields",
        schemata="Transportation",
        searchable=True
    ),

    StringField('agreeToCosts',
        widget=StringWidget(
            label="I understand that if I choose not to fly on dates recommended by the OIE or by my hosts abroad, I remain responsible for the full program cost, regardless of whether I participate in all events or make use of all services.",
            description="Enter your initials",
            label_msgid='UWOshOIE_label_agreeToCosts',
            description_msgid='UWOshOIE_help_agreeToCosts',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify normal fields",
        required=1,
        schemata="Transportation",
        searchable=True,
        friendlyName="Is Agreed To Costs"
    ),

    DateTimeField('orientationDate1',
        widget=CalendarWidget(
            label="I will attend the family orientation on",
            description="Enter one date and time for the four-hour session, or enter two dates and times for the two-hour sessions",
            show_hm = False,
            label_msgid='UWOshOIE_label_orientationDate1',
            description_msgid='UWOshOIE_help_orientationDate1',
            i18n_domain='UWOshOIE',
        ),
        required=1,
        write_permission="UWOshOIE: Modify normal fields",
        schemata="Orientation",
        searchable=True,
        friendlyName="Orientation Session part 1 (Date)"
    ),

    StringField('orientationHours1',
        widget=SelectionWidget(
            label="Orientation Session 1 \"hours\"",
            description="",
            label_msgid='UWOshOIE_label_orientationHours1',
            description_msgid='UWOshOIE_help_orientationHours1',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify normal fields",
        schemata="Orientation",
        required=1,
        vocabulary=NamedVocabulary("""UWOshOIESessionHours"""),
        searchable=True,
    ),

    DateTimeField('orientationDate2',
        widget=CalendarWidget(
            label="Orientation Session part 2 (Date)",
            description="if applicable",
            show_hm = False
        ),
        write_permission="UWOshOIE: Modify normal fields",
        schemata="Orientation",
        searchable=True,
        validators=(validators.orientationSession2DateValidator(),)
    ),

    BooleanField('orientationHours2',
        widget=SelectionWidget(
            description="if applicable",
            label="Will attend orientation Session part 2 from 3pm - 5pm",
            show_hm = False,
            label_msgid='UWOshOIE_label_orientationHours2',
            description_msgid='UWOshOIE_help_orientationHours2',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify normal fields",
        schemata="Orientation",
        searchable=True,
        validators= [validators.orientationSession2hoursValidator()]
    ),

    IntegerField('numberOfGuests',
        widget=IntegerWidget(
            label="The following number of people will attend with me",
            label_msgid='UWOshOIE_label_numberOfGuests',
            description_msgid='UWOshOIE_help_numberOfGuests',
            i18n_domain='UWOshOIE',
        ),
        searchable=True,
        required=1,
        friendlyName="Number of Guests",
        write_permission="UWOshOIE: Modify revisable fields",
        schemata="Orientation",
        validators=[u"ExpressionValidator('python:value >= 0')"]
    ),

    StringField('orientationConflict',
        widget=SelectionWidget(
            label="Do you have a conflict with any of the other pre-travel academic and/or orientation sessions?",
            label_msgid='UWOshOIE_label_orientationConflict',
            description_msgid='UWOshOIE_help_orientationConflict',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify normal fields",
        friendlyName="Has Conflicts",
        required=1,
        schemata="Orientation",
        vocabulary=['No','Yes, I have a conflict on (enter the date next):','No dates are listed'],
        searchable=True,
        validators=[validators.orientationConflictDateValidator()]
    ),

    DateTimeField('conflictDate',
        widget=CalendarWidget(
            label="Date of your conflict",
            description="if you selected Yes above",
            show_hm = False,
            label_msgid='UWOshOIE_label_conflictDate',
            description_msgid='UWOshOIE_help_conflictDate',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify normal fields",
        schemata="Orientation",
        searchable=True
    ),

    StringField('subject1',
        widget=SelectionWidget(
            label="Course 1 subject",
            label_msgid='UWOshOIE_label_subject1',
            description_msgid='UWOshOIE_help_subject1',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify normal fields",
        required=1,
        schemata="Courses",
        validators = ( ExpressionValidator('python: value != \'-- choose one --\'', "You must select a subject."), ),
        vocabulary=NamedVocabulary("""UWOshOIESubjects"""),
        searchable=True
    ),

    StringField('course1',
        widget=StringWidget(
            label="Course Number 1",
            label_msgid='UWOshOIE_label_course1',
            description_msgid='UWOshOIE_help_course1',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify normal fields",
        required=1,
        schemata="Courses",
        searchable=True
    ),

    FloatField('credits1',
        widget=DecimalWidget(
            label="Credits 1",
            label_msgid='UWOshOIE_label_credits1',
            description_msgid='UWOshOIE_help_credits1',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify normal fields",
        required=1,
        schemata="Courses",
        searchable=True
    ),

    StringField('subject2',
        widget=SelectionWidget(
            label="Course 2 subject",
            label_msgid='UWOshOIE_label_subject2',
            description_msgid='UWOshOIE_help_subject2',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify normal fields",
        schemata="Courses",
        vocabulary=NamedVocabulary("""UWOshOIESubjects"""),
        searchable=True
    ),

    StringField('course2',
        widget=StringWidget(
            label="Course Number 2",
            label_msgid='UWOshOIE_label_course2',
            description_msgid='UWOshOIE_help_course2',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify normal fields",
        schemata="Courses",
        searchable=True
    ),

    FloatField('credits2',
        widget=DecimalWidget(
            label="Credits 2",
            label_msgid='UWOshOIE_label_credits2',
            description_msgid='UWOshOIE_help_credits2',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify normal fields",
        schemata="Courses",
        searchable=True
    ),

    StringField('subject3',
        widget=SelectionWidget(
            label="Course 3 subject",
            label_msgid='UWOshOIE_label_subject3',
            description_msgid='UWOshOIE_help_subject3',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify normal fields",
        schemata="Courses",
        vocabulary=NamedVocabulary("""UWOshOIESubjects"""),
        searchable=True
    ),

    StringField('course3',
        widget=StringWidget(
            label="Course Number 3",
            label_msgid='UWOshOIE_label_course3',
            description_msgid='UWOshOIE_help_course3',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify normal fields",
        schemata="Courses",
        searchable=True
    ),

    FloatField('credits3',
        widget=DecimalWidget(
            label="Credits 3",
            label_msgid='UWOshOIE_label_credits3',
            description_msgid='UWOshOIE_help_credits3',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify normal fields",
        schemata="Courses",
        searchable=True
    ),

    StringField('subject4',
        widget=SelectionWidget(
            label="Course 4 subject",
            label_msgid='UWOshOIE_label_subject4',
            description_msgid='UWOshOIE_help_subject4',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify normal fields",
        schemata="Courses",
        vocabulary=NamedVocabulary("""UWOshOIESubjects"""),
        searchable=True
    ),

    StringField('course4',
        widget=StringWidget(
            label="Course Number 4",
            label_msgid='UWOshOIE_label_course4',
            description_msgid='UWOshOIE_help_course4',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify normal fields",
        schemata="Courses",
        searchable=True
    ),

    FloatField('credits4',
        widget=DecimalWidget(
            label="Credits 4",
            label_msgid='UWOshOIE_label_credits4',
            description_msgid='UWOshOIE_help_credits4',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify normal fields",
        schemata="Courses",
        searchable=True
    ),

    StringField('subject5',
        widget=SelectionWidget(
            label="Course 5 subject",
            label_msgid='UWOshOIE_label_subject5',
            description_msgid='UWOshOIE_help_subject5',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify normal fields",
        schemata="Courses",
        vocabulary=NamedVocabulary("""UWOshOIESubjects"""),
        searchable=True
    ),

    StringField('course5',
        widget=StringWidget(
            label="Course Number 5",
            label_msgid='UWOshOIE_label_course5',
            description_msgid='UWOshOIE_help_course5',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify normal fields",
        schemata="Courses",
        searchable=True
    ),

    FloatField('credits5',
        widget=DecimalWidget(
            label="Credits 5",
            label_msgid='UWOshOIE_label_credits5',
            description_msgid='UWOshOIE_help_credits5',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify normal fields",
        schemata="Courses",
        searchable=True
    ),

    StringField('subject6',
        widget=SelectionWidget(
            label="Course 6 subject",
            label_msgid='UWOshOIE_label_subject6',
            description_msgid='UWOshOIE_help_subject6',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify normal fields",
        schemata="Courses",
        vocabulary=NamedVocabulary("""UWOshOIESubjects"""),
        searchable=True
    ),

    StringField('course6',
        widget=StringWidget(
            label="Course Number 6",
            label_msgid='UWOshOIE_label_course6',
            description_msgid='UWOshOIE_help_course6',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify normal fields",
        schemata="Courses",
        searchable=True
    ),

    FloatField('credits6',
        widget=DecimalWidget(
            label="Credits 6",
            label_msgid='UWOshOIE_label_credits6',
            description_msgid='UWOshOIE_help_credits6',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify normal fields",
        schemata="Courses",
        searchable=True
    ),

    BooleanField('readSyllabus',
        widget=BooleanWidget(
            label="I have read the syllabus for the one-credit course International Studies 333",
            label_msgid='UWOshOIE_label_readSyllabus',
            description_msgid='UWOshOIE_help_readSyllabus',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify normal fields",
        schemata="Courses",
        searchable=True,
        friendlyName="Has Read Syllabus"
    ),

    BooleanField('enrolledIS333',
        widget=BooleanWidget(
            label="Enroll me in International Studies 333",
            description="You will only be enrolled if you have read the syllabus",
            label_msgid='UWOshOIE_label_enrolledIS333',
            description_msgid='UWOshOIE_help_enrolledIS333',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify normal fields",
        schemata="Courses",
        searchable=True,
        friendlyName="Is Enrolled in International Studies 333"
    ),

    StringField('applyForAid',
        widget=SelectionWidget(
            label="Are you applying for financial aid?",
            description="If you are not applying for financial aid, skip to the next section.",
            label_msgid='UWOshOIE_label_applyForAid',
            description_msgid='UWOshOIE_help_applyForAid',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify normal fields",
        required=1,
        vocabulary=['Yes','No'],
        schemata="Financial Aid",
        searchable=True,
        view="Owner; Reviewer; Manager; UWOshOIEFinAid",
        friendlyName="Is Applying for Financial Aid",
        validators=[validators.financialAidValidator()]
    ),

    StringField('holdApplication',
        widget=SelectionWidget(
            label="Should the OIE hold or process your application?",
            description="HOLD your Study Abroad Application (i.e. you will only study abroad IF financial aid is available; at this point the application fee is still refundable but the OIE is not reserving a seat for you), or PROCESS your Study Abroad Applciation (i.e. you will study abroad regardless of your aid package; at this point the application fee is non-refundable and the OIE will reserve your seat.",
            label_msgid='UWOshOIE_label_holdApplication',
            description_msgid='UWOshOIE_help_holdApplication',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify normal fields",
        schemata="Financial Aid",
        vocabulary=['HOLD','PROCESS'],
        searchable=True,
        friendlyName="Hold Application"
    ),

    BooleanField('financialAidGranted',
        widget=BooleanWidget(
            label="Financial Aid Granted?",
            description="Set by Financial Aid staff only",
            label_msgid='UWOshOIE_label_financialAidGranted',
            description_msgid='UWOshOIE_help_financialAidGranted',
            i18n_domain='UWOshOIE',
        ),
        schemata="Financial Aid",
        write_permission="UWOshOIE: Modify Financial Aid fields",
        read_permission="View",
        friendlyName="Financial Aid Granted"
    ),

    StringField('roomType',
        widget=SelectionWidget(
            label="Room Type",
            label_msgid='UWOshOIE_label_roomType',
            description_msgid='UWOshOIE_help_roomType',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify revisable fields",
        schemata="Accommodation Preferences",
        vocabulary=['Single Room','Double Room','Triple Room'],
        searchable=True
    ),

    StringField('roommateName1',
        widget=StringWidget(
            label="Roommate 1 Name",
            label_msgid='UWOshOIE_label_roommateName1',
            description_msgid='UWOshOIE_help_roommateName1',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify revisable fields",
        schemata="Accommodation Preferences",

        searchable=True
    ),

    StringField('roommateName2',
        widget=StringWidget(
            label="Roommate 2 Name",
            label_msgid='UWOshOIE_label_roommateName2',
            description_msgid='UWOshOIE_help_roommateName2',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify revisable fields",
        schemata="Accommodation Preferences",

        searchable=True
    ),

    TextField('questionExpectations',
        allowable_content_types=('text/plain',),
        widget=TextAreaWidget(
            label="Your Expectations For",
            description="a) this program as a whole? <br> b) the pre-travel general orientation session? <br> c) the pre-travel academic sessions? <br> d) your hosts (host institution, family, etc.) in the foreign country (if applicable)?",
            label_msgid='UWOshOIE_label_questionExpectations',
            description_msgid='UWOshOIE_help_questionExpectations',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify normal fields",
        required=1,
        schemata="Expectations",
        searchable=True,
        friendlyName="Expectations",
        default_output_type='text/plain'
    ),

    StringField('awareOfAllMaterials',
        widget=SelectionWidget(
            label="Are you aware of the application requirements for your program?",
            description="Additional application requirements for select programs are listed on individual program web pages.  Not all programs have additional requirements.",
            label_msgid='UWOshOIE_label_awareOfAllMaterials',
            description_msgid='UWOshOIE_help_awareOfAllMaterials',
            i18n_domain='UWOshOIE',
        ),
        write_permission="UWOshOIE: Modify normal fields",
        schemata="Verification",
        vocabulary=['Yes, I am aware of the application requirements for my program','There are no additional application requirements for my program'],
        required=1,
        enforceVocabulary=1,
        friendlyName="Is Aware of Application Requirements",
        searchable=True
    ),

    StringField('UWOshkoshRelease',
        widget=SelectionWidget(
            label="Release of Liability",
            description="I hereby agree to hold harmless and indemnify the Board of Regents of the University of Wisconsin System and the University of Wisconsin Oshkosh, their officers, agents and employees, from any and all liability, loss, damages, costs or expenses which are sustained, incurred or required arising out of my actions.",
            label_msgid='UWOshOIE_label_UWOshkoshRelease',
            description_msgid='UWOshOIE_help_UWOshkoshRelease',
            i18n_domain='UWOshOIE',
        ),
        vocabulary=['Yes','No'],
        must_be='Yes',
        required=1,
        write_permission="UWOshOIE: Modify normal fields",
        schemata="Verification",
        friendlyName="Agreed To Release of Liability",
        searchable=True
    ),

    StringField('certification',
        widget=SelectionWidget(
            label="Certification",
            description="I certify that the information stated above is true and correct.  If accepted to the program, I agree to follow all payment and withdrawal policies and to regularly check my UW Oshkosh email account for program information beginning today.  If I am a non-UW Oshkosh student, I will use and submit an email address that I check regularly.",
            label_msgid='UWOshOIE_label_certification',
            description_msgid='UWOshOIE_help_certification',
            i18n_domain='UWOshOIE',
        ),
        vocabulary=['Yes','No'],
        must_be='Yes',
        required=1,
        write_permission="UWOshOIE: Modify normal fields",
        schemata="Verification",
        friendlyName="Has Certified Information Correct",
        searchable=True
    ),

#########################
#OFFICE USE ONLY SECTION
#########################

    StringField('seatNumber',
        widget=StringWidget(
            label='Seat Number',
            label_msgid='UWOshOIE_label_seatNumber',
            description_msgid='UWOshOIE_help_seatNumber',
            i18n_domain='UWOshOIE',
        ),
        schemata="OFFICE USE ONLY",
        read_permission="View",
        write_permission="UWOshOIE: Modify Office Use Only fields",
        searchable=True
    ),
    
    DateTimeField('completionDate',
        widget=CalendarWidget(
            label="Date Application Was Completed",
            description="This is the date in which the application was completed.",
            show_hm="0",
            label_msgid='UWOshOIE_label_completionDate',
            description_msgid='UWOshOIE_help_completionDate',
            i18n_domain='UWOshOIE',
        ),
        required_by_state=['needsDirectorReview'],
        schemata="OFFICE USE ONLY",
        read_permission="View",
        write_permission="UWOshOIE: Modify Office Use Only fields",
        searchable=True
    ),

    BooleanField('applicationIsComplete',
        widget=BooleanWidget(
            label="Application is Complete",
            label_msgid='UWOshOIE_label_applicationIsComplete',
            description_msgid='UWOshOIE_help_applicationIsComplete',
            i18n_domain='UWOshOIE',
        ),
        schemata="OFFICE USE ONLY",
        read_permission="View",
        write_permission="UWOshOIE: Modify Office Use Only fields",
    ),
    
    TextField('comments',
        allowable_content_types=('text/plain',),
        widget=TextAreaWidget(
            label='Comments',
            label_msgid='UWOshOIE_label_comments',
            description_msgid='UWOshOIE_help_comments',
            i18n_domain='UWOshOIE',
        ),
        default_output_type='text/plain',
        schemata="OFFICE USE ONLY",
        read_permission="UWOshOIE: Modify Office Use Only fields",
        write_permission="UWOshOIE: Modify Office Use Only fields"
    ),
    
    BooleanField('applicationFeeOK',
        widget=BooleanWidget(
            label="Application Fee Submitted",
            label_msgid='UWOshOIE_label_applicationFeeOK',
            description_msgid='UWOshOIE_help_applicationFeeOK',
            i18n_domain='UWOshOIE',
        ),
        schemata="OFFICE USE ONLY",
        read_permission="View",
        write_permission="UWOshOIE: Modify Office Use Only fields",
        required_by_state=['needsDirectorReview'],
        must_not_be=False
    ),

    BooleanField('UWSystemStatementOK',
        widget=BooleanWidget(
            label="UW System Statement of Responsibility Submitted",
            label_msgid='UWOshOIE_label_UWSystemStatementOK',
            description_msgid='UWOshOIE_help_UWSystemStatementOK',
            i18n_domain='UWOshOIE',
        ),
        schemata="OFFICE USE ONLY",
        read_permission="View",
        write_permission="UWOshOIE: Modify Office Use Only fields",
        required_by_state=['needsDirectorReview'],
        must_not_be=False
    ),

    BooleanField('UWOshkoshStatementOK',
        widget=BooleanWidget(
            label="UW Oshkosh Statement of Responsibility Submitted",
            label_msgid='UWOshOIE_label_UWOshkoshStatementOK',
            description_msgid='UWOshOIE_help_UWOshkoshStatementOK',
            i18n_domain='UWOshOIE',
        ),
        schemata="OFFICE USE ONLY",
        read_permission="View",
        write_permission="UWOshOIE: Modify Office Use Only fields",
        required_by_state=['needsDirectorReview'],
        must_not_be=False
    ),
    
    BooleanField('withdrawalRefund',
        widget=BooleanWidget(
            label="Withdrawal and Refund Form Submitted",
            label_msgid='UWOshOIE_label_withdrawalRefund',
            description_msgid='UWOshOIE_help_withdrawalRefund',
            i18n_domain='UWOshOIE',
        ),
        schemata="OFFICE USE ONLY",
        read_permission="View",
        write_permission="UWOshOIE: Modify Office Use Only fields",
        required_by_state=['needsDirectorReview'],
        must_not_be=False
    ),
    
    BooleanField('transcriptsOK',
        widget=BooleanWidget(
            label="Transcripts Submitted",
            label_msgid='UWOshOIE_label_transcriptsOK',
            description_msgid='UWOshOIE_help_transcriptsOK',
            i18n_domain='UWOshOIE',
        ),
        schemata="OFFICE USE ONLY",
        read_permission="View",
        write_permission="UWOshOIE: Modify Office Use Only fields",
        required_by_state=['needsDirectorReview'],
        must_not_be=False
    ),
        
    StringField('programSpecificMaterialsRequired',
        widget=SelectionWidget(
            label="Program-Specific Materials Required(Step II)?",
            label_msgid='UWOshOIE_label_programSpecificMaterialsRequired',
            description_msgid='UWOshOIE_help_programSpecificMaterialsRequired',
            i18n_domain='UWOshOIE',
            macro="selectioninline"
        ),
        schemata="OFFICE USE ONLY",
        read_permission="View",
        vocabulary=["Yes", "No", ''],
        required_by_state=['needsDirectorReview'],
        must_not_be=None,
        write_permission="UWOshOIE: Modify Office Use Only fields"
    ),
    
    BooleanField('programSpecificMaterialsOK',
        widget=BooleanWidget(
            label="Program-Specific Materials Submitted(Step II)",
            label_msgid='UWOshOIE_label_programSpecificMaterialsOK',
            description_msgid='UWOshOIE_help_programSpecificMaterialsOK',
            i18n_domain='UWOshOIE',
        ),
        schemata="OFFICE USE ONLY",
        read_permission="View",
        write_permission="UWOshOIE: Modify Office Use Only fields"
    ),
    
    StringField('specialStudentFormRequired',
        widget=SelectionWidget(
            label="Special Student Form Required",
            label_msgid='UWOshOIE_label_specialStudentFormRequired',
            description_msgid='UWOshOIE_help_specialStudentFormRequired',
            i18n_domain='UWOshOIE',
            macro="selectioninline"
        ),
        schemata="OFFICE USE ONLY",
        read_permission="View",
        vocabulary=["Yes", "No", ''],
        required_by_state=['needsDirectorReview'],
        must_not_be=None,
        write_permission="UWOshOIE: Modify Office Use Only fields"
    ),
    
    BooleanField('specialStudentFormOK',
        widget=BooleanWidget(
            label="Special Student Form Submitted",
            label_msgid='UWOshOIE_label_specialStudentFormOK',
            description_msgid='UWOshOIE_help_specialStudentFormOK',
            i18n_domain='UWOshOIE',
        ),
        schemata="OFFICE USE ONLY",
        read_permission="View",
        write_permission="UWOshOIE: Modify Office Use Only fields"
    ),

    StringField('creditOverloadFormRequired',
        widget=SelectionWidget(
            label="Credit Overload Form Required",
            label_msgid='UWOshOIE_label_creditOverloadFormRequired',
            description_msgid='UWOshOIE_help_creditOverloadFormRequired',
            i18n_domain='UWOshOIE',
            macro="selectioninline"
        ),
        schemata="OFFICE USE ONLY",
        read_permission="View",
        vocabulary=['Yes', 'No', ''],
        required_by_state=['needsDirectorReview'],
        must_not_be=None,
        write_permission="UWOshOIE: Modify Office Use Only fields"
    ),

    BooleanField('creditOverloadFormOK',
        widget=BooleanWidget(
            label="Credit Overload Form Submitted",
            label_msgid='UWOshOIE_label_creditOverloadFormOK',
            description_msgid='UWOshOIE_help_creditOverloadFormOK',
            i18n_domain='UWOshOIE',
        ),
        schemata="OFFICE USE ONLY",
        read_permission="View",
        write_permission="UWOshOIE: Modify Office Use Only fields"
    ),

    BooleanField('medicalOK',
        widget=BooleanWidget(
            label="Medical information is Submitted/Updated",
            label_msgid='UWOshOIE_label_medicalOK',
            description_msgid='UWOshOIE_help_medicalOK',
            i18n_domain='UWOshOIE',
        ),
        schemata="OFFICE USE ONLY",
        read_permission="View",
        write_permission="UWOshOIE: Modify Office Use Only fields",
        required_by_state=['seatAssigned'],
        must_be=True
    ),
    
    TextField('medicalForm',
        allowable_content_types=('text/plain',),
        widget=TextAreaWidget(
            label='Medical Form',
            label_msgid='UWOshOIE_label_medicalForm',
            description_msgid='UWOshOIE_help_medicalForm',
            i18n_domain='UWOshOIE',
            ),
        default_output_type='text/plain',
        schemata="OFFICE USE ONLY",
        read_permission="View",
        write_permission="UWOshOIE: Modify Office Use Only fields",
        searchable=True
    ),
    
    BooleanField('passportOK',
        widget=BooleanWidget(
            label="Passport information or receipt Submitted",
            label_msgid='UWOshOIE_label_passportOK',
            description_msgid='UWOshOIE_help_passportOK',
            i18n_domain='UWOshOIE',
        ),
        schemata="OFFICE USE ONLY",
        read_permission="View",
        write_permission="UWOshOIE: Modify Office Use Only fields",
        required_by_state=['seatAssigned'],
        must_be=True
    ),

    StringField('metPassportDeadline',
        widget=SelectionWidget(
            label="Passport Deadline Met",
            label_msgid='UWOshOIE_label_metPassportDeadline',
            description_msgid='UWOshOIE_help_metPassportDeadline',
            i18n_domain='UWOshOIE',
            macro="selectioninline"
        ),
        schemata="OFFICE USE ONLY",
        read_permission="View",
        vocabulary=["Yes", "No", ""],
        write_permission="UWOshOIE: Modify Office Use Only fields"
    ),

    StringField('programSpecificMaterialsRequiredStepIII',
        widget=SelectionWidget(
            label="Program-Specific Materials Required(Step III)?",
            label_msgid='UWOshOIE_label_programSpecificMaterialsRequired',
            description_msgid='UWOshOIE_help_programSpecificMaterialsRequired',
            i18n_domain='UWOshOIE',
            macro="selectioninline"
        ),
        schemata="OFFICE USE ONLY",
        read_permission="View",
        vocabulary=["Yes", "No", ""],
        write_permission="UWOshOIE: Modify Office Use Only fields"
    ),

    BooleanField('programSpecificMaterialsOKStepIII',
        widget=BooleanWidget(
            label="Program-Specific Materials Submitted(Step III)",
            label_msgid='UWOshOIE_label_programSpecificMaterialsOK',
            description_msgid='UWOshOIE_help_programSpecificMaterialsOK',
            i18n_domain='UWOshOIE',
        ),
        schemata="OFFICE USE ONLY",
        read_permission="View",
        write_permission="UWOshOIE: Modify Office Use Only fields"
    ),
    
    StringField('attendedOrientation',
        widget=SelectionWidget(
            label="Attended Orientation",
            label_msgid='UWOshOIE_label_attendedOrientation',
            description_msgid='UWOshOIE_help_attendedOrientation',
            i18n_domain='UWOshOIE',
            macro="selectioninline"
        ),
        schemata="OFFICE USE ONLY",
        read_permission="View",
        vocabulary=["Yes", "No", ""],
        write_permission="UWOshOIE: Modify Office Use Only fields"
    ),
    
    StringField('cisiDates',
        widget=StringWidget(
            label="Health Insurance Dates",
            description="Cultural Insurance Services International",
            label_msgid='UWOshOIE_label_cisiDates',
            description_msgid='UWOshOIE_help_cisiDates',
            i18n_domain='UWOshOIE',
        ),
        schemata="OFFICE USE ONLY",
        read_permission="View",
        write_permission="UWOshOIE: Modify Office Use Only fields"
    ),

    IntegerField('cisiNumberOfMonths',
        widget=IntegerWidget(
            label="Health Insurance Number of Months",
            description="Cultural Insurance Services International",
            label_msgid='UWOshOIE_label_cisiNumberOfMonths',
            description_msgid='UWOshOIE_help_cisiNumberOfMonths',
            i18n_domain='UWOshOIE',
        ),
        schemata="OFFICE USE ONLY",
        read_permission="View",
        write_permission="UWOshOIE: Modify Office Use Only fields"
    ),
    
    FloatField('programFee',
        widget=DecimalWidget(
            label="Program Fee",
            label_msgid='UWOshOIE_label_programFee',
            description_msgid='UWOshOIE_help_programFee',
            i18n_domain='UWOshOIE',
        ),
        schemata="OFFICE USE ONLY",
        read_permission="View",
        write_permission="UWOshOIE: Modify Office Use Only fields"
    ),
    
    FloatField('tuitionPayment',
        widget=DecimalWidget(
            label="Tuition Payment(student exchange only)",
            label_msgid='UWOshOIE_label_tuitionPayment',
            description_msgid='UWOshOIE_help_tuitionPayment',
            i18n_domain='UWOshOIE',
        ),
        schemata="OFFICE USE ONLY",
        read_permission="View",
        write_permission="UWOshOIE: Modify Office Use Only fields"
    ),
    
    StringField('depositOnTime',
        widget=SelectionWidget(
            label="Deposit Paid on Time",
            label_msgid='UWOshOIE_label_depositOnTime',
            description_msgid='UWOshOIE_help_depositOnTime',
            i18n_domain='UWOshOIE',
        ),
        schemata="OFFICE USE ONLY",
        read_permission="View",
        vocabulary=['Yes','No'],
        write_permission="UWOshOIE: Modify Office Use Only fields",
        must_be="Yes"
    ),

    StringField('payment2OnTime',
        widget=SelectionWidget(
            label="Final Payment Made on Time(except exchange students)",
            label_msgid='UWOshOIE_label_payment2OnTime',
            description_msgid='UWOshOIE_help_payment2OnTime',
            i18n_domain='UWOshOIE',
        ),
        schemata="OFFICE USE ONLY",
        read_permission="View",
        vocabulary=['Yes','No'],
        write_permission="UWOshOIE: Modify Office Use Only fields"
    ),

    StringField('applicationFeeRefund',
        widget=SelectionWidget(
            label="Application Fee Refunded",
            label_msgid='UWOshOIE_label_applicationFeeRefund',
            description_msgid='UWOshOIE_help_applicationFeeRefund',
            i18n_domain='UWOshOIE',
        ),
        schemata="OFFICE USE ONLY",
        read_permission="View",
        vocabulary=['Yes','No'],
        write_permission="UWOshOIE: Modify Office Use Only fields"
    ),
    
    StringField('foreignCourse1',
        widget=StringWidget(
            label="Foreign institution course 1",
            label_msgid='UWOshOIE_label_foreignCourse1',
            description_msgid='UWOshOIE_help_foreignCourse1',
            i18n_domain='UWOshOIE',
        ),
        schemata="OFFICE USE ONLY",
        read_permission="View",
        write_permission="UWOshOIE: Modify Office Use Only fields",
        searchable=True
    ),

    StringField('foreignCourse2',
        widget=StringWidget(
            label="Foreign institution course 2",
            label_msgid='UWOshOIE_label_foreignCourse2',
            description_msgid='UWOshOIE_help_foreignCourse2',
            i18n_domain='UWOshOIE',
        ),
        schemata="OFFICE USE ONLY",
        read_permission="View",
        write_permission="UWOshOIE: Modify Office Use Only fields",
        searchable=True
    ),

    StringField('foreignCourse3',
        widget=StringWidget(
            label="Foreign institution course 3",
            label_msgid='UWOshOIE_label_foreignCourse3',
            description_msgid='UWOshOIE_help_foreignCourse3',
            i18n_domain='UWOshOIE',
        ),
        schemata="OFFICE USE ONLY",
        read_permission="View",
        write_permission="UWOshOIE: Modify Office Use Only fields",
        searchable=True
    ),

    StringField('foreignCourse4',
        widget=StringWidget(
            label="Foreign institution course 4",
            label_msgid='UWOshOIE_label_foreignCourse4',
            description_msgid='UWOshOIE_help_foreignCourse4',
            i18n_domain='UWOshOIE',
        ),
        schemata="OFFICE USE ONLY",
        read_permission="View",
        write_permission="UWOshOIE: Modify Office Use Only fields",
        searchable=True
    ),

    StringField('foreignCourse5',
        widget=StringWidget(
            label="Foreign institution course 5",
            label_msgid='UWOshOIE_label_foreignCourse5',
            description_msgid='UWOshOIE_help_foreignCourse5',
            i18n_domain='UWOshOIE',
        ),
        schemata="OFFICE USE ONLY",
        read_permission="View",
        write_permission="UWOshOIE: Modify Office Use Only fields",
        searchable=True
    ),

    StringField('foreignCourse6',
        widget=StringWidget(
            label="Foreign institution course 6",
            label_msgid='UWOshOIE_label_foreignCourse6',
            description_msgid='UWOshOIE_help_foreignCourse6',
            i18n_domain='UWOshOIE',
        ),
        schemata="OFFICE USE ONLY",
        read_permission="View",
        write_permission="UWOshOIE: Modify Office Use Only fields",
        searchable=True
    ),
    
    BooleanField('papersOK',
        widget=BooleanWidget(
            label="Papers information is OK",
            label_msgid='UWOshOIE_label_papersOK',
            description_msgid='UWOshOIE_help_papersOK',
            i18n_domain='UWOshOIE',
        ),
        schemata="OFFICE USE ONLY",
        read_permission="View",
        write_permission="UWOshOIE: Modify Office Use Only fields"
    ),

    BooleanField('noMoreMaterials',
        widget=BooleanWidget(
            label='No More Materials',
            label_msgid='UWOshOIE_label_noMoreMaterials',
            description_msgid='UWOshOIE_help_noMoreMaterials',
            i18n_domain='UWOshOIE',
        ),
        schemata="OFFICE USE ONLY",
        read_permission="View",
        write_permission="UWOshOIE: Modify Office Use Only fields"
    ),

    BooleanField('programMaterials',
        widget=BooleanWidget(
            label='Program Materials',
            label_msgid='UWOshOIE_label_programMaterials',
            description_msgid='UWOshOIE_help_programMaterials',
            i18n_domain='UWOshOIE',
        ),
        schemata="OFFICE USE ONLY",
        read_permission="View",
        write_permission="UWOshOIE: Modify Office Use Only fields"
    ),

    IntegerField('programFee2',
        widget=IntegerWidget(
            label='Program Fee 2',
            label_msgid='UWOshOIE_label_programFee2',
            description_msgid='UWOshOIE_help_programFee2',
            i18n_domain='UWOshOIE',
        ),
        schemata="OFFICE USE ONLY",
        read_permission="View",
        write_permission="UWOshOIE: Modify Office Use Only fields"
    ),
),
)

OIEStudentApplication_schema = BaseSchema + \
    schema

class OIEStudentApplication(ATCTContent, HistoryAwareMixin):
    security = ClassSecurityInfo()
    __implements__ = (ATCTContent.__implements__,
                      HistoryAwareMixin.__implements__
                     )


    # This name appears in the 'add' box
    archetype_name             = 'OIE Student Application'
    meta_type                  = 'OIEStudentApplication'
    portal_type                = 'OIEStudentApplication'
    allowed_content_types      = []
    filter_content_types       = 0
    global_allow               = 1
    allow_discussion           = 0
    immediate_view             = 'base_view'
    default_view               = 'base_view'
    suppl_views                = ()
    typeDescription            = "OIE Student Application"
    typeDescMsgId              = 'description_edit_oiestudentapplication'

    schema = OIEStudentApplication_schema

#    def at_post_edit_script(self):
#        new_id = self.generateNewId()
#        
#        if new_id != self.id:
#            parent = aq_parent(aq_inner(self))
#            if parent is not None:
#                
#                while new_id in parent.objectIds():
#                    try:
#                        version = int(new_id[len(new_id)-1])
#                        new_id[len(new_id)] = str(version+1)
#                    except:
#                        new_id = new_id + "-1"
#                
#                # See Referenceable, keep refs on what is a move/rename
#                self._v_cp_refs = 1
#                try:
#                    parent.manage_renameObject(self.id, new_id)
#                except:
#                    #could not rename object...
#                    pass
#            self._setId(new_id)
#    def at_post_edit_script(self):
#        new_id = self.generateNewId()
#        
#        if new_id != self.id:
#           parent = aq_parent(aq_inner(self))
#            if parent is not None:
#                
#                while new_id in parent.objectIds():
#                    try:
#                        version = int(new_id[len(new_id)-1])
#                        new_id[len(new_id)] = str(version+1)
#                    except:
#                        new_id = new_id + "-1"
#                
#                    # See Referenceable, keep refs on what is a move/rename
#                    self._v_cp_refs = 1
#                    try:
#                        parent.manage_renameObject(self.id, new_id)
#                    except:
#                        #could not rename object...
#                        pass
#             self._setId(new_id)


    def generateNewId(self):
         plone_tool = getToolByName(self, 'plone_utils', None)

         programName = ""
         try:
             programName = self.getProgramName().Title()
         except:
             pass

         new_id = plone_tool.normalizeString(self.getFullName() + "-" + 
                                             programName + "-" +
                                             "(" + self.getProgramSemester() + "-" + str(self.getProgramYear()) + ")")

         return new_id

    def getFullName(self):
        return self.getFirstName() + " " + self.getMiddleName() + " " + self.getLastName()

    def getMemberEmail (self):
        pm = getToolByName (self, "portal_membership")
        m = pm.getAuthenticatedMember()
        return m.getProperty('email', "")

    def getProgramNameAsString(self):
        try:
            return self.getProgramName().Title()
        except:
            return ''

registerType(OIEStudentApplication,PROJECTNAME)




