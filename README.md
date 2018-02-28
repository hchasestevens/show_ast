# showast
[![PyPI version](https://badge.fury.io/py/showast.svg)](https://badge.fury.io/py/showast)
![Liberapay receiving](https://img.shields.io/liberapay/receives/hchasestevens.svg)

An IPython/Jupyter notebook plugin for visualizing abstract syntax trees.

Example usage
--------------
Examples can be found in [this IPython notebook](https://github.com/hchasestevens/show_ast/blob/master/Example.ipynb).

```python
import showast
```

```python
%%showast
print 1 + 2
```
![print 1 + 2 AST](http://i.imgur.com/vK3XTkX.png)

```python
from showast import show_source
import antigravity
show_source(antigravity)
```
![antigravity module AST](http://i.imgur.com/NJY6xhw.png)

Installation
-------------
```
pip install showast
```

showast has the following Python dependencies:
```
ipython
graphviz
```

You will also need to have [Graphviz](http://www.graphviz.org/Download..php) installed.

Use of the alternative nltk-based rendering engine requires the following packages:
```
nltk
pillow
```
When using this option, you will additionally need to have [Ghostscript](http://ghostscript.com/download/gsdnld.html) installed.

Contacts
--------

* Name: [H. Chase Stevens](http://www.chasestevens.com)
* Twitter: [@hchasestevens](https://twitter.com/hchasestevens)
