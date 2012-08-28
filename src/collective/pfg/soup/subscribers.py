from zope.app.component.hooks import getSite
from .storage import PfgCatalogFactory


def create_catalogfactory(obj, event):
    sm = getSite().getSiteManager()
    sm.registerUtility(factory=PfgCatalogFactory, name=obj._soup_name)


def rebuild_catalog(obj, event):

    # check if adapter is present
    # if not return
    # get soup
    # soup.rebuild()
    pass
