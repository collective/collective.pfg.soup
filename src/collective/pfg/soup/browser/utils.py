from Products.Five import BrowserView


class UtilsView(BrowserView):

    def rebuild(self):
        soup = self.context.get_soup()
        res = soup.rebuild()
        return u"Rebuild Done: %s" % res
