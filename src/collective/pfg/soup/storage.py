from zope.interface import implementer
from zope.component import queryAdapter
from Acquisition import aq_parent
from repoze.catalog.catalog import Catalog
from souper.interfaces import ICatalogFactory
from .interfaces import IAddPfgIndex
from .adapter import SoupAdapter


@implementer(ICatalogFactory)
class PfgCatalogFactory(object):

    def __call__(self, context):
        if not isinstance(context, SoupAdapter):
            raise ValueError('Current context must be a SoupAdapter')
        pfg = aq_parent(context)
        catalog = Catalog()
        for field in pfg._getFieldObjects():
            pfgindexadder = queryAdapter(field, IAddPfgIndex)
            if pfgindexadder is None:
                continue
            pfgindexadder(catalog)
        return catalog
