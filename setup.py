from setuptools import setup
 
setup(
    name='showast',
    packages=['showast', 'showast.rendering', 'showast.util',],
    version='0.2.4',
    description = 'IPython notebook plugin for visualizing abstract syntax trees.',
    license='MIT',
    author='H. Chase Stevens',
    author_email='chase@chasestevens.com',
    url='https://github.com/hchasestevens/show_ast',
    install_requires=[
        'ipython',
        'graphviz',
    ],
    extras_require={
        'nltk': ['nltk', 'pillow'],
    },
    keywords='ipython jupyter notebook ast asts graphing visualization syntax',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Topic :: Software Development :: Code Generators',
        'Framework :: IPython',
        'Topic :: Multimedia :: Graphics :: Presentation',
    ]
)
