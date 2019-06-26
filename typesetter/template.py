#!/usr/bin/env python3


FILE = 'template.tex'


class Template:
    '''
    Simple class to hold a document template, the document body and
    methods to insert the latter into the former.
    '''

    def __init__(self, contents: str):
        '''
        Creates the Template object.

        Reads the file FILE which should have the string '%(contents)s' in it
        one or more times. Inserts `contents` parameter in all occurrences of this
        fstring.
        '''

        with open(FILE, 'r') as stream:
            self._template = stream.read()

        self._content = contents
        self._document = self._template % {'contents': self._contents}

    def __str__(self):
        return self._template % {'contents' % self._contents}

    @property
    def document(self):
        return str(self)
