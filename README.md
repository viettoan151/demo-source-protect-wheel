# Distributing python packages protected with Cython

This is a sample application for demonstrating how to protect an app source code and distribute package. All magic is in the ``setup.py`` file.

## Reference examples
[Python Guideline](https://packaging.python.org/tutorials/packaging-projects/) <br/>
[Simple to complicated](https://medium.com/swlh/distributing-python-packages-protected-with-cython-40fc29d84caf) <br/>
[Advance in Cython](https://bucharjan.cz/blog/using-cython-to-protect-a-python-codebase.html)


## Packaging python code
Packaging is grouping python modules of a task into as blackbox.<br/>
Your package will be able to:
* install with *pip*.
* specify as a dependency for another package.
* add and distribute with documentation.

#### Folder structure
A project that has **app** package will look like: 
```bash
root project directory
├── app                 <-- package folder
│   ├── includes        <-- wheel include folder (will be copied to wheel)
│   ├── core.py         <-- python source code
│   ├── main.py         <-- python source code
│   └── __init__.py     <-- package mandatory file
├── example2.py         <-- example test module script
└── setup.py            <-- module setup script
```
Mandatory files:
* **\_\_init__.py**: Folder of an package must contain  **\_\_init__.py** file. This file can be blanked in simple project. But for a Cython packaging, you have to export your package modules there. <br/>
* **setup.py**: File **setup.py** is directive to build your package. An simple setup file is ...
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
You also can see another example of structure in [link](https://python-packaging.readthedocs.io/en/latest/minimal.html).

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