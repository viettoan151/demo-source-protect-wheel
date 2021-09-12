# Distribute python packages and protect them with Cython

This is a example application for demonstrating how to protect python source code and distribute package.<br/> 
(If you want to see my reference, please jump to last section. I will not explain **why** questions in this Readme.)

## Packaging python code
Packaging is grouping python codes of a task into a module as blackbox.<br/>
Your package will be able to:
* install with *pip*.
* specify as a dependency for another package.
* add and distribute with documentation.

In advance with **Cython**, your python code will be compiled to object files (.dll in Windows, .so in Linux). <br/>
And it's difficult to reverse your released.

#### Folder structure
A project that has **app** package will look like: 
```bash
root project directory
├── app                 <-- package folder
│   ├── includes        <-- wheel include folder (an example folder that you want to )
│   ├── core.py         <-- python source code
│   ├── main.py         <-- python source code
│   └── __init__.py     <-- package mandatory file
├── example2.py         <-- example test module script
└── setup.py            <-- module setup script
└── setup_cython.py     <-- Run it, instead of above script, to setup with Cython
```
##### Mandatory files:
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
    You also can see another example of structure in [link](https://python-packaging.readthedocs.io/en/latest/minimal.html).<br/>

##### Advance:
* **setup_cython.py**: this file will be used, instead of **setup.py**, when you need to hide your python code.<br/>
    It contains overrided functions of Cython utilities.<br/>
    This file is required to be modified, to adapt with each your application.
    (*Please read this file carefully before use for other application*)

#### Set up environment
```
$ virtualenv .venv --python=python3.6
$ source .venv/bin/activate
$ pip3 install Cython
``` 

#### Build package
In simple, you just run *setup.py* script to generate wheel files.
```
$ rm -rf app.egg-info dist build
$ python3 setup.py bdist_wheel
```
But above wheel does not help to hide your python code. <br/>
Let's try the next, *setup_cython.py*:
```
$ rm -rf app.egg-info dist build
$ python3 setup_cython.py bdist_wheel
```
OK, you already hide your code. Go next step to verify it!

#### Verify package
Unzip your wheel:
```
$ unzip dist/app-0.1.0-cp36-cp36m-linux_x86_64.whl -d dist/app
```

In unzip folder, verify there is no python source code
```
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

And try to run example:
```
$ cp example2.py dist/app
$ cd dist/app
$ python3 -m example2

Hello from __init__
Test greeting
--> Greeting
Test hello
--> Hello world2
Success!
```


## Referenced examples
[Python Guideline](https://packaging.python.org/tutorials/packaging-projects/) <br/>
[Simple to complicated](https://medium.com/swlh/distributing-python-packages-protected-with-cython-40fc29d84caf) <br/>
[Advance in Cython](https://bucharjan.cz/blog/using-cython-to-protect-a-python-codebase.html)

