import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
    
NAME_APP = 'app'

setuptools.setup(
    name=NAME_APP,
    version='0.1.0',
    author = ["Toan Truong Viet"],
    author_email = ["viettoan151"],
    license = "MIT",
    description = "sample packaging",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/viettoan151/demo-source-protect-wheel",
    packages = setuptools.find_packages(),
    platforms = "Cross Platform",
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    
    # data_files=[('includes', ['app/includes/example.bin', 'app/includes/example.py'])],
    package_data={
        NAME_APP: ['includes/example.bin', 'includes/example.py'],
    },
)


# build command
# python3 setup.py bdist_wheel
# python3 setup.py install
# rm -rf app.egg-info dist build
# unzip dist/app-0.1.0-cp36-cp36m-linux_x86_64.whl -d dist/app
