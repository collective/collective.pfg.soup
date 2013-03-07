from Products.Five import BrowserView


class RemoveEntryView(BrowserView):

    def __call__(self):
        soup = self.context.get_soup()
        iid = int(self.request.form.get('iid'))
        del soup[soup.get(iid)]
        self.request.response.redirect(self.context.absolute_url())
        return 'redirect'
