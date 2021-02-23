# coding: utf-8
import os
import fnmatch
import sysconfig

from setuptools import setup, find_packages
from setuptools.command.build_py import build_py as _build_py
from setuptools.extension import Extension

from Cython.Build import cythonize
from Cython.Distutils import build_ext
from pathlib import Path
import shutil

EXCLUDE_FILES = [
    # 'app/main.py'
]


# noinspection PyPep8Naming
class build_py(_build_py):

    def find_package_modules(self, package, package_dir):
        ext_suffix = sysconfig.get_config_var('EXT_SUFFIX')
        modules = super().find_package_modules(package, package_dir)
        filtered_modules = []
        for (pkg, mod, filepath) in modules:
            if os.path.exists(filepath.replace('.py', ext_suffix)):
                continue
            filtered_modules.append((pkg, mod, filepath, ))
        return filtered_modules


def get_ext_paths(root_dir, exclude_files):
    """get filepaths for compilation"""
    paths = []

    for root, dirs, files in os.walk(root_dir):
        for filename in files:
            if os.path.splitext(filename)[1] != '.py':
                continue

            file_path = os.path.join(root, filename)
            if file_path in exclude_files:
                continue

            paths.append(file_path)
    return paths


class MyBuildExt(build_ext):
    def run(self):
        build_ext.run(self)

        build_dir = Path(self.build_lib)
        root_dir = Path(__file__).parent

        target_dir = build_dir if not self.inplace else root_dir

        self.copy_file(Path('app') / '__init__.py', root_dir, target_dir)
        # self.copy_file(Path('mypkg2') / '__init__.py', root_dir, target_dir)
        
    def copy_file(self, path, source_dir, destination_dir):
        if not (source_dir / path).exists():
            return

        shutil.copyfile(str(source_dir / path), str(destination_dir / path))


setup(
    name='app',
    version='0.1.0',
    # packages=find_packages(),
    packages=[],
    ext_modules=cythonize(
        # get_ext_paths('app', EXCLUDE_FILES),
        [
           Extension("app.*", ["app/*.py"]),
        ],
        build_dir="build",
        compiler_directives={'language_level': 3,
                             'always_allow_keywords': True,
                             }
    ),
    cmdclass={
        # 'build_py': build_py,
        'build_ext': MyBuildExt,
    }
)