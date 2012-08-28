from zope.interface import implementer
from zope.component import queryAdapter
from Acquisition import aq_parent
from repoze.catalog.catalog import Catalog
from repoze.catalog.indexes.field import CatalogFieldIndex
from souper.interfaces import ICatalogFactory
from souper.soup import NodeAttributeIndexer
from .config import auto_field_ids
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
        for field_id in auto_field_ids():
            indexer = NodeAttributeIndexer(field_id)
            catalog[field_id] = CatalogFieldIndex(indexer)
        return catalog
