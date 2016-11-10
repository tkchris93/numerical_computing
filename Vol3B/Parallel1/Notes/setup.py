from distutils.core import setup
from Cython.Build import cythonize

setup(name="adj_zeros", ext_modules=cythonize('cy_adj_zeros.pyx'))
