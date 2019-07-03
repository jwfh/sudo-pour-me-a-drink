#!/usr/bin/env python3


import os
import sys
import textwrap
import yaml
from . import template


def run(args: list) -> None:
    '''
    This, being the only public function in the module, does everything.
    '''

    # A little help message for those who don't RTFM :p
    HELP = textwrap.dedent('''\
    Usage: %(binary)s ARGUMENTS

        [-no]-page-numbers
                Enable/disable page numbering.

        [-no]-crop-marks
                Enable/disable visible crop marks.

        -nup XDIMxYDIM
                Enables n-up printing with XDIMxYDIM pages per sheet. Acceptable
                values for XDIMxYDIM are '1x2', '2x2', '2x3', etc.

        -h, --help
                Prints this help message.
    ''' % {'binary': sys.argv[0]})

    # Let's try to parse the args... Yay for user input 😬
    nup = None
    cropMarks = True
    pageNums = True
    try:
        assert len(sys.argv) > 1, textwrap.dedent('''\
            Either I look psychic or I\'ve had one too many tonight! Why don\'t you be a
            little more specific in telling me what you want.

            ''') + HELP

        argset = set(sys.argv)
        if argset.intersection({'-h', '--help'}):
            print(HELP)
            sys.exit(0)

        assert not {'-crop-marks', '-no-crop-marks'}.issubset(argset), \
            'I\'m confused... Use either `-crop-marks\' or `-no-crop-marks\', not both.'

        assert not {'-page-numbers', '-no-page-numbers'}.issubset(argset), \
            'I\'m confused... Use either `-page-numbers\' or `-no-page-numbers\', not both.'

        if '-nup' in sys.argv:
            assert sys.argv.index('-nup') < len(sys.argv) - 1, \
                'Hmm... `-nup\' requires one argument but none were given.'
            nup = sys.argv[sys.argv.index('-nup') + 1].split('x')
            assert len(nup) == 2, '-nup takese two arguments, delimited by an `x\'. E.g., -nup 2x2'
        else:
            nup = None

        if '-no-crop-marks' in argset:
            cropMarks = False
        else:
            # Default
            cropMarks = True

        if '-no-page-numbers' in argset:
            pageNums = False
        else:
            # Default
            pageNums = True

    except AssertionError as e:
        sys.stderr.write(str(e))
        sys.exit(1)

    recipes = dict()
    recipesDir = os.path.dirname(os.path.dirname(__file__)) + '/recipes/'
    for d in os.listdir(recipesDir):
        liquorDir = recipesDir + d
        if os.path.isdir(liquorDir):
            liquor = os.path.basename(liquorDir)
            recipes[liquor] = dict()
            for f in os.listdir(liquorDir):
                if f.endswith('.yaml') or f.endswith('.yml'):
                    with open(liquorDir + '/' + f, 'r') as stream:
                        recipe = yaml.safe_load(stream)

                        if recipe.get('name') is None:
                            raise ValueError('Expected YAML file with `name\' defined.')
                        if recipe.get('ingredients') is None:
                            raise ValueError('Expected YAML file with `ingredients\' defined.')
                        if recipe.get('instructions') is None:
                            raise ValueError('Expected YAML file with `instructions\' defined.')

                        recipes[liquor][recipe['name']] = template.Recipe(
                            recipe['name'],
                            recipe['ingredients'],
                            recipe['instructions']
                        )

    document = template.Document(recipes, pageNums, cropMarks)
    document.typeset()
