# Distributing python packages protected with Cython

This is a sample application for demonstrating how to protect app source code and distribute package. All magic is in the ``setup.py`` file.

## Reference examples
[Simple to complicated](https://medium.com/swlh/distributing-python-packages-protected-with-cython-40fc29d84caf) <br/>
[Advance in Cython](https://bucharjan.cz/blog/using-cython-to-protect-a-python-codebase.html)


## Packaging a project
#### Folder structure
```bash
root dir
├── app
│   ├── core.py
│   ├── main.py
│   └── __init__.py
├── example2.py
└── setup.py
```

Folder of an package must contain  \_\_init__.py file. This file can be blanked in simple project. But for a Cython packaging, this file must contain exported modules. <br/>
File setup.py is directive to build your package. A simple setup file:
```python
# coding: utf-8
import os

from setuptools import setup, find_packages

setup(
    name='app',
    version='0.1.0',
    packages=find_packages()
)
```

#### Set up environment
```
$ virtualenv .venv --python=python3.6
$ source .venv/bin/activate
$ pip install Cython
``` 


#### Build package

```
$ rm -rf app.egg-info dist build
$ python setup.py bdist_wheel
```


#### Verify package
In unzip folder, there is no python source code
```
$ unzip dist/app-0.1.0-cp36-cp36m-linux_x86_64.whl -d dist/app
$ tree dist/app
dist/app
├── app
│    ├── core.cpython-36m-x86_64-linux-gnu.so
│    ├── __init__.cpython-36m-x86_64-linux-gnu.so
│    ├── __init__.py
│    └── main.cpython-36m-x86_64-linux-gnu.so
└── app-0.1.0.dist-info
    ├── METADATA
    ├── RECORD
    ├── top_level.txt
    └── WHEEL
```
Run example
```
$ cp example2.py dist/app
$ cd dist/app
$ python -m example2

Hello from __init__
Test greeting
--> Greeting
Test hello
--> Hello world2
Success!
```