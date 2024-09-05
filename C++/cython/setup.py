

from setuptools import setup, Extension

from Cython.Build import cythonize



ext_modules = [
    Extension(
        "cpy_srcipc",
        sources=["cpy_srcipc.pyx"],
        libraries=["czmq", "libzmq-v143-mt-4_3_6", "EntRecBridge"],
        library_dirs=["../libs/x64/", "./"],
        include_dirs=["../src", "../includes"],
    )
]


setup(
    
    name = 'cpy_entrec_bridge',
    ext_modules = cythonize(ext_modules, build_dir="../builds/" ),
)