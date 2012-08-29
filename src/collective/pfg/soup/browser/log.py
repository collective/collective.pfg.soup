from Products.Five import BrowserView


class LogOverlayView(BrowserView):

    def logentries(self):
        soup = self.context.get_soup()
        iid = int(self.request.form.get('iid'))
        record = soup.get(iid)
        return record.attrs.get('_auto_log', {})
