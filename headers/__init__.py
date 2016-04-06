from .c_family import HEADER as C_FAMILY_HEADER
from .makefile import HEADER as MAKEFILE_HEADER
from .php import HEADER as PHP_HEADER
from .html import HEADER as HTML_HEADER
from .lua import HEADER as LUA_HEADER
from .ocaml import HEADER as OCAML_HEADER
from .haskell import HEADER as HASKELL_HEADER
from .asm import HEADER as ASM_HEADER

from os.path import split

C_STYLE_COMMENT_EXTENSIONS = (
    'c', 'h', 'cpp', 'hpp', 'tpp',
    'js', 'css', 'cs', 'scala', 'rs', 'go', 'swift'
)

# This is where we associate headers to file extensions
HEADER_SPEC = (
    (C_STYLE_COMMENT_EXTENSIONS,                C_FAMILY_HEADER),
    (('Makefile', ),                            MAKEFILE_HEADER),
    (('php', ),                                 PHP_HEADER),
    (('html', ),                                HTML_HEADER),
    (('lua', ),                                 LUA_HEADER),
    (('ml', 'mli'),                             OCAML_HEADER),
    (('hs', ),                                  HASKELL_HEADER),
    (('s', 's64', 'asm', 'hs', 'h64', 'inc'),   ASM_HEADER),
)

# Flattening the spec extensions and indexing them
TEMPLATES_BY_EXTENSION = dict()
for extensions, header in HEADER_SPEC:
    for ext in extensions:
        TEMPLATES_BY_EXTENSION[ext] = header

class NoHeaderError(Exception):
    pass

def get_template(file_path):
    _, file_name = split(file_path)
    dot_index = file_name.find('.')
    extension = file_name[dot_index + 1:]

    try:
        return TEMPLATES_BY_EXTENSION[extension]
    except KeyError:
        raise NoHeaderError
