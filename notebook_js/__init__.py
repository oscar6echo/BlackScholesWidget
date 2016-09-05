
import os
from IPython.display import display, HTML


def toggle_code_cells(init='Show'):
    """init = Show or Hide"""

    dir_path = os.path.dirname(os.path.realpath(__file__))

    if init == 'Show':
        name = 'toggle_code_cells_init_show'
    elif init == 'Hide':
        name = 'toggle_code_cells_init_hide'
    else:
        raise('Wrong init')

    fn = os.path.join(dir_path, name+'.html')
    with open(fn, 'r') as f:
        html = f.read()

    fn = os.path.join(dir_path, name+'.js')
    with open(fn, 'r') as f:
        js = '<script>' + f.read() + '</script>'

    display(HTML(html+js))


def restart_kernel():

    dir_path = os.path.dirname(os.path.realpath(__file__))

    name = 'restart_kernel'

    fn = os.path.join(dir_path, name+'.html')
    with open(fn, 'r') as f:
        html = f.read()

    fn = os.path.join(dir_path, name+'.js')
    with open(fn, 'r') as f:
        js = '<script>' + f.read() + '</script>'

    display(HTML(html+js))


def run_all_cells():

    dir_path = os.path.dirname(os.path.realpath(__file__))

    name = 'run_all_cells'

    fn = os.path.join(dir_path, name+'.html')
    with open(fn, 'r') as f:
        html = f.read()

    fn = os.path.join(dir_path, name+'.js')
    with open(fn, 'r') as f:
        js = '<script>' + f.read() + '</script>'

    display(HTML(html+js))


def init_notebook():

    dir_path = os.path.dirname(os.path.realpath(__file__))

    name = 'init_notebook'

    fn = os.path.join(dir_path, name+'.html')
    with open(fn, 'r') as f:
        html = f.read()

    fn = os.path.join(dir_path, name+'.js')
    with open(fn, 'r') as f:
        js = '<script>' + f.read() + '</script>'

    display(HTML(html+js))

