#!/usr/bin/env python3


import os
import sys
import textwrap
import shutil
import subprocess
import tempfile

TEMPLATE_FILE = os.path.dirname(__file__) + '/template.tex'

CROPMARKSTRUE = '\\usepackage[cam, width=4in, height=5.5in, center]{crop}'
CROPMARKSFALSE = ''
PGNUMSTRUE = '\\cfoot{\\footnotesize--\\,\\thepage\\,--}'
PGNUMSFALSE = '\\cfoot{}'
SECTION = '\n\\part{%(liquorName)s}\n'
DRINK = textwrap.dedent('''\
    \\begin{drink}{%(drinkName)s}
        \\begin{ingredients}
    %(ingredientsItems)s
        \\end{ingredients}
        \\begin{instructions}
            %(instructionsStr)s
        \\end{instructions}
    \\end{drink}

    ''')


class Document:
    '''
    Simple class to hold a document template, the document body and
    methods to insert the latter into the former.
    '''

    def __init__(self, recipes: dict, pageNums: bool, cropMarks: bool):
        '''
        Creates the Template object.

        Reads the file FILE which should have the string '%(contents)s' in it
        one or more times. Inserts `contents` parameter in all occurrences of
        this string.
        '''

        contents = ''
        for liquor in sorted(recipes.keys()):
            contents += SECTION % {'liquorName': liquor}
            for recipeKey in sorted(recipes[liquor].keys()):
                recipe = recipes[liquor][recipeKey]
                contents += str(recipe)

        # Load the template...
        with open(TEMPLATE_FILE, 'r') as stream:
            self._template = stream.read()

        # ...and populate it.
        self._content = contents
        self._cropMarks = CROPMARKSTRUE if cropMarks else CROPMARKSFALSE
        self._pageNums = PGNUMSTRUE if pageNums else PGNUMSFALSE
        self._document = self._template % {
            'contents': self._content,
            'cfoot': self._pageNums,
            'cropmarks': self._cropMarks
        }

    def __str__(self) -> str:
        '''
        Returns entire document as string.

        Strings are immutable in Python so access to the internal string is OK.
        '''

        return self._document

    @property
    def document(self) -> str:
        '''
        See Template.__str__.
        '''

        return str(self)

    def typeset(self) -> None:

        with tempfile.TemporaryDirectory() as tmpdir:
            texpath = os.path.dirname(__file__) + '/cocktails.tex'
            pdfpath = tmpdir + '/cocktails.pdf'

            with open(texpath, 'w') as texfile:
                texfile.write(self._document)

            try:
                shutil.copyfile(
                    os.path.dirname(__file__) + '/CMakeLists.txt',
                    tmpdir + '/CMakeLists.txt'
                )
                shutil.copyfile(
                    os.path.dirname(__file__) + '/modules/UseLATEX/UseLATEX.cmake',
                    tmpdir + '/UseLATEX.cmake'
                )
                generateBuildFiles = subprocess.Popen(
                    [
                        'cmake',
                        os.path.dirname(__file__),
                        '-GUnix Makefiles'
                    ],
                    cwd=tmpdir
                )
                generateBuildFiles.wait()
                build = subprocess.Popen(
                    ['make'],
                    cwd=tmpdir
                )
                build.wait()
            except Exception as e:
                print(
                    'Looks like LuaLaTeX had a few too many cocktails! '
                    'It died with the following error:\n'
                )
                print(str(e) + '\n')
                sys.exit(1)

            try:
                os.rename(pdfpath, os.getcwd() + '/cocktails.pdf')
            except Exception as e:
                print(
                    'Looks like Python and the OS had a few too many '
                    'cocktails! Renaming the cocktail manual failed with the '
                    'following error:\n'
                )
                print(str(e) + '\n')
                sys.exit(1)


class Recipe:
    def __init__(self, name: str, ingredients: list, instructions: str):
        self._name = name
        self._ingredients = ingredients
        self._instructions = instructions

    def __str__(self) -> str:
        return DRINK % {
            'drinkName': self._name,
            'ingredientsItems': '\n'.join(
                ['        \\item ' + ingredient
                    for ingredient in self._ingredients]),
            'instructionsStr': self._instructions
        }

    @property
    def name(self) -> str:
        return self._name

    @property
    def recipe(self) -> str:
        return str(self)
