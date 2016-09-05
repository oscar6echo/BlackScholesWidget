import ipywidgets as widgets
import traitlets as tl

import os, glob
from IPython.display import display, Javascript


class DatePickerWidget(widgets.DOMWidget):
    _view_name = tl.Unicode('DatePickerView').tag(sync=True)
    _view_module = tl.Unicode('datepicker').tag(sync=True)
    value = tl.Unicode().tag(sync=True)
    description = tl.Unicode('LabelView').tag(sync=True)

class NumberInputWidget(widgets.DOMWidget):
    _view_name = tl.Unicode('NumberInputView').tag(sync=True)
    _view_module = tl.Unicode('numberinput').tag(sync=True)
    value = tl.CFloat().tag(sync=True)
    description = tl.Unicode('LabelView').tag(sync=True)


def load_js_extensions():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    # print('js extensions loaded:')
    js = ''
    for fn in glob.glob(dir_path+'/*.js'):
        # print('\t'+os.path.basename(fn))
        with open(fn, 'r') as f:
            js += '\n' + f.read()
    display(Javascript(js))
