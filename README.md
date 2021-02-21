# DISCLAIMER

This is a fork of  [opencollab/giws](https://github.com/opencollab/giws) repo. (After commit [97a5e4a
](https://github.com/opencollab/giws/commit/97a5e4aab23cb29171062d8a69f3374ef2e72d9c)) I am very stupid 
for python, my only change is to make it run with Python 3. I hope it will be helpful for some of you.

GIWS 
====

### Description 

GIWS is basically the opposite of SWIG.

When SWIG generates wrappers to call C/C++ functions/methods from other 
languages, GIWS creates wrapper for those who wants to call Java methods 
from C/C++.

GIWS is widely used in Scilab (from version 5.0) to drive the rendering and 
the GUI.

### Documentation

The best way to understand how to use GIWS is to read the examples

Code using C++ generated files
examples/*/main.cpp

XML declaration files:
examples/*/*.xml


### Usage

./giws -h to see the help

Options :

-o / --output-dir= <dir> :
Where files should be generated

-f / --description-file= <file> :
Specify the declaration file to use

-p / --per-package :
Creates a file per package instead of a file per object

-e / --throws-exception-on-error:
Throws a C++ exception instead of an exit(EXIT_FAILURE)

--header-extension-file : 
Specify the extension of the header file generated [Default : .hxx]

--body-extension-file :
Specify the extension of the body file generated [Default : .cpp]

-v / --version :
Displays the version and other information

-h / --help :
Displays the help

	

### Dependencies 

Obviously, as GIWS has been written in Python, it needs the Python interpretor
to work. And that's it !
 