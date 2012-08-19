import json
from Acquisition import aq_parent
from Products.Five import BrowserView


class EditData(BrowserView):

    def __call__(self):
        soup = self.context.get_soup()
        iid = int(self.request.get('iid'))
        record = soup.storage.data[iid]
        data = {}
        for name in record.attrs:
            if name.startswith('_auto_'):
                continue
            data[name] = record.attrs[name]
            # XXX binary data not handled
        result = dict(data=data)
        result['url'] = aq_parent(self.context).absolute_url()
        return json.dumps(data)
