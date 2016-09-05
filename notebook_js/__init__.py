
import os
from IPython.display import display, HTML

def build_html(name):
    dir_path = os.path.dirname(os.path.realpath(__file__))

    fn = os.path.join(dir_path, name+'.html')
    with open(fn, 'r') as f:
        html = f.read()

    fn = os.path.join(dir_path, name+'.js')
    with open(fn, 'r') as f:
        js = '<script>' + f.read() + '</script>'

    return html + js


def toggle_code_cells(init='Show'):
    """init = Show or Hide"""

    if init == 'Show':
        name = 'toggle_code_cells_init_show'
    elif init == 'Hide':
        name = 'toggle_code_cells_init_hide'
    else:
        raise('Wrong init')

    contents = build_html(name)
    display(HTML(contents))


def restart_kernel():
    name = 'restart_kernel'
    contents = build_html(name)
    display(HTML(contents))



def run_all_cells():
    name = 'run_all_cells'
    contents = build_html(name)
    display(HTML(contents))


def init_notebook():
    name = 'init_notebook'
    contents = build_html(name)
    display(HTML(contents))


def jupyter_credit():
    name = 'jupyter_credit'
    contents = build_html(name)
    display(HTML(contents))


