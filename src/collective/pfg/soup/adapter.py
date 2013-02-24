from bda.calendar.base.timezone import tzawarenow
from persistent.list import PersistentList
from zope.interface import implementer
from AccessControl import (
    ClassSecurityInfo,
    getSecurityManager,
)
from Products.Archetypes import atapi
from Products.ATContentTypes.content.base import registerATCT
from Products.PloneFormGen.content.actionAdapter import (
    FormActionAdapter,
    FormAdapterSchema,
)
from node.ext.zodb import OOBTNode
from souper.soup import get_soup
from collective.pfg.soup import _
from collective.pfg.soup.config import PROJECTNAME
from .interfaces import IPfgSoupAdapter
from .config import (
    AUTOFIELDS,
)

import logging
logger = logging.getLogger("PloneFormGen")

atfields = list()

atfields.append(atapi.BooleanField('reedit',
        schemata='default',
        default=False,
        mode="w",
        required=False,
        widget=atapi.BooleanWidget(
            label=u"Auto re-edit own form data",
            description=u"Users  are shown their own form data on subsequent "
                        u"visits in order to change/edit it.",
        )
))

for aid in AUTOFIELDS:
    atfields.append(atapi.BooleanField('show_%s' % aid,
            schemata='default',
            default=False,
            mode="w",
            required=False,
            widget=atapi.BooleanWidget(
                label=u"Show %s" % aid.replace('_', ' ').title(),
                description=u"Show data column in table or not?",
            )
    ),)
    atfields.append(atapi.BooleanField('export_%s' % aid,
            schemata='default',
            default=False,
            mode="w",
            required=False,
            widget=atapi.BooleanWidget(
                label=u"Export %s" % aid.replace('_', ' ').title(),
                description=u"Export data column in CSV-file or not?",
            )
    ),)


@implementer(IPfgSoupAdapter)
class SoupAdapter(FormActionAdapter):
    """A form action adapter storing form input data in a soup.
    """

    schema = FormAdapterSchema.copy() + atapi.Schema(atfields)

    meta_type = 'SoupAdapter'

    security = ClassSecurityInfo()

    def exclude_from_nav(self):
        return True

    @property
    def _soup_name(self):
        return 'PFGSOUP%s' % self.UID()

    def get_soup(self):
        return get_soup(self._soup_name, self)

    def onSuccess(self, fields, REQUEST=None, loopstop=False):
        """
        saves data.
        """
        now = tzawarenow()
        soup = self.get_soup()
        modified_fields = list()
        iid = self.REQUEST.cookies.get('PFGSOUP_EDIT', None)
        if iid:
            iid = int(iid)
            data = soup.get(iid)
        else:
            data = OOBTNode()
        for field in fields:
            if field.isLabel():
                continue
            field_name = field.getFieldFormName()
            if field.isFileField():
                file_value = REQUEST.form.get('%s_file' % field_name)
                raise NotImplementedError('FileField Not Yet Done')
            value = REQUEST.form.get(field_name, '')
            if iid:
                if data.attrs.get(field_name, None) == value:
                    continue
                modified_fields.append(field_name)
            data.attrs[field_name] = value
        sm = getSecurityManager()
        if iid:
            if modified_fields:
                data.attrs['_auto_last_modified'] = now
                log = {}
                log['user'] = sm.getUser().getId()
                log['date'] = now
                log['fields'] = modified_fields
                if '_auto_log' not in data.attrs:
                    data.attrs['_auto_log'] = PersistentList()
                data.attrs['_auto_log'].append(log)
            self.REQUEST.response.expireCookie('PFGSOUP_EDIT', path='/')
            # XXX redirect to table
            # self.REQUEST.response.redirect(...)
            return
        data.attrs['_auto_created'] = now
        data.attrs['_auto_last_modified'] = now
        data.attrs['_auto_userid'] = sm.getUser().getId()
        data.attrs['_auto_log'] = PersistentList()
        soup.add(data)

registerATCT(SoupAdapter, PROJECTNAME)
