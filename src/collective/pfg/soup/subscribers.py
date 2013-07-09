try:
    # Plone < 4.3
    from zope.app.component.hooks import setSite
except ImportError:
    # Plone >= 4.3
    from zope.component.hooks import setSite  

from Acquisition import aq_parent
from Products.PloneFormGen.interfaces import IPloneFormGenForm
from .interfaces import IPfgSoupAdapter
from .storage import PfgCatalogFactory


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
            sub.get_soup().rebuild()
