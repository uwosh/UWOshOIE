#really only for testing
settings_folder = {
    'id': 'uwoshoie-settings', 
    'title': 'UWOshOIE Settings', 
    'type_name': 'Folder'
}
message_template_folder = {
    'id': 'message-templates', 
    'title': 'Email Message Templates', 
    'type_name': 'UWOshOIEEmailTemplateFolder'
}
template_addcomment = { 
    'id': 'emailMessageTemplate_addComment', 
    'title':'Email Template Add Comment',
    'transition': 'addComment',
    'sendEmail': True,
    'ccAddresses': ['oie@uwosh.edu'],
    'emailText': 'Transition',
    'type_name': 'UWOshOIEEmailTemplate',
}
template_admitconditionally = { 
    'type_name': 'UWOshOIEEmailTemplate',
    'id': 'emailMessageTemplate_admitConditionally', 
    'title':'Email Template Admit Conditionally', 
    'transition': 'admitConditionally',
    'sendEmail': True,
    'ccAddresses': ['oie@uwosh.edu'],
    'emailText': 'Transition'
}
template_assertreadyforcondtionaladmit = {  
    'type_name': 'UWOshOIEEmailTemplate',
    'id': 'emailMessageTemplate_assertReadyForConditionalAdmit', 
    'title':'Email Template Ready For Conditional Admit', 
    'transition': 'assertReadyForConditionalAdmit',
    'sendEmail': True,
    'ccAddresses': ['oie@uwosh.edu'],
    'emailText': 'Transition'
}
template_assignseatfailure = {      
    'type_name': 'UWOshOIEEmailTemplate',
    'id': 'emailMessageTemplate_assignseatfailure', 
    'title':'Email Template Assign Seat Failure', 
    'transition': 'assignSeat',
    'sendEmail': True,
    'sendEmailOnFailure': True,
    'ccAddresses': ['oie@uwosh.edu'],
    'emailText': 'Transition'
}
template_facultyapproves = {    
    'type_name': 'UWOshOIEEmailTemplate',
    'id': 'emailMessageTemplate_facultyApproves', 
    'title':'Email Template Faculty Approves', 
    'transition': 'facultyApproves',
    'sendEmail': True,
    'sendEmailOnFailure': False,
    'ccAddresses': ['oie@uwosh.edu'],
    'emailText': 'Transition'
}
template_recheckforfahold = {   
    'type_name': 'UWOshOIEEmailTemplate',
    'id': 'emailMessageTemplate_recheckForFAHold', 
    'title':'Email Template Recheck For FA Hold', 
    'transition': 'recheckForFAHold',
    'sendEmail': True,
    'sendEmailOnFailure': False,
    'ccAddresses': ['oie@uwosh.edu'],
    'emailText': 'Transition'
}
template_withdraw = {   
    'type_name': 'UWOshOIEEmailTemplate',
    'id': 'emailMessageTemplate_withdraw', 
    'title':'Email Template Withdraw', 
    'transition': 'withdraw',
    'sendEmail': True,
    'sendEmailOnFailure': False,
    'ccAddresses': ['oie@uwosh.edu'],
    'emailText': 'Transition'
}
template_submit = {   
    'type_name': 'UWOshOIEEmailTemplate',
    'id': 'emailMessageTemplate_submit', 
    'title':'Email Template Submit', 
    'transition': 'submit',
    'sendEmail': True,
    'sendEmailOnFailure': False,
    'ccAddresses': ['oie@uwosh.edu'],
    'emailText': 'Transition'
}
template_archive = {   
    'type_name': 'UWOshOIEEmailTemplate',
    'id': 'emailMessageTemplate_archive', 
    'title':'Email Template Archive', 
    'transition': 'archive',
    'sendEmail': True,
    'sendEmailOnFailure': False,
    'ccAddresses': ['oie@uwosh.edu'],
    'emailText': 'Transition'
}
template_waitForPrintMaterials = {   
    'type_name': 'UWOshOIEEmailTemplate',
    'id': 'emailMessageTemplate_waitForPrintedMaterials', 
    'title':'Email Template waitForPrintedMaterials', 
    'transition': 'waitForPrintedMaterials',
    'sendEmail': True,
    'sendEmailOnFailure': False,
    'ccAddresses': ['oie@uwosh.edu'],
    'emailText': 'Transition'
}     
template_sendForDirectorReview = {   
    'type_name': 'UWOshOIEEmailTemplate',
    'id': 'emailMessageTemplate_sendForDirectorReview', 
    'title':'Email Template sendForDirectorReview', 
    'transition': 'sendForDirectorReview',
    'sendEmail': True,
    'sendEmailOnFailure': False,
    'ccAddresses': ['oie@uwosh.edu'],
    'description': 'To avoid sending out a message, enter just a space in the body text.',
    'emailText': 'Transition'
}             
template_sendForProgramManagerReview = { 
    'type_name': 'UWOshOIEEmailTemplate',  
    'id': 'emailMessageTemplate_sendForProgramManagerReview', 
    'title':'Email Template sendForProgramManagerReview', 
    'transition': 'sendForProgramManagerReview',
    'sendEmail': True,
    'sendEmailOnFailure': False,
    'ccAddresses': ['oie@uwosh.edu'],
    'description': 'To avoid sending out a message, enter just a space in the body text.',
    'emailText': 'Transition'
}
template_decline = {   
    'type_name': 'UWOshOIEEmailTemplate',
    'id': 'emailMessageTemplate_decline', 
    'title':'Email Template decline', 
    'transition': 'decline',
    'sendEmail': True,
    'sendEmailOnFailure': False,
    'ccAddresses': ['oie@uwosh.edu'],
    'description': 'To avoid sending out a message, enter just a space in the body text.',
    'emailText': 'Transition'
}
template_addToWaitlist = {   
    'type_name': 'UWOshOIEEmailTemplate',
    'id': 'emailMessageTemplate_addToWaitlist', 
    'title':'Email Template addToWaitlist', 
    'transition': 'addToWaitlist',
    'sendEmail': True,
    'sendEmailOnFailure': False,
    'ccAddresses': ['oie@uwosh.edu'],
    'description': 'To avoid sending out a message, enter just a space in the body text.',
    'emailText': 'Transition'
}
template_admitConditionally = {   
    'type_name': 'UWOshOIEEmailTemplate',
    'id': 'emailMessageTemplate_admitConditionally', 
    'title':'Email Template admitConditionally', 
    'transition': 'admitConditionally',
    'sendEmail': True,
    'sendEmailOnFailure': False,
    'ccAddresses': ['oie@uwosh.edu'],
    'description': 'To avoid sending out a message, enter just a space in the body text.',
    'emailText': 'Transition'
}  
template_assignSeat = {   
    'type_name': 'UWOshOIEEmailTemplate',
    'id': 'emailMessageTemplate_assignSeat', 
    'title':'Email Template assignSeat', 
    'transition': 'assignSeat',
    'sendEmail': True,
    'sendEmailOnFailure': False,
    'ccAddresses': ['oie@uwosh.edu'],
    'description': 'To avoid sending out a message, enter just a space in the body text.',
    'emailText': 'Transition'
}      
template_manageDeadlines = {   
    'type_name': 'UWOshOIEEmailTemplate',
    'id': 'emailMessageTemplate_manageDeadlines', 
    'title':'Email Template manageDeadlines', 
    'transition': 'manageDeadlines',
    'sendEmail': True,
    'sendEmailOnFailure': False,
    'ccAddresses': ['oie@uwosh.edu'],
    'description': 'To avoid sending out a message, enter just a space in the body text.',
    'emailText': 'Transition'
}
template_manageDeadlines = {   
    'type_name': 'UWOshOIEEmailTemplate',
    'id': 'emailMessageTemplate_manageDeadlines', 
    'title':'Email Template manageDeadlines', 
    'transition': 'manageDeadlines',
    'sendEmail': True,
    'sendEmailOnFailure': True,
    'ccAddresses': ['oie@uwosh.edu'],
    'description': 'To avoid sending out a message, enter just a space in the body text.',
    'emailText': 'Transition'
}
template_sendForFacultyReview = {   
    'type_name': 'UWOshOIEEmailTemplate',
    'id': 'emailMessageTemplate_sendForFacultyReview', 
    'title':'Email Template sendForFacultyReview', 
    'transition': 'sendForFacultyReview',
    'sendEmail': True,
    'sendEmailOnFailure': False,
    'ccAddresses': ['oie@uwosh.edu'],
    'description': 'To avoid sending out a message, enter just a space in the body text.',
    'emailText': 'Transition'
}
template_holdForFAIncomplete = {   
    'type_name': 'UWOshOIEEmailTemplate',
    'id': 'emailMessageTemplate_holdForFAIncomplete', 
    'title':'Email Template holdForFAIncomplete', 
    'transition': 'holdForFAIncomplete',
    'sendEmail': True,
    'sendEmailOnFailure': False,
    'ccAddresses': ['oie@uwosh.edu'],
    'description': 'To avoid sending out a message, enter just a space in the body text.',
    'emailText': 'Transition'
}    
template_declineFromFacultyReview = {   
    'type_name': 'UWOshOIEEmailTemplate',
    'id': 'emailMessageTemplate_declineFromFacultyReview', 
    'title':'Email Template declineFromFacultyReview', 
    'transition': 'declineFromFacultyReview',
    'sendEmail': True,
    'sendEmailOnFailure': False,
    'ccAddresses': ['oie@uwosh.edu'],
    'description': 'To avoid sending out a message, enter just a space in the body text.',
    'emailText': 'Transition'
}
template_approveForFA = {   
    'type_name': 'UWOshOIEEmailTemplate',
    'id': 'emailMessageTemplate_approveForFA', 
    'title':'Email Template approveForFA', 
    'transition': 'approveForFA',
    'sendEmail': True,
    'sendEmailOnFailure': False,
    'ccAddresses': ['oie@uwosh.edu'],
    'description': 'To avoid sending out a message, enter just a space in the body text.',
    'emailText': 'Transition'
}
                                     
settings_folder['children'] = [message_template_folder]
message_template_folder['children'] = [template_addcomment, template_admitconditionally, template_assertreadyforcondtionaladmit,
            template_assignseatfailure, template_facultyapproves, template_recheckforfahold, template_withdraw, template_submit,
            template_archive, template_waitForPrintMaterials, template_sendForDirectorReview, template_sendForProgramManagerReview,
            template_decline, template_addToWaitlist, template_admitConditionally, template_assignSeat, template_manageDeadlines,
            template_sendForFacultyReview, template_holdForFAIncomplete, template_declineFromFacultyReview, template_approveForFA]

