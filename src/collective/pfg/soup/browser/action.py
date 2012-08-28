from Products.Five import BrowserView
from ..interfaces import IPfgSoupAdapter


class CheckView(BrowserView):
    """check for a soup
    """

    def has_soupadapter(self):
        return self.get_soupadapter_url() is not None

    def get_soupadapter_url(self):
        for name in self.context.contentIds():
            sub = self.context[name]
            if IPfgSoupAdapter.providedBy(sub):
                return sub.absolute_url()
        return None
