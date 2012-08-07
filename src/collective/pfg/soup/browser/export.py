import csv
import datetime
from StringIO import StringIO
from .table import TableView


class DialectExcelWithColons(csv.excel):
    delimiter = ';'

csv.register_dialect('excel-colon', DialectExcelWithColons)


class CSVView(TableView):

    enabled_field = 'pfgsoup_export'

    def __call__(self):
        """csv with soupdata.
        """
        now = datetime.datetime.now()
        soup = self.context.get_soup()
        sio = StringIO()
        ex = csv.writer(sio, dialect='excel-colon')
        labels = [_[0] for _ in self.columns()]
        attrs = [_[1] for _ in self.columns()]
        ex.writerow(labels)
        iids = soup.catalog['_auto_created'].sort(soup.storage.data.keys())
        for iid in iids:
            record = soup.storage.data[iid]
            values = [record.attrs.get(_, '') for _ in attrs]
            ex.writerow(values)
        filename = now.strftime('%Y-%m-%D_%H-%M-%S.csv')
        filename = '%s_%s' % (self.context.getId(), filename)
        self.request.response.setHeader('Content-Type', 'text/csv')
        self.request.response.setHeader('Content-Disposition',
                                        'attachment; filename=%s' % filename)
        return sio.getvalue().decode('utf8')
