# showast
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
![print 1 + 2 AST](http://i.imgur.com/DCXbiOK.png)

Installation
-------------
```
easy_install showast
```

showast has the following dependencies:
```
ipython
nltk
pillow
```

Additionally, you will need to have [Ghostscript](http://ghostscript.com/download/gsdnld.html) installed.

Contacts
--------

* Name: [H. Chase Stevens](http://www.chasestevens.com)
* Twitter: [@hchasestevens](https://twitter.com/hchasestevens)
