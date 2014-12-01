## Script (Python) "expandTemplateMacros"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=templateText
##title=
##
# Expands any macros found in the given string, and returns the final string.
# Macros are of the form %%MACRONAME%%.
templateText.replace('%%OIEEMAIL%%','oie@uwosh.edu')
templateText.replace('%%OIEWEBSITE%%','http://www.uwosh.edu/OIE')
return templateText

