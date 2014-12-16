import json
import datetime
import logging
from odict import odict
from Acquisition import aq_parent
from Products.Five import BrowserView
from plone.memoize.view import memoize
from repoze.catalog.query import (
    Contains,
    Or,
    Eq,
)
from zope.component import ComponentLookupError
from souper.soup import LazyRecord
from ..config import AUTOFIELDS
from ..storage import PfgCatalogFactory

try:
    # Plone < 4.3
    from zope.app.component.hooks import getSite
except ImportError:
    # Plone >= 4.3
    from zope.component.hooks import getSite

logger = logging.getLogger('collective.pfg.soup.subscribers')


class TableView(BrowserView):
    """datatables view
    """

    enabled_field = 'pfgsoup_show'
    enabled_auto_prefix = 'show'

    @memoize
    def columns(self):
        pfg = aq_parent(self.context)
        soup = self.context.get_soup()
        try:
            catalog = soup.catalog
        except ComponentLookupError:
            # ugly workaround - for some reason after copy the factory is gone
            logger.warn("Soup catalog wasnt created correctly after copy of "
                        "soup adapter. Auto-healing this now.")
            sm = getSite().getSiteManager()
            sm.registerUtility(factory=PfgCatalogFactory, name=soup.soup_name)
            catalog = soup.catalog
        result = odict()
        for field in pfg._getFieldObjects():
            if not field.Schema()[self.enabled_field].get(field):
                continue
            if field.isLabel():
                continue
            name = field.fgField.getName()
            col_info = {}
            col_info['label'] = field.fgField.widget.label
            col_info['sortable'] = False
            col_info['searchable'] = False
            col_info['sortindex'] = None
            if ('_sort_%s' % name) in catalog:
                col_info['sortable'] = hasattr(catalog['_sort_%s' % name],
                                               'sort')
                col_info['sortindex'] = '_sort_%s' % name
            if name in catalog:
                index = catalog[name]
                if not col_info['sortable']:
                    col_info['sortable'] = hasattr(index, 'sort')
                    if col_info['sortable']:
                        col_info['sortindex'] = name
                opattrs = ['applyContains', 'applyAny', 'applyEq']
                opavail = [_ for _ in opattrs if hasattr(index, _)]
                col_info['searchable'] = bool(opavail)
            result[name] = col_info
        for autofield in AUTOFIELDS:
            atfieldid = '%s_%s' % (self.enabled_auto_prefix, autofield)
            if self.context.Schema()[atfieldid].get(self.context):
                name = '_auto_%s' % autofield
                col_info = {}
                col_info['label'] = autofield.replace('_', ' ').title()
                col_info['sortable'] = True
                col_info['sortindex'] = name
                col_info['searchable'] = autofield == 'userid'
                result[name] = col_info
        return result


