from AccessControl import ClassSecurityInfo
from zope.contenttype import guess_content_type
from ZPublisher.HTTPRequest import FileUpload
from Products.Archetypes.public import (
    Schema,
)
from Products.ATContentTypes.content.base import registerATCT
from Products.PloneFormGen.content.actionAdapter import (
    FormActionAdapter,
    FormAdapterSchema,
)
from collective.pfg.soup import _
from collective.pfg.soup.config import PROJECTNAME

import logging
logger = logging.getLogger("PloneFormGen")


class SoupAdapter(FormActionAdapter):
    """A form action adapter that will save form input data in a soup.
    """

    schema = FormAdapterSchema.copy() + Schema((
    ))

    meta_type = 'SoupAdapter'

    security = ClassSecurityInfo()

    def onSuccess(self, fields, REQUEST=None, loopstop=False):
        """
        saves data.
        """
        # XXX below store to soup
        data = []
        for f in fields:
            if f.isFileField():
                file = REQUEST.form.get('%s_file' % f.fgField.getName())
                if isinstance(file, FileUpload) and file.filename != '':
                    file.seek(0)
                    fdata = file.read()
                    filename = file.filename
                    mimetype, enc = guess_content_type(filename, fdata, None)
                    if mimetype.find('text/') >= 0:
                        # convert to native eols
                        fdata = fdata.replace('\x0d\x0a', '\n').replace('\x0a', '\n').replace('\x0d', '\n')
                        data.append('%s:%s:%s:%s' % (filename, mimetype, enc, fdata))
                    else:
                        data.append('%s:%s:%s:Binary upload discarded' % (filename, mimetype, enc))
                else:
                    data.append('NO UPLOAD')
            elif not f.isLabel():
                val = REQUEST.form.get(f.fgField.getName(), '')
                if not isinstance(val, basestring):
                    # Zope has marshalled the field into
                    # something other than a string
                    val = str(val)
                data.append(val)

        self._addDataRow(data)


registerATCT(SoupAdapter, PROJECTNAME)
