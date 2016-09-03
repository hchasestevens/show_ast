from setuptools import setup
 
setup(
    name='showast',
    packages=['showast'],
    version='0.1.1',
    description = 'IPython notebook plugin for visualizing abstract syntax trees.',
    license='MIT',
    author='H. Chase Stevens',
    author_email='chase@chasestevens.com',
    url='https://github.com/hchasestevens/show_ast',
    install_requires=[
        'nltk',
        'pillow',
        'ipython',
    ],
    keywords='ipython jupyter notebook ast asts',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Topic :: Software Development :: Code Generators',
    ]
)
