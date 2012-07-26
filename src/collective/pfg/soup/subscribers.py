from zope.app.component.hooks import getSite
from .storage import PfgCatalogFactory


def create_catalogfactory(obj, event):
    sm = getSite().getSiteManager()
    sm.registerUtility(factory=PfgCatalogFactory, name=obj._soup_name)
