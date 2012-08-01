from zope.interface import implements
from archetypes.schemaextender.interfaces import (
    IOrderableSchemaExtender,
    IBrowserLayerAwareExtender,
)
from archetypes.schemaextender.field import ExtensionField
from Products.Archetypes import atapi
from Products.Archetypes.utils import OrderedDict
from .interfaces import IPfgSoupLayer


class BooleanExtensionField(ExtensionField, atapi.BooleanField):
    """BooleanField for use within schemaextender."""


class PfgFieldSoupExtender(object):
    """Schema extender for PfgFields adding storage specific settings.
    """

    fields = [
        BooleanExtensionField('pfgsoup_show',
            schemata='soupsettings',
            default=True,
            mode="w",
            required=False,
            widget=atapi.BooleanWidget(
                label=u"Show in Table",
                description=u"Show column with data of field in data table",
            )
        ),
        BooleanExtensionField('pfgsoup_export',
            schemata='soupsettings',
            default=True,
            mode="w",
            required=False,
            widget=atapi.BooleanWidget(
                label=u"Export",
                description=u"Export column with data of field in csv",
            )
        ),
    ]

    implements(IOrderableSchemaExtender, IBrowserLayerAwareExtender)

    layer = IPfgSoupLayer

    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self.fields

    def getOrder(self, original):
        neworder = OrderedDict()
        for schemata in original.keys():
            neworder[schemata] = original[schemata]
        return neworder
