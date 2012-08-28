from zope.interface import implementer
from repoze.catalog.indexes.field import CatalogFieldIndex
from repoze.catalog.indexes.text import CatalogTextIndex
from repoze.catalog.indexes.keyword import CatalogKeywordIndex
from souper.soup import NodeAttributeIndexer
from .interfaces import IAddPfgIndex


@implementer(IAddPfgIndex)
class BaseIndexCreator(object):

    def __init__(self, field):
        self.field = field

    def __call__(self, catalog):
        field_id = self.field.getId()
        indexer = NodeAttributeIndexer(field_id)
        catalog[field_id] = self.create(indexer)
        sort_index = self.create_sort(indexer)
        if sort_index is None:
            return
        sort_id = '_sort_%s' % field_id
        catalog[sort_id] = sort_index

    def create(self, indexer):
        raise NotImplementedError('Base class only')

    def create_sort(self, indexer):
        return None


class FieldIndexCreator(BaseIndexCreator):

    def create(self, indexer):
        return CatalogFieldIndex(indexer)


class TextIndexCreator(BaseIndexCreator):

    def create(self, indexer):
        # XXX use txng here if available
        return CatalogTextIndex(indexer)

    def create_sort(self, indexer):
        return CatalogFieldIndex(indexer)


class KeywordIndexCreator(BaseIndexCreator):

    def create(self, indexer):
        return CatalogKeywordIndex(indexer)

    def create_sort(self, indexer):
        return CatalogFieldIndex(indexer)
