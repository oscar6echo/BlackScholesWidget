
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

