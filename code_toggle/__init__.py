
import os
from IPython.display import display, HTML


def toggle_code_cells(init_code_shown=True):

    dir_path = os.path.dirname(os.path.realpath(__file__))

    fn = os.path.join(dir_path, 'code_toggle.html')
    with open(fn, 'r') as f:
        html = f.read()

    fn = os.path.join(dir_path, 'code_toggle.js')
    with open(fn, 'r') as f:
        js = f.read()

    js = js.replace('__init_code_shown__', str(init_code_shown).lower())
    html = html.replace('__js_code__', js)

    display(HTML(html))
