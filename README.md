# IPython Connect Imaris XTension
This extensions starts an iPython session, allowing one to interactively analyse their data using Python excellent numeric and scientific computation tools.

# Installation
You will need Python. On Windows I recommend installing the [Anaconda](http://continuum.io/downloads) distribution as it makes it easier to get all the dependencies. For nix systems, you can generally use the distributed version of Python or install it using the your systems package manager. On OS X, I recommend [Homebrew](http://brew.sh).

If you are willing, I also highly recommend getting familiar with virtual environments for Python, whether that be [virtualenv](https://virtualenv.pypa.io/) or the Anaconda flavour. I personally prefer to set up a virtualenv with all the dependencies that I need for analysis and iPython and then use that virtual env python executable in Imaris (see below).

## Dependencies
Full instructions for how to install iPython are give [here](http://ipython.org/install.html). For those being lazy:
```
pip install -U 'ipython[all]'
```

You will probably also was to install the other [SciPy](http://www.scipy.org) tools:
```
pip install -U numpy scipy matplotlib
```
and anything you might need for image analysis e.g., scikit-image, SimpleITK, mahotas etc.

## Configure Imaris XT module
You will need to configure the XT module in Imaris to point to your Python executable:

1. Edit --> Preferences --> Custom Tools
2. Point to 'Python application' field to your Python installation. Important: If you installed a virtualenv, you need to point Imaris to that.

## Installing the iPython connect XTension
There are several ways one could do this, the aim is to get XTIPythonConnect.py file into a place where Imaris can find it. Perhaps the easiest way would be to clone this repo:
```
cd ~/path/to/personal/imaris/xtensions
git clone https://github.com/keithschulze/xtipythonconnect.git
```
or to download the tar from github and put in somewhere where you would like to keep Imaris XTensions.

Then add that path into the 'XTension folders' box in the XT modules 'Custom Tools' config (see above).

# Running iPython Connect
When you run Imaris with the XT module enabled, you should now have a new menu item called `IPython Connect` in the 'Image Processing' menu. Click this will run the XTension.
IPythonConnector puts a variable `aImarisId` in the global scope of you IPython session, which allows you to connect to the current Imaris instance. The following example shows connecting to Imaris using the execellent [pIceImarisConnector](https://github.com/aarpon/pIceImarisConnector) library - I highly recommend this as it simplifies things a lot.

```python
from pIceImarisConnector import pIceImarisConnector as ice
# aImarisId is place in global scope when XTension is run
conn = ice(aImarisId)
```
