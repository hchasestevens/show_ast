"""
Rendering module for nltk/PIL.
"""

import os
import contextlib
from functools import partial
try:
    from Tkinter import Tk, IntVar
except ImportError:
    from tkinter import Tk, IntVar

from nltk.tree import Tree
from nltk.draw.tree import TreeView, TreeWidget
from nltk.draw.util import CanvasFrame
from PIL import Image, ImageChops, ImageEnhance
from IPython.display import Image as IPImage

from showast.asts import recurse_through_ast
from showast.util.contextmanagers import suppress


def handle_ast(node, omit_docstrings):
    return recurse_through_ast(
        node, 
        partial(handle_ast, omit_docstrings=omit_docstrings), 
        handle_terminal, 
        handle_fields, 
        handle_no_fields,
        omit_docstrings,
    )


def handle_terminal(terminal):
    return str(terminal)


def handle_fields(node, fields):
    return '({.__class__.__name__} {} )'.format(node, ' '.join(fields))


def handle_no_fields(node):
    return node.__class__.__name__


class SizableTreeView(TreeView):
    def __init__(self, tree, settings):
        self._trees = (tree,)

        self._top = Tk()

        cf = self._cframe = CanvasFrame(self._top)

        # Size is variable.
        self._size = IntVar(self._top)
        self._size.set(12)
        bold = (settings['font'], -int(12 * settings['scale']), 'bold')
        norm = (settings['font'], -int(12 * settings['scale']))

        self._width = 1
        self._widgets = []
        widget = TreeWidget(
            cf.canvas(), 
            tree, 
            node_font=bold,
            leaf_color=settings['terminal_color'], 
            node_color=settings['nonterminal_color'],
            roof_color='#004040', 
            roof_fill='white',
            line_color='#004040', 
            leaf_font=norm,
        )
        widget['xspace'] = int(settings['scale'] * widget['xspace'])
        widget['yspace'] = int(settings['scale'] * widget['yspace'])
        self._widgets.append(widget)
        cf.add_widget(widget, 0, 0)

        self._layout()
        self._cframe.pack(expand=1, fill='both', side='left')

        
@contextlib.contextmanager
def _tree_image(tree, settings):
    t = Tree.fromstring(tree)
    tv = SizableTreeView(t, settings)
    tv._cframe.print_to_file('.temp.ps')
    im = Image.open('.temp.ps')
    
    # trim whitespace
    bg = Image.new(im.mode, im.size, im.getpixel((0, 0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        im = im.crop(bbox)
        
    im.save('.temp.png', 'PNG')
    try:
        yield '.temp.png'
    finally:
        for fname in ('.temp.ps', '.temp.png'):
            with suppress(IOError, OSError):
                os.remove(fname)


def render(node, settings):
    """
    Given an AST node and settings, return a displayable object.
    """
    tree = handle_ast(node, settings['omit_docstrings'])
    with _tree_image(tree, settings) as fname:
        return IPImage(filename=fname)
