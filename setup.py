from numpy.lib.utils import get_include
from setuptools import Extension, setup
from Cython.Build import cythonize

moduloExt = [Extension(
    "RutinasBoltzmann",
    ["RutinasBoltzmann.pyx"],
    extra_compile_args=["-ffast-math","-O3","-march=native","-fopenmp"],
    extra_link_args=["-fopenmp"]
)]

setup(
    name="RutinasBoltzmann",
    ext_modules=cythonize(moduloExt, annotate=True),
    include_dirs=[get_include()],
    zip_safe=False
)
