from Products.CMFCore.permissions import setDefaultRoles

PROJECTNAME = 'collective.pfg.soup'
ADD_PERMISSIONS = {
    'SoupAdapter': 'collective.pfg.soup: Add SoupAdapter',
}
setDefaultRoles(ADD_PERMISSIONS['SoupAdapter'],
                ('Manager', 'Owner', 'Contributor', 'Site Administrator')
)

AUTOFIELDS = ['created', 'last_modified', 'userid']


def auto_field_ids():
    for field_suffix in AUTOFIELDS:
        yield '_auto_%s' % field_suffix
