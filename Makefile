DEVDIR=/Users/Kimtheman/src/UWOshOIE
INSTALLDIR=/Applications/Plone2/Sites/Default/Products/UWOshOIE

install:
	rm -rf $(INSTALLDIR)
	cp -pr $(DEVDIR) $(INSTALLDIR)

