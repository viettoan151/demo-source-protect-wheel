# Distribute python packages and protect them with Cython

This is an example application for demonstrating how to protect python source code and distribute package.<br/> 
(If you want to see my reference, please jump to last section. I will not explain **why** questions in this Readme.)

## Packaging python code
Packaging is grouping python codes of project into a module as blackbox.<br/>
Your package will be able to:
* install and manage as *pip* library.
* specify as a dependency for another package.
* add and distribute with documentation.

With **Cython**, in advanced, your python code will be compiled to object files (.pyd in Windows, .so in Linux). <br/>
And it's difficult to reverse your release.<br/>

I will go step by step from structure of this example, how to setup, build, and verify your result.
#### Folder structure
A project that has **app** package will look like: 
```
root project directory
├── app                 <-- application folder
│   ├── includes        <-- include folder (an example folder that you want to copy to wheel)
│   ├── core.py         <-- python source code
│   ├── main.py         <-- python source code
│   └── __init__.py     <-- package mandatory file
├── example2.py         <-- script for testing *app*
└── setup.py            <-- script for packaging 
└── setup_cython.py     <-- Run it, instead of above script, to package with Cython
```
##### *Mandatory files:*
* **\_\_init__.py**: Folder of an application must contain  **\_\_init__.py** file. This file can be blanked in simple project. <br/>
    But for a Cython packaging, you have to explicitly export your application modules there. <br/>
    ```python
    from __future__ import print_function
    from . import main
    from .core import greeting
    from .main import hello
    from .main import hello2
    
    print('Hello from __init__')
    ```
  In above **\_\_init__.py** file, I explicitly declare three functions that my **app** will provide.<br/>
  These functions are implemented in another python files.
  
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
* **example2.py**: in this file, I include **app** as a library. And I use functions in **app**.

##### *Advance:*
* **setup_cython.py**: this file will be used, instead of **setup.py**, when you need to hide your python code.<br/>
    It contains overrided functions of Cython utilities.<br/>
    This file is required to be modified, to adapt with each your application.
    (*Please read this file carefully before use for other application*)

##### *Notice:*
You can also see another example of folder structure in [link](https://python-packaging.readthedocs.io/en/latest/minimal.html) .<br/>
Your application code may be organized different with above structure. Steps will different with this guide.<br/>

#### Set up environment
```shell script
$ git clone https://github.com/viettoan151/demo-source-protect-wheel.git
$ cd demo-source-protect-wheel

$ virtualenv .venv --python=python3.6
$ source .venv/bin/activate
$ pip3 install Cython
``` 

#### Build package
In simple, you just run *setup.py* script to generate wheel files.
```shell script
$ rm -rf app.egg-info dist build
$ python3 setup.py bdist_wheel
```
Your wheel is generated in [dist/](dist/), name *app-x.x.x-py3-none-any.whl* <br/>
(From my understanding *x.x.x* is version of **app**, *py3* is python3 compatibility, *none-any* is independent from OS and architecture)<br/><br/>
But above wheel does not hide your python code. Unzip this wheel and check yourself.<br/>
Let's try the next script, *setup_cython.py*:
```shell script
$ rm -rf app.egg-info dist build
$ python3 setup_cython.py bdist_wheel
```
Your wheel is generated in [dist/](dist/), name *app-x.x.x-cp36-cp36m-linux_x86_64.whl* <br/>
(Name is different with above! Now, this wheel is only compatible with python 3.6, Linux OS, and x86_64 architecture)<br/><br/>
OK, you already hide your code . Go next step to verify it!

#### Verify package
Unzip your wheel:
```shell script
$ unzip dist/app-0.1.0-cp36-cp36m-linux_x86_64.whl -d dist/app
```

In unzip folder, verify there is no python source code
```shell script
$ tree dist/app
dist/app
├── app
│    ├── core.cpython-36m-x86_64-linux-gnu.so
│    ├── includes
│    │    ├── example.bin
│    │    └── example.py
│    ├── __init__.cpython-36m-x86_64-linux-gnu.so
│    ├── __init__.py
│    └── main.cpython-36m-x86_64-linux-gnu.so
└── app-0.1.0.dist-info
    ├── METADATA
    ├── RECORD
    ├── top_level.txt
    └── WHEEL ...
```

And try to run example in extracted folder:
```shell script
$ cp example2.py dist/app
$ cd dist/app
$ python3 -m example2
Hello from __init__
Test 0: greeting function
--> Greeting
Test 1: hello2 functiond
--> Hello world2
Test done
```


## References
[Python Guideline](https://packaging.python.org/tutorials/packaging-projects/) <br/>
[Python Sample project](https://github.com/pypa/sampleproject) <br/>
[Simple to complicated with Cython](https://medium.com/swlh/distributing-python-packages-protected-with-cython-40fc29d84caf) <br/>
[Advance in Cython](https://bucharjan.cz/blog/using-cython-to-protect-a-python-codebase.html)

