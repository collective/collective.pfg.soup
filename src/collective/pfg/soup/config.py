from Products.CMFCore.permissions import setDefaultRoles

PROJECTNAME = 'collective.pfg.soup'
ADD_PERMISSIONS = {
    'SoupAdapter': 'collective.pfg.soup: Add SoupAdapter',
}
setDefaultRoles(ADD_PERMISSIONS['SoupAdapter'],
                ('Manager', 'Owner', 'Contributor', 'Site Administrator')
)
