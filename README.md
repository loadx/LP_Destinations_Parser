Installation
==========
First you'll need python installed, this particular example works in python2 and will require a version greater than Python 2.5.

Once you have python installed you will probably want to install both [pip](http://www.pip-installer.org/en/latest/installing.html) & [virtualenv](http://www.virtualenv.org/en/latest/virtualenv.html#installation).

*Note: This environment is functionally similar to that of rbenv with bundler.*


With your environment prepared go ahead and create your virtualenv (if you're using virtualenv).

```bash
mkdir -p /path/where_you_want_to_install && cd $_
virtualenv .
```

Checkout the source code from this repository into a 'src' folder.
```bash
git clone path/to/this.git src/
```

Install the required pip packages
```bash
cd src
pip install -v -r requirements.txt
```

Activate the virtualenv
```bash
source /path/where_you_installed/bin/activate
```

To verify the virtualenv is working correctly.
```bash
which python
```
This should return something like /path/where_you_installed/bin/python

Now you have everything set up you can do one of two things:

Test
----
To run the tests switch to the src directory and run:
```bash
nosetests -v tests/*
```


Run program
---
To run the program 
```bash
python main.py <destinations.xml> <taxonomy.xml> /path/to/output_location
```
paths can be relative or absolute.
Remember you'll need your own xml data files.


Requirements
===
Python 2.5+
all included dependancies in requirements.txt
