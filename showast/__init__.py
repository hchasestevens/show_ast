import os
import re
import ast
import imp
import inspect

from IPython.core.magic import register_cell_magic
from IPython.display import display
    
    
__all__ = ['show_ast', 'show_source', 'show_text', 'Settings', 'Renderers',]


RENDERING_PATH = os.path.join(os.path.dirname(__file__), 'rendering')


class Renderers:
    graphviz = 'graphviz', [RENDERING_PATH]
    nltk = 'nltk', [RENDERING_PATH]
    

Settings = dict(
    # Styling options:
    scale=2,
    font='courier',
    shape='none',
    terminal_color='#008040',
    nonterminal_color='#004080',

    # AST display options:
    omit_module=True,
    omit_docstrings=True,
    omit_location_info=True,
    locations_format="L{begin[0]}:{begin[1]}-L{end[0]}:{end[1]}",
    omit_source=True,

    # Rendering engine is expected to expose "render" function
    renderer=Renderers.graphviz,
)
        
        
def show_ast(module, settings=Settings):
    omit_docstrings = settings['omit_docstrings']
    if settings['omit_module'] and len(module.body) == 1:
        node = module.body[0]
    else:
        node = module
    renderer = imp.load_module(
        'renderer', 
        *imp.find_module(*settings['renderer'])
    )
    display(renderer.render(node, settings))


@register_cell_magic
def showast(__, cell):
    m = ast.parse(cell)
    show_ast(m)


def show_source(item, settings=Settings):
    src = inspect.getsource(item)
    show_text(src, settings)


def show_text(src, settings=Settings):
    try:
        module = ast.parse(src)
    except IndentationError:
        initial_whitespace = re.match(r'^\s+', src)
        if initial_whitespace is not None:
            amt_whitespace = len(initial_whitespace.group())
            src = '\n'.join(
                line[amt_whitespace:]
                for line in
                src.splitlines()
            )
        module = ast.parse(src)
    show_ast(module, settings)
