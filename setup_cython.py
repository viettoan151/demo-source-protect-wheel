# coding: utf-8
import os
import sys
import fnmatch
import subprocess
import sysconfig

from setuptools import setup, find_packages
from setuptools.command.build_py import build_py as _build_py
from setuptools.extension import Extension

from Cython.Build import cythonize
from Cython.Distutils import build_ext
from pathlib import Path
import shutil

# NOTICE: For compatible with python windows, all build package must use Microsoft build tool
# TODO: replace Microsoft Build Tool cmd with your system
if sys.platform == 'win32':
    # patch env with vcvarsall.bat from vs2015 (vc14)
    target_s = 'x86_amd64'
    cmd = '"C:\\Program Files (x86)\\Microsoft Visual Studio\\2019\\BuildTools\\VC\\Auxiliary\\Build\\vcvarsall.bat" ' \
          '{} >nul 2>&1 && set'.format(target_s)
    try:
        out = subprocess.check_output(cmd, stderr=subprocess.STDOUT, universal_newlines=True)
    except Exception as e:
        print("Error executing {}".format(cmd))
        raise e
    
    for key, _, value in (line.partition('=') for line in out.splitlines()):
        if key and value:
            os.environ[key] = value
    
    # inform setuptools that the env is already set
    os.environ['DISTUTILS_USE_SDK'] = '1'

# Exclude file, when you don't want to compile these files
# Must use OS independent path name
EXCLUDE_FILES = [
    # os.path.join('app','main.py'),
]

# The module folder, your application will be named as its also
NAME_APP = 'app'


# noinspection PyPep8Naming
class build_py(_build_py):
    def find_package_modules(self, package, package_dir):
        ext_suffix = sysconfig.get_config_var('EXT_SUFFIX')
        modules = super().find_package_modules(package, package_dir)
        filtered_modules = []
        for (pkg, mod, filepath) in modules:
            if os.path.exists(filepath.replace('.py', ext_suffix)):
                continue
            filtered_modules.append((pkg, mod, filepath,))
        return filtered_modules


def get_ext_paths(root_dir, exclude_files):
    """
    Get path of all .py files for compilation
    @param root_dir: Root directory for searching .py file
    @param exclude_files: exclude files list
    @return: list of .py files, except exclude_files
            example [Extension("app.*", ["app/*.py"]),]
    """
    paths = []
    for root, dirs, files in os.walk(root_dir):
        for filename in files:
            # ignore file without .py extension
            if os.path.splitext(filename)[1] != '.py':
                continue
            # join to root dir
            file_path = os.path.join(root, filename)
            # filter out exclude files
            if file_path in exclude_files:
                continue
            
            paths.append(file_path)
    
    return paths


def get_export_symbols_fixed(self, ext):
    """
    https://stackoverflow.com/a/58826688
    Function to find all module __init__.py for Windows compilation
    @param self:
    @param ext:
    @return:
    """
    names = ext.name.split('.')
    if names[-1] != "__init__":
        initfunc_name = "PyInit_" + names[-1]
    else:
        # take name of the package if it is an __init__-file
        initfunc_name = "PyInit_" + names[-2]
    if initfunc_name not in ext.export_symbols:
        ext.export_symbols.append(initfunc_name)
    return ext.export_symbols


class MyBuildExt(build_ext):
    def run(self):
        build_ext.get_export_symbols = get_export_symbols_fixed
        build_ext.run(self)
        build_dir = Path(self.build_lib)
        root_dir = Path(__file__).parent
        
        target_dir = build_dir if not self.inplace else root_dir
        
        # TODO: Manually copy all your module __init__.py here
        self.copy_file(Path(NAME_APP) / '__init__.py', root_dir, target_dir)
        # TODO: When you have submodule __init__.py, please do copy them also
        # self.copy_file(Path(NAME_APP) / 'submodule' / '__init__.py', root_dir, target_dir)
        # or
        # self.copy_file(Path('submodule') / '__init__.py', root_dir, target_dir)
        
    @classmethod
    def copy_file(cls, path, source_dir, destination_dir):
        """
        Copy a path from source_dir to destination_dir
        @param path: file in Path format
        @param source_dir: source directory in Path format
        @param destination_dir: destination directory in in Path format
        @return: None
        """
        if not (source_dir / path).exists():
            return
        shutil.copyfile(str(source_dir / path), str(destination_dir / path))


setup(
    name=NAME_APP,
    version='0.1.0',
    # packages=find_packages(),
    packages=[],
    ext_modules=cythonize(
        get_ext_paths(NAME_APP, EXCLUDE_FILES),
        build_dir="build",
        compiler_directives={'language_level': 3,
                             'always_allow_keywords': True,
                             }
    ),
    include_dir=[NAME_APP, os.path.join(NAME_APP, 'includes')],
    cmdclass={
        'build_py': build_py,
        'build_ext': MyBuildExt,
    },
)

# build command
# python3 setup_cython.py bdist_wheel
# python3 setup_cython.py install
# rm -rf app.egg-info dist build
# unzip dist/app-0.1.0-cp36-cp36m-linux_x86_64.whl -d dist/app

