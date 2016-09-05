## BlackScholes Widget

Based on [ipywidgets](https://ipywidgets.readthedocs.io/en/latest/)
Additionally the [demo notebook](http://nbviewer.ipython.org/github/oscar6echo/BlackScholesWidget/blob/master/demo_blackscholes_widget.ipynb) contains some javascript to
+ hide the code cells  
+ (re)initialize the notebook (ie restart kernel then run all cells)  

so as the make the notebook (almost) appear as a webapp.

## Installation

The following dependencies are required: 
+ numpy
+ pandas
+ datetime
+ ipywidgets >5.0
+ pyperclip
+ ezhc
+ ezvid3d

For the 3 unusual dependencies install with pip:
````
pip install pyperclip ezhc ezvis3d
````
For ipywidgets follow [these instructions](https://ipywidgets.readthedocs.io/en/latest/user_install.html)

## Python version

For now it only works with Python 2 (because of some parasite print statements in ezhc and ezvis3d - that I'll correct soon).

