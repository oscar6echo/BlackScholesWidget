import ipywidgets as widgets
import traitlets as tl

import os, glob
from IPython.display import display, Javascript


class ToggleCodeCellsWidget(widgets.DOMWidget):
    _view_name = tl.Unicode('ToggleCodeCellsView').tag(sync=True)
    _view_module = tl.Unicode('togglecodecells').tag(sync=True)
    code_shown = tl.Bool(True).tag(sync=True)


class InitNotebook(widgets.DOMWidget):
    _view_name = tl.Unicode('InitNotebookView').tag(sync=True)
    _view_module = tl.Unicode('initnotebook').tag(sync=True)


def load_js_extensions():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    # print('js extensions loaded:')
    js = ''
    for fn in glob.glob(dir_path+'/*.js'):
        # print('\t'+os.path.basename(fn))
        with open(fn, 'r') as f:
            js += '\n' + f.read()
    display(Javascript(js))
