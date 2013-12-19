from zope.component import ComponentLookupError
try:
    # Plone < 4.3
    from zope.app.component.hooks import getSite
except ImportError:
    # Plone >= 4.3
    from zope.component.hooks import getSite

from Acquisition import aq_parent
from Products.PloneFormGen.interfaces import IPloneFormGenForm
from .interfaces import IPfgSoupAdapter
from .storage import PfgCatalogFactory

import logging

logger = logging.getLogger('collective.pfg.soup.subscribers')


def create_catalogfactory(obj, event):
    sm = getSite().getSiteManager()
    sm.registerUtility(factory=PfgCatalogFactory, name=obj._soup_name)


def rebuild_catalog(obj, event):
    parent = aq_parent(obj)
    while True:
        if not parent or IPloneFormGenForm.providedBy(parent):
            break
        parent = aq_parent(parent)
    if parent is None:
        return
    for name in parent.contentIds():
        sub = parent[name]
        if IPfgSoupAdapter.providedBy(sub):
            try:
                sub.get_soup().rebuild()
            except ComponentLookupError:
                logger.warn('Can not fetch a soup for %s' % obj)