class TableDataView(TableView):
    """datatables json data
    """

    def _extract_sort(self):
        sortparams = dict()
        columns = self.columns()
        # sortingcols, sortable, searchable are not used for now, but to be
        # complete it gets extracted
        sortparams['sortingcols'] = self.request.form.get('iSortingCols')
        try:
            sortparams['sortingcols'] = int(sortparams['sortingcols'])
        except:
            sortparams['sortingcols'] = None
        sortparams['sortable'] = dict()
        sortparams['searchable'] = dict()
        sortparams['reverse'] = False
        sortparams['index'] = None
        for idx in range(0, len(columns)):
            colname = columns.keys()[idx]
            soabl = self.request.form.get('bSortable_%d' % idx,
                                         'false')
            sortparams['sortable'][colname] = soabl == 'true'
            seabl = self.request.form.get('bSearchable_%d' % idx,
                                         'false')
            sortparams['searchable'][colname] = seabl == 'true'
            col = int(self.request.form.get('iSortCol_%d' % idx, -1))
            if col > -1:
                sortparams['index'] = columns.keys()[col]
            sdir = self.request.form.get('sSortDir_%d' % idx, None)
            if sdir is not None:
                sortparams['reverse'] = sdir == 'desc'
        self.request.response.setHeader("Content-type", "application/json")
        return sortparams


    def _alldata(self, soup):
        columns = self.columns()
        iids = soup.storage.data.keys()
        sort = self._extract_sort()
        if sort['index'] and columns[sort['index']]['sortable']:
            sortindex = soup.catalog[columns[sort['index']]['sortindex']]
            try:
                iids = sortindex.sort(soup.storage.data.keys(),
                                      reverse=sort['reverse'])
            except TypeError:
                # sucking textindex raise this
                iids = soup.storage.data.keys()

        def lazyrecords():
            for iid in iids:
                yield LazyRecord(iid, soup)
        return soup.storage.length.value, lazyrecords()

    @memoize
    def _select_index_op(self, index, value):
        # this is crap, but no idea how to make it more efficient
        try:
            index.applyContains(value)
        except NotImplementedError, e:
            try:
                index.applyEq(value)
            except NotImplementedError, e:
                return None
            else:
                return Eq
        except Exception, e:
            return None
        else:
            return Contains

    def _query(self, soup):
        all_columns = self.columns()
        columns = odict()
        for name in all_columns:
            if all_columns[name]['searchable']:
                columns[name] = all_columns[name]
        querymap = dict()
        for idx in range(0, len(columns.keys())):
            name = columns.keys()[idx]
            term = self.request.form['sSearch_%d' % idx]
            if not term or not term.strip() \
               or not soup.catalog.get(name, False):
                continue
            querymap[name] = term
        global_term = self.request.form['sSearch']
        if not querymap and not global_term:
            return self._alldata(soup)
        query = None
        if querymap:
            for index_name in querymap:
                query_element = None
                searchvalue = querymap[index_name]
                op = self._select_index_op(soup.catalog[index_name],
                                           searchvalue)
                if op is None:
                    continue
                if op is Contains and not searchvalue.endswith('*'):
                    searchvalue += '*'
                query_element = op(index_name, searchvalue)
                if query is not None:
                    query &= query_element
                else:
                    query = query_element
        global_query = None
        if global_term:
            for index_name in columns:
                if index_name.startswith('_sort_'):
                    continue
                query_element = None
                op = self._select_index_op(soup.catalog[index_name],
                                           global_term)
                if op is None:
                    continue
                searchvalue = global_term
                if op is Contains and not searchvalue.endswith('*'):
                    searchvalue += '*'
                query_element = op(index_name, searchvalue)
                if global_query is not None:
                    global_query = Or(global_query, query_element)
                else:
                    global_query = query_element
        if query is not None and global_query is not None:
            query = Or(query, global_query)
        elif query is None and global_query is not None:
            query = global_query
        sort = self._extract_sort()
        if sort['index'] and all_columns[sort['index']]['sortable']:
            sortindex = all_columns[sort['index']]['sortindex']
        else:
            sortindex = None
        try:
            result = soup.lazy(query, sort_index=sortindex,
                               reverse=sort['reverse'],
                               with_size=True)
            length = result.next()
            return length, result
        except Exception, e:
            # ParseError raised by zope.index.text.*. this sucks
            return self._alldata(soup)

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
        columns = self.columns()
        aaData = list()
        length, lazydata = self._query(soup)
        # XXX Todo html from template
        url = self.context.absolute_url()
        html = '<a href="#" data-iid="%(iid)s" class="pfgsoup-edit">edit</a> '
        html += '<a href="%(url)s/pfgsoupdel?iid=%(iid)s" class="pfgsoup-delete">remove</a> '
        html += ('<a href="%(url)s/@@pfgsouplog?iid=%(iid)s" '
                 'class="pfgsoup-log">log</a>')


        def record2list(record):
            result = list()
            for colname in columns:
                value = record.attrs.get(colname, '')
                if isinstance(value, list):
                    value = ', '.join(value)
                elif isinstance(value, datetime.datetime):
                    value = value.isoformat()
                elif isinstance(value, dict):
                    value = ', '.join([str(_) for _ in value.items])
                try:
                    json.dumps(value)
                except TypeError:
                    value = str(value)
                result.append(value)
            result.append(html % {'iid': record.intid, 'url': url})
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
