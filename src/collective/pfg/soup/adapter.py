from zope.interface import implementer
from AccessControl import ClassSecurityInfo
from Products.Archetypes.public import Schema
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

import logging
logger = logging.getLogger("PloneFormGen")


@implementer(IPfgSoupAdapter)
class SoupAdapter(FormActionAdapter):
    """A form action adapter storing form input data in a soup.
    """

    schema = FormAdapterSchema.copy() + Schema((
    ))

    meta_type = 'SoupAdapter'

    security = ClassSecurityInfo()

    @property
    def _soup_name(self):
        return 'PFGSOUP%s' % self.UID()

    def get_soup(self):
        return get_soup(self._soup_name, self)

    def onSuccess(self, fields, REQUEST=None, loopstop=False):
        """
        saves data.
        """
        soup = self.get_soup()
        data = OOBTNode()
        for field in fields:
            if field.isLabel():
                continue
            field_name = field.fgField.getName()
            if field.isFileField():
                file_value = REQUEST.form.get('%s_file' % field_name)
                raise NotImplementedError('Not Yet Done')
            value = REQUEST.form.get(field_name, '')
            if not isinstance(value, basestring):
                value = str(value)
            data.attrs[field_name] = value
        soup.add(data)

registerATCT(SoupAdapter, PROJECTNAME)
