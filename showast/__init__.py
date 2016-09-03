import ast
import os
import inspect
import re
from math import sqrt, ceil
from base64 import b64encode

from nltk.tree import Tree
from nltk.draw.tree import TreeView, TreeWidget
from nltk.draw.util import CanvasFrame
from PIL import Image, ImageChops, ImageEnhance

from IPython.core.magic import register_cell_magic
from IPython.display import Image as IPImage, display

try:
    from Tkinter import Tk, IntVar
except ImportError:
    from tkinter import Tk, IntVar

    
__all__ = ['show_ast', 'show_source', 'Settings']
    

Settings = dict(
    scale=2,
    font='courier',
    terminal_color='#008040',
    nonterminal_color='#004080',
    omit_module=True,
)


def nltk_treestring(node):
    fields = []
    node_fields = zip(
        node._fields, 
        (getattr(node, attr) for attr in node._fields)
    )
    for k, v in node_fields:
        if isinstance(v, ast.AST):
            fields.append(nltk_treestring(v))
        
        elif isinstance(v, list):
            fields.extend(
                nltk_treestring(item)
                if isinstance(item, ast.AST)
                else str(item)
                for item in v
            )
            
        elif isinstance(v, basestring):
            fields.append('"{}"'.format(v))
                
        elif v is not None:
            fields.append(str(v))
            
    if not fields:
        return node.__class__.__name__
            
    return '({} {} )'.format(
        node.__class__.__name__, 
        ' '.join(fields)
    )


class SizableTreeView(TreeView):
    def __init__(self, *trees):
        self._trees = trees

        self._top = Tk()

        cf = self._cframe = CanvasFrame(self._top)

        # Size is variable.
        self._size = IntVar(self._top)
        self._size.set(12)
        bold = (Settings['font'], -int(12 * Settings['scale']), 'bold')
        norm = (Settings['font'], -int(12 * Settings['scale']))

        # Lay the trees out in a square.
        self._width = int(ceil(sqrt(len(trees))))
        self._widgets = []
        for tree in trees:
            widget = TreeWidget(
                cf.canvas(), 
                tree, 
                node_font=bold,
                leaf_color=Settings['terminal_color'], 
                node_color=Settings['nonterminal_color'],
                roof_color='#004040', 
                roof_fill='white',
                line_color='#004040', 
                leaf_font=norm,
            )
            widget['xspace'] = int(Settings['scale'] * widget['xspace'])
            widget['yspace'] = int(Settings['scale'] * widget['yspace'])
            self._widgets.append(widget)
            cf.add_widget(widget, 0, 0)

        self._layout()
        self._cframe.pack(expand=1, fill='both', side='left')

        
def tree_image(tree):
    t = Tree.fromstring(tree)
    tv = SizableTreeView(t)
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
    display(IPImage(filename='.temp.png'))
    for fname in ('.temp.ps', '.temp.png'):
        try:
            os.remove(fname)
        except (IOError, WindowsError):
            pass
        
        
def show_ast(module):
    if Settings['omit_module'] and len(module.body) == 1:
        treestring = nltk_treestring(module.body[0])
    else:
        treestring = nltk_treestring(module)
    tree_image(treestring)
        

@register_cell_magic
def showast(__, cell):
    m = ast.parse(cell)
    show_ast(m)


def show_source(item):
    src = inspect.getsource(item)
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
    show_ast(ast.parse(src))
