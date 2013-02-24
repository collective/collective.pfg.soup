import json
from Acquisition import aq_parent
from AccessControl import getSecurityManager
from Products.Five import BrowserView
from repoze.catalog.query import Eq
from ..interfaces import IPfgSoupAdapter

class EditData(BrowserView):

    def _get_data(self, record):
        data = {}
        for name in record.attrs:
            if name.startswith('_auto_'):
                continue
            data[name] = record.attrs[name]
            # XXX binary data not handled
        return data

    def __call__(self):
        soup = self.context.get_soup()
        iid = int(self.request.get('iid'))
        record = soup.get(iid)
        result = dict()
        result['data'] = self._get_data(record)
        result['url'] = aq_parent(self.context).absolute_url()
        return json.dumps(result)


class ReeditData(EditData):

    def failed(self):
        return json.dumps(dict(status='failed'))

    def get_soupadapter(self):
        for name in self.context.contentIds():
            sub = self.context[name]
            if IPfgSoupAdapter.providedBy(sub):
                return sub
        return None

    def __call__(self):
        sa = self.get_soupadapter()
        if not sa or not sa.getField('reedit').get(sa):
            return self.failed()
        sm = getSecurityManager()
        user = sm.getUser()
        if user.has_role('Anonymous'):
            return self.failed()
        userid = user.getId()
        soup = sa.get_soup()
        result = soup.query(Eq(u'_auto_userid', userid))
        record = result.next()
        if not record:
            return self.failed()
        result = dict()
        result['data'] = self._get_data(record)
        result['url'] = self.context.absolute_url()
        result['intid'] = str(record.intid)
        result['status'] = 'ok'
        return json.dumps(result)


