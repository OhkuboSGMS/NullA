from setuptools import setup
from Cython.Build import cythonize
setup(
    name="nulla",
    ext_modules=cythonize("nulla/**/*.pyx",annotate=True)
)