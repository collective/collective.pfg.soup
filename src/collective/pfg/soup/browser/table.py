import json
from Acquisition import aq_parent
from Products.Five import BrowserView
from repoze.catalog.query import (
    Contains,
    Or,
)
from souper.soup import LazyRecord


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

    def _alldata(self, soup):
        data = soup.storage.data
        def lazyrecords():
            for record_id in data:
                yield LazyRecord(record_id, soup)
        return soup.storage.length.value, lazyrecords()

    def _query(self, soup):
        from pprint import pprint
        pprint(self.request.form)
        rows = self.rows()
        querymap = dict()
        for idx in range(0, len(rows)):
            term = self.request.form['sSearch_%d' % idx]
            if not term or not term.strip():
                continue
            querymap[rows[idx][1]] = term
        global_term = self.request.form['sSearch']
        if not querymap and not global_term:
            return self._alldata(soup)
        query = None
        if querymap:
            for index_name in querymap:
                query_element = Contains(index_name, querymap[index_name])
                if query is not None:
                    query &= query_element
                else:
                    query = query_element

        global_query = None
        if global_term:
            for index_name in soup.catalog:
                query_element = Contains(index_name, global_term)
                if global_query is not None:
                    global_query = Or(global_query, query_element)
                else:
                    global_query = query_element
        if query is not None and global_query is not None:
            query = Or(query, global_query)
        elif query is None and global_query is not None:
            query = global_query
        query.print_tree()
        result = soup.lazy(query, with_size=True)
        length = result.next()
        return length, result

    def _slice(self, fullresult):
        start = int(self.request.form['iDisplayStart'])
        length = int(self.request.form['iDisplayLength'])
        count = 0
        for lr in fullresult:
            if count >= start and count < (start + length):
                yield lr
            if count >= (start + length):
                break
            count += 1

    def __call__(self):
        soup = self.context.get_soup()
        aaData = list()
        length, lazydata = self._query(soup)
        rownames = [_[1] for _ in self.rows()]

        def record2list(record):
            result = list()
            for rowname in rownames:
                result.append(record.attrs.get(rowname, ''))
            return result
        for lazyrecord in self._slice(lazydata):
            aaData.append(record2list(lazyrecord()))
        data = {
          "sEcho": int(self.request.form['sEcho']),
          "iTotalRecords": soup.storage.length.value,
          "iTotalDisplayRecords": length,
          "aaData": aaData,
        }
        return json.dumps(data)
