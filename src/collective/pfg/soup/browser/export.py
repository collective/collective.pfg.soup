import csv
import datetime
from StringIO import StringIO
from .table import TableView


class DialectExcelWithColons(csv.excel):
    delimiter = ';'

csv.register_dialect('excel-colon', DialectExcelWithColons)


class CSVView(TableView):

    enabled_field = 'pfgsoup_export'
    enabled_auto_prefix = 'export'

    def __call__(self):
        """csv with soupdata.
        """
        now = datetime.datetime.now()
        columns = self.columns()
        soup = self.context.get_soup()
        sio = StringIO()
        ex = csv.writer(sio, dialect='excel-colon')
        labels = [columns[_]['label'] for _ in columns]
        ex.writerow([_.encode('utf8') for _ in labels])
        iids = soup.catalog['_auto_created'].sort(soup.storage.data.keys())
        for iid in iids:
            record = soup.storage.data[iid]
            values = []
            for name in columns.keys():
                value = record.attrs.get(name, '')
                if isinstance(value, list):
                    value = ', '.join(value)
                values.append(value)
            ex.writerow(values)
        filename = now.strftime('%Y-%m-%D_%H-%M-%S.csv')
        filename = '%s_%s' % (self.context.getId(), filename)
        self.request.response.setHeader('Content-Type', 'text/csv')
        self.request.response.setHeader('Content-Disposition',
                                        'attachment; filename=%s' % filename)
        return sio.getvalue().decode('utf8')
