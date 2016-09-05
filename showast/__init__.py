import ast
import os
import inspect
import re
import itertools
import functools
from math import sqrt, ceil

from nltk.tree import Tree
from nltk.draw.tree import TreeView, TreeWidget
from nltk.draw.util import CanvasFrame
from PIL import Image, ImageChops, ImageEnhance

import graphviz

from IPython.core.magic import register_cell_magic
from IPython.display import Image as IPImage, display

try:
    from Tkinter import Tk, IntVar
except ImportError:
    from tkinter import Tk, IntVar
    
try:
    _basestring = basestring
except NameError:
    _basestring = str

    
__all__ = ['show_ast', 'show_source', 'Settings']
    

Settings = dict(
    scale=2,
    font='courier',
    terminal_color='#008040',
    nonterminal_color='#004080',
    omit_module=True,
    omit_docstrings=True,
)


def strip_docstring(body):
    first = body[0]
    if isinstance(first, ast.Expr) and isinstance(first.value, ast.Str):
        return body[1:]
    return body


def nltk_treestring(node, omit_docstrings=True):
    fields = []
    node_fields = zip(
        node._fields, 
        (getattr(node, attr) for attr in node._fields)
    )
    func_or_class = isinstance(node, (ast.FunctionDef, ast.ClassDef))
    for k, v in node_fields:
        if isinstance(v, ast.AST):
            fields.append(nltk_treestring(v))
        
        elif isinstance(v, list):
            if func_or_class and omit_docstrings and k == 'body':
                v = strip_docstring(v)
            fields.extend(
                nltk_treestring(item)
                if isinstance(item, ast.AST)
                else str(item)
                for item in v
            )
            
        elif isinstance(v, _basestring):
            fields.append('"{}"'.format(v))
                
        elif v is not None:
            fields.append(str(v))
            
    if not fields:
        return node.__class__.__name__
            
    return '({} {} )'.format(
        node.__class__.__name__, 
        ' '.join(fields)
    )


def attach_to_parent(parent, graph, names, label, name=None):
    node_name = next(names) if name is None else name
    node = graph.node(node_name, label=label)
    graph.edge(parent, node_name)
    

def graphviz_add_children(ast_node, parent_node, graph, names, omit_docstrings=True):
    node_fields = zip(
        ast_node._fields, 
        (getattr(ast_node, attr) for attr in ast_node._fields)
    )
    _attach_to_parent = functools.partial(
        attach_to_parent, 
        parent=parent_node, 
        graph=graph, 
        names=names,
    )
    func_or_class = isinstance(ast_node, (ast.FunctionDef, ast.ClassDef))
    for k, v in node_fields:
        if isinstance(v, ast.AST):
            node_name = next(names)
            _attach_to_parent(label=v.__class__.__name__, name=node_name)
            graphviz_add_children(v, node_name, graph, names, omit_docstrings)
        
        elif isinstance(v, list):
            if func_or_class and omit_docstrings and k == 'body':
                v = strip_docstring(v)
            for item in v:
                if isinstance(item, ast.AST):
                    pass
                else:
                    pass
            #fields.extend(
            #    nltk_treestring(item)
            #    if isinstance(item, ast.AST)
            #    else str(item)
            #    for item in v
            #)
            
        elif isinstance(v, _basestring):
            _attach_to_parent(label='"{}"'.format(v))
                
        elif v is not None:
            _attach_to_parent(label=str(v))
            
    if not node_fields:
        return
        _attach_to_parent(label=ast_node.__class__.__name__)


def graphviz_graph(node, omit_docstrings=True):
    graph = graphviz.Graph(format='svg')
    names = (str(x) for x in itertools.count())
    root_name = next(names)
    root = graph.node(root_name, label=node.__class__.__name__)
    graphviz_add_children(node, root_name, graph, names, omit_docstrings)
    return graph


class SizableTreeView(TreeView):
    def __init__(self, tree, settings=Settings):
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

        
def tree_image(tree, settings=Settings):
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
    display(IPImage(filename='.temp.png'))
    for fname in ('.temp.ps', '.temp.png'):
        try:
            os.remove(fname)
        except (IOError, WindowsError):
            pass
        
        
def show_ast(module, settings=Settings):
    omit_docstrings = settings['omit_docstrings']
    if settings['omit_module'] and len(module.body) == 1:
        treestring = nltk_treestring(module.body[0], omit_docstrings)
    else:
        treestring = nltk_treestring(module, omit_docstrings)
    tree_image(treestring, settings)
        

@register_cell_magic
def showast(__, cell):
    m = ast.parse(cell)
    show_ast(m)


def show_source(item, settings=Settings):
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
    show_ast(ast.parse(src), settings)
