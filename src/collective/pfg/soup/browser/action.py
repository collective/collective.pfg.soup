import transaction
from zExceptions import Redirect
from Products.Five import BrowserView
from ..interfaces import IPfgSoupAdapter

class BaseView(BrowserView):

    def get_soupadapter(self):
        for name in self.context.contentIds():
            sub = self.context[name]
            if IPfgSoupAdapter.providedBy(sub):
                return sub
        return None

class CheckView(BaseView):
    """check for a soup
    """

    def has_soupadapter(self):
        return self.get_soupadapter() is not None

    def get_soupadapter_url(self):
        sa = self.get_soupadapter()
        if sa is None:
            return sa
        return sa.absolute_url()


class ThanksPageSelectorView(BaseView):

    def __call__(self):
        sa = self.get_soupadapter()
        if sa is None:
            return self.context.getThanksPage()
        iid = self.request.cookies.get('PFGSOUP_EDIT')
        if iid:
            # return sa.getId()
            # rendering doesn not work for some resons ... wtf??
            # so workaround: 
            transaction.commit()
            raise Redirect(sa.absolute_url())
        return self.context.getThanksPage()
