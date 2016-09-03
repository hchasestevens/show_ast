import ast
import os
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


SCALE = 1.9


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
        bold = ('courier', -int(12 * SCALE), 'bold')
        helv = ('courier', -int(12 * SCALE))

        # Lay the trees out in a square.
        self._width = int(ceil(sqrt(len(trees))))
        self._widgets = []
        for tree in trees:
            widget = TreeWidget(
                cf.canvas(), 
                tree, 
                node_font=bold,
                leaf_color='#008040', 
                node_color='#004080',
                roof_color='#004040', 
                roof_fill='white',
                line_color='#004040', 
                leaf_font=helv,
            )
            widget['xspace'] = int(SCALE * widget['xspace'])
            widget['yspace'] = int(SCALE * widget['yspace'])
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
        

@register_cell_magic
def showast(__, cell):
    m = ast.parse(cell)
    treestring = nltk_treestring(m.body[0] if len(m.body) == 1 else m)
    tree_image(treestring)
    return
