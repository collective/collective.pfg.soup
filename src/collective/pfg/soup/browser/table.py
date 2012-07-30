import json
from Acquisition import aq_parent
from Products.Five import BrowserView


class TableView(BrowserView):
    """datatables view
    """

    def rows(self):
        pfg = aq_parent(self.context)
        result = []
        for field in pfg._getFieldObjects():
            if field.isLabel():
                continue
            result.append((field.fgField.widget.label,
                           field.fgField.getName(),
                           ))
        return result


class TableDataView(TableView):
    """datatables json data
    """

    def __call__(self):
        from pprint import pprint
        pprint(self.request.form)
        soup = self.context.get_soup()
        rownames = [_[1] for _ in self.rows()]
        def record2list(record):
            result = list()
            for rowname in rownames:
                result.append(record.attrs.get(rowname, ''))
            return result
        aaData = list()
        count = 0
        data = soup.storage.data
        for record_id in data:
            count += 1
            aaData.append(record2list(data[record_id]))
        data = {
          "sEcho": int(self.request.form['sEcho']),
          "iTotalRecords": soup.storage.length.value,
          "iTotalDisplayRecords": soup.storage.length.value,
          "aaData": aaData,
        }
        pprint(data)
        return json.dumps(data)
