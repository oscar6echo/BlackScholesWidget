
from __future__ import division, print_function

import os
import numpy as np
import pandas as pd
import datetime as dt

import ipywidgets as widgets
# import traitlets as tl

import pyperclip
import ezhc as hc
import ezvis3d as v3d

from .custom_widgets_2 import load_js_extensions, NumberInputWidget
from .blackscholes_pricer import Price_Call, Price_Put


load_js_extensions()



li_input_data = [
    {   'name': 'Spot',
        'label': 'Spot',
        'value': 100,
        'min': 0.0001,
        'max': 200,
    },
    {   'name': 'Strike',
        'label': 'Strike',
        'value': 100,
        'min': 0.0,
        'max': 200,
    },
    {   'name': 'Mat',
        'label': 'Mat(y)',
        'value': 3,
        'min': 0.0001,
        'max': 10,
    },
    {   'name': 'Vol',
        'label': 'Vol(%)',
        'value': 20,
        'min': 0.0001,
        'max': 40,
    },
    {   'name': 'Rate',
        'label': 'Rate(%)',
        'value': 2,
        'min': -2,
        'max': 10,
    },
    {   'name': 'Div',
        'label': 'Div(%)',
        'value': 0,
        'min': -2,
        'max': 7,
    },
]

li_output_data = [
    ['d1', "d1"],
    ['N_d1', "N(d1)"],
    ['N_minus_d1', "N(-d1)"],
    ['N_prime_d1', "N'(d1)"],
    ['d2', "d2"],
    ['N_d2', "N(d2)"],
    ['N_minus_d2', "N(-d2)"],
    ['N_prime_d2', "N'(d2)"],
    ['price', "Price"],
    ['delta', "Delta"],
    ['gamma', "Gamma"],
    ['vega', "Vega"],
    ['theta', "Theta"],
    ['rho', "Rho"],
    ['voma', "Voma"],
    ['PV', "PV"],
    ['PV_K', "PV*K"],
    ['payoff', "Payoff"],
    ['PV_payoff', "PV*Payoff"]
]


# Build widget functions

def to_px(n): return str(n)+'px'
def to_int(s): return int(s[:-2]) if len(s)>2 else None


def build_Number(data, width, border=None):
    description = data['label']
    value = data['value']
    w = NumberInputWidget(description=description, value=value, width=to_px(width))
    if 'min' in data:
        w.min = data['min']
    if 'max' in data:
        w.max = data['max']
    w.border = border
    return w

def build_RadioButtons(description, options, value, width, border=None):
    w = widgets.RadioButtons(description=description, options=options, value=value, width=to_px(width))
    w.border = border
    return w

def build_Label(value, width, border=None):
    w = widgets.Label(value=value, width=to_px(width))
    w.border = border
    return w

def build_button(description, width, height):
    w = widgets.Button(description=description, button_style='info', width=to_px(width))
    return w

def build_HTML(value, width, height, border=None):
    w = widgets.HTML(value=value, width=to_px(width), height=to_px(height))
    w.border = border
    return w


def stack_box(li_box, orient, border=None):
    li_width = [to_int(b.layout.width) for b in li_box]

    if orient == 'H':
        box = widgets.HBox(li_box)
        width = sum([e for e in li_width if e is not None])
    elif orient=='V':
        box = widgets.VBox(li_box)
        width = max([e for e in li_width if e is not None])
    else:
        raise('Wrong orient')

    box.width = to_px(width + 5)
    box.border = border
    return box


# Copy & save utilities

def save_price(dic_price):
    if not os.path.exists('dump'):
        os.makedirs('dump')

    df = pd.DataFrame(pd.Series(dic_price))
    df.columns = ['Value']
    df.to_csv(os.path.join('dump', 'df_price.csv'))


def copy_price_to_clipboard(dic_price):
    res = ''
    for k, v in dic_price.items():
        res += k+'\t'+str(v)+'\n'
    pyperclip.copy(res)


def save_plot(html):
    if not os.path.exists('dump'):
        os.makedirs('dump')

    tag = 'BlackScholes_Plot'
    dated = dt.datetime.now().strftime('%Y%m%d_%H%M%S')
    JS_SAVE = hc._config.JS_SAVE
    with open(os.path.join('dump', dated+'_'+tag+'.html'), 'w') as f:
        js_load = ''.join(['<script src="%s"></script>' % e for e in JS_SAVE])
        contents = js_load+html
        f.write(contents)



class BlackScholesWidget(object):

    def __init__(self):
        self.li_input_data = li_input_data
        self.li_ip_name = [e['name'] for e in li_input_data]
        self.li_op_name = [e[0] for e in li_output_data]
        self.li_op_label = [e[1] for e in li_output_data]
        self.dic_op_name_label = dict(li_output_data)
        self.dic_op_label_name = {v: k for k, v in self.dic_op_name_label.items()}
        
        self.dic_price = None
        self.df_data_2d = None
        self.axis_z = None
        self.df_data_3d = None

        self.build_form()
        self.attach_events()
        self.init_form()
    

    # BUILD FORM

    def build_form(self):

        # DEBUG
        # border_1 = '1px solid blue'
        # border_2 = '1px solid red'
        # border_3 = '1px solid green'
        # border_RB = '1px solid magenta'
        border_1, border_2, border_3, border_RB = '', '', '', '',
        border_form = '1px solid black'
        
        # INPUT

        # input values of parameters
        width = 160
        li_data = li_input_data
        li_box = [build_Number(d, width) for d in li_data]
        b1 = stack_box(li_box, orient='V', border=border_1)

        # input values of min's
        li_data = [{'label': 'From', 'value': d['min']} for d in li_input_data]
        width = 150
        li_box = [build_Number(d, width) for d in li_data]
        b2 = stack_box(li_box, orient='V', border=border_1)

        # input values of max's
        li_data = [{'label': 'To', 'value': d['max']} for d in li_input_data]
        width = 150
        li_box = [build_Number(d, width) for d in li_data]
        b3 = stack_box(li_box, orient='V', border=border_1)

        # input values of values, min's and max's
        b4 = stack_box([b1, b2, b3], orient='H', border=border_2)

        # input values of option type
        self.wi_option = build_RadioButtons('Option', ['Call', 'Put'], 'Call', 130, border=border_RB)

        # input values of graph type
        self.wi_graph = build_RadioButtons('Graph', ['2D', '3D'], '2D', 130, border=border_RB)

        # input values of nb of steps from min's to max's
        self.wi_nbstep = build_Number({'label': 'Nb Steps (x, y)','value': 30, 'min': 2,'max': 100}, 150)

        # save button
        self.wi_save = build_button('Save Results', 200, 50)

        # input values of option type, graph type, nb of steps
        b5 = stack_box([self.wi_option, self.wi_graph, self.wi_nbstep], orient='H', border=border_1)
        b5 = stack_box([b5, self.wi_save], orient='V', border=border_1)

        # stacks input values
        b6 = stack_box([b4, b5], orient='V', border=border_2)

        # input values of x axis
        self.wi_x = build_RadioButtons('x', self.li_ip_name, 'Spot', 140, border=border_RB)

        # input values of y axis
        self.wi_y = build_RadioButtons('y', self.li_ip_name, 'Mat', 140, border=border_RB)

        # input values of z axis
        self.wi_z = build_RadioButtons('z', self.li_op_label, 'Price', 170, border=border_RB)

        # stacks input values
        b7 = stack_box([b6, self.wi_x, self.wi_y, self.wi_z], orient='H', border=border_3)


        # OUPUT

        # output labels 
        width = 80
        li_data = self.li_op_label
        li_box = [build_Label(d, width) for d in li_data]
        b8 = stack_box(li_box, orient='V', border=border_1)

        # labels 
        width = 15
        li_data = ['=']*len(li_output_data)
        li_box = [build_Label(d, width) for d in li_data]
        b9 = stack_box(li_box, orient='V', border=border_1)

        # output values of results
        width = 80
        li_data = ['0.00']*len(li_output_data)
        li_box = [build_Label(d, width) for d in li_data]
        b10 = stack_box(li_box, orient='V', border=border_1)

        # stacks output
        b11 = stack_box([b8, b9, b10], orient='H', border=border_3)

        # output plot zone
        width = 750
        height = 470
        self.wi_plot = build_HTML('Plot Zone', width=width, height=height)

        # stacks ouputs
        b12 = stack_box([b11, self.wi_plot], orient='H', border=border_3)

        # stacks inputs and ouputs
        self.form = stack_box([b7, b12], orient='V', border=border_form)

        # keep references
        self.li_wi_ip_val = b1.children
        self.li_wi_ip_min = b2.children
        self.li_wi_ip_max = b3.children
        self.li_wi_op_val = b10.children
        self.dic_wi_ip_val = dict(zip(self.li_ip_name, self.li_wi_ip_val))
        self.dic_wi_ip_min = dict(zip(self.li_ip_name, self.li_wi_ip_min))
        self.dic_wi_ip_max = dict(zip(self.li_ip_name, self.li_wi_ip_max))
        self.dic_wi_op_val = dict(zip(self.li_op_name, self.li_wi_op_val))
        


    # COMPUTE FUNCTIONS

    def compute_price(self):
        S, K, T, v, r, q = [self.dic_wi_ip_val[name].value for name in self.li_ip_name]
        v = v/100.0
        r = r/100.0
        q = q/100.0
        if self.wi_option.value == 'Call':
            self.dic_price = Price_Call(S, K, T, v, r, q)
        elif self.wi_option.value == 'Put':
            self.dic_price = Price_Put(S, K, T, v, r, q)
        


    def compute_plot_data_2d(self):
        dic_param = {}

        name_x = self.wi_x.value
        x_min = self.dic_wi_ip_min[name_x].value
        x_max = self.dic_wi_ip_max[name_x].value
        nb_step = self.wi_nbstep.value
        arr_x = np.linspace(x_min, x_max, num=nb_step, endpoint=True)
        dic_param[name_x] = list(arr_x)
        N_x = len(arr_x)

        for name in self.li_ip_name:
            if name != name_x:
                dic_param[name] = [self.dic_wi_ip_val[name].value] * N_x
                
        df = pd.DataFrame(dic_param)
        df = df[self.li_ip_name] # make sure right order ie S, K, T, v, r, q
        df['Vol'] = df['Vol']/100.0
        df['Rate'] = df['Rate']/100.0
        df['Div'] = df['Div']/100.0
        
        if self.wi_option.value == 'Call':
            Price = Price_Call
        elif self.wi_option.value == 'Put':
            Price = Price_Put
        else:
            raise('Wrong option value')

        li_price = []
        arr = df.values
        for k in range(len(arr)):
            param = list(arr[k])
            li_price.append(Price(*param))
        
        dfr = pd.DataFrame(li_price)
        dfr = dfr[dfr.columns.intersection(self.li_op_name)]
        dfr.index = arr_x
        dfr.index.name = name_x

        self.df_data_2d = dfr.copy()
        



    def compute_plot_data_3d(self):        
        dic_param = {}

        name_x = self.wi_x.value
        x_min = self.dic_wi_ip_min[name_x].value
        x_max = self.dic_wi_ip_max[name_x].value

        name_y = self.wi_y.value
        y_min = self.dic_wi_ip_min[name_y].value
        y_max = self.dic_wi_ip_max[name_y].value

        nb_step = self.wi_nbstep.value

        arr_x = np.linspace(x_min, x_max, num=nb_step, endpoint=True)
        N_x = len(arr_x)

        arr_y = np.linspace(y_min, y_max, num=nb_step, endpoint=True)
        N_y = len(arr_y)

        arr_x, arr_y = np.meshgrid(arr_x, arr_y)
        arr_x = arr_x.flatten()
        arr_y = arr_y.flatten()
        dic_param[name_x] = list(arr_x)
        dic_param[name_y] = list(arr_y)

        for name in self.li_ip_name:
            if (name != name_x) and (name != name_y) :
                dic_param[name] = [self.dic_wi_ip_val[name].value] * N_x * N_y

        df = pd.DataFrame(dic_param)
        df = df[self.li_ip_name] # make sure right order ie S, K, T, v, r, q
        df['Vol'] = df['Vol']/100.0
        df['Rate'] = df['Rate']/100.0
        df['Div'] = df['Div']/100.0

        if self.wi_option.value == 'Call':
            Price = Price_Call
        elif self.wi_option.value == 'Put':
            Price = Price_Put
        else:
            raise('Wrong option value')

        li_price = []
        arr = df.values
        for k in range(len(arr)):
            param = list(arr[k])
            li_price.append(Price(*param))

        dfr = pd.DataFrame(li_price)
        dfr[name_x] = arr_x
        dfr[name_y] = arr_y

        self.df_data_3d = dfr.copy()


    # DISPLAY AND PLOT FUNCTIONS

    def display_price(self):
        dic_price = {k: v for k, v in self.dic_price.items()}

        dic_label = {}
        for name in self.li_op_name:
            if name in dic_price:
                val = dic_price[name]
                label = '{:.4f}'.format(val)
                dic_label[name] = label
        if self.wi_option.value == 'Call':
            dic_label['N_minus_d1'] = '_'
            dic_label['N_minus_d2'] = '_'
        elif self.wi_option.value == 'Put':
            dic_label['N_d1'] = '_'
            dic_label['N_d2'] = '_'
        for name, label in dic_label.items():
            self.dic_wi_op_val[name].value = label

        for name in self.li_ip_name:
            dic_price[name] = self.dic_wi_ip_val[name].value
        copy_price_to_clipboard(dic_price)    
        save_price(dic_price)



    def display_plot_2d(self):
        df = self.df_data_2d
        label_z = self.wi_z.value
        name_z = self.dic_op_label_name[label_z]

        df = df[[name_z]]
        df.columns = [label_z]

        g = hc.Highcharts()
        g.chart.width = to_int(self.wi_plot.width)
        g.chart.height = to_int(self.wi_plot.height)
        g.chart.marginLeft = 80
        g.chart.marginTop = 10
        g.chart.marginBottom = 50
        g.chart.alignTicks = False
        g.chart.animation = False
        g.chart.borderColor = '#cccccc'
        g.chart.borderRadius = 0
        g.chart.borderWidth = 1
        g.chart.zoomType = 'xy'

        g.title.text = ''
        g.subtitle.text = ''

        g.xAxis.title.text = self.wi_x.value
        g.yAxis.title.text = label_z
        g.xAxis.gridLineWidth = 1.0
        g.xAxis.gridLineDashStyle = 'Dot'
        g.yAxis.gridLineWidth = 1.0
        g.yAxis.gridLineDashStyle = 'Dot'

        g.plotOptions.line.marker.enabled = False
        g.plotOptions.line.events.legendItemClick = 'function(){ return false; }'

        g.legend.enabled = False
        g.legend.layout = 'horizontal'
        g.legend.align = 'center'
        g.legend.verticalAlign = 'bottom'
        g.legend.floating = True
        g.legend.maxHeight = 0
        g.legend.x = 0
        g.legend.y = 0
        g.legend.backgroundColor = '#FFFFFF'

        g.tooltip.enabled = True
        g.tooltip.valueDecimals = 4
        g.tooltip.formatter = "function(){ return 'x: <b>'+ this.x.toFixed(4) + '</b>, ' + this.series.name + ': <b>'+ this.y.toFixed(4) +'</b>';}"

        g.credits.enabled = False
        g.exporting.enabled = False

        g.series = hc.build.series(df)

        html = g.html()
        self.wi_plot.value = html



    def display_plot_3d(self):
        df = self.df_data_3d
        name_x = self.wi_x.value
        name_y = self.wi_y.value
        li_name = []
        label_z = self.wi_z.value
        name_z = self.dic_op_label_name[label_z]
        df = df[[name_x, name_y, name_z]]
        df.columns = ['x', 'y', 'z']
        
        g = v3d.Vis3d()
        g.width = self.wi_plot.width
        g.height = self.wi_plot.height
        g.style = 'surface'
        g.showPerspective = True
        g.showGrid = True
        g.showShadow = False
        g.keepAspectRatio = False
        g.verticalRatio = 0.8
        g.xLabel = name_x
        g.yLabel = name_y
        g.zLabel = label_z
        g.cameraPosition = {'horizontal' : 0.9,
                            'vertical': 0.5,
                            'distance': 1.8}

        html = g.html(df, center=True, save=False)
        self.wi_plot.value = html


    # EVENTS 

    def update_price(self):
        self.compute_price()
        self.display_price()


    def update_plot_data_and_plot(self):
        if self.wi_graph.value == '2D':
            self.compute_plot_data_2d()
            self.display_plot_2d()
        elif self.wi_graph.value == '3D':
            self.compute_plot_data_3d()
            self.display_plot_3d()


    def update_plot(self):
        if self.wi_graph.value == '2D':
            self.display_plot_2d()
        elif self.wi_graph.value == '3D':
            self.display_plot_3d()


    def build_handle_new_val(self, name):
        wi_val = self.dic_wi_ip_val[name]
        wi_min = self.dic_wi_ip_min[name]
        wi_max = self.dic_wi_ip_max[name]

        def handle_new_val(change):
            new_val = min(max(wi_min.value, change['new']), wi_max.value)
            wi_val.value = new_val
            self.update_price()
            self.update_plot_data_and_plot()
            

        return handle_new_val


    def build_handle_new_min(self, name):
        wi_val = self.dic_wi_ip_val[name]
        wi_min = self.dic_wi_ip_min[name]
        wi_max = self.dic_wi_ip_max[name]
        wi_x = self.wi_x
        wi_y = self.wi_y

        def handle_new_min(change):
            new_val = min(wi_min.value, wi_val.value)
            wi_min.value = new_val
            wi_val.min = new_val
            if name in [self.wi_x.value, self.wi_y.value]:
                self.update_plot_data_and_plot()

        return handle_new_min


    def build_handle_new_max(self, name):
        wi_val = self.dic_wi_ip_val[name]
        wi_min = self.dic_wi_ip_min[name]
        wi_max = self.dic_wi_ip_max[name]

        def handle_new_max(change):
            new_val = max(wi_max.value, wi_val.value)
            wi_max.value = new_val
            wi_val.max = new_val
            if name in [self.wi_x.value, self.wi_y.value]:
                self.update_plot_data_and_plot()

        return handle_new_max


    def build_handle_new_graph(self):

        def handle_new_graph(change):
            if self.wi_graph.value == '2D':
                self.wi_y.disabled = True
            elif self.wi_graph.value == '3D':
                self.wi_y.disabled = False
            self.update_plot_data_and_plot()            

        return handle_new_graph


    def build_handle_new_option(self):

        def handle_new_option(change):
            self.update_price()
            self.update_plot_data_and_plot()

        return handle_new_option


    def build_handle_new_nbstep(self):

        def handle_new_nbstep(change):
            self.update_plot_data_and_plot()

        return handle_new_nbstep


    def build_handle_new_xy(self):

        def handle_new_xy(change):
            self.update_plot_data_and_plot()

        return handle_new_xy


    def build_handle_new_z(self):

        def handle_new_z(change):
            self.update_plot()

        return handle_new_z


    def build_onclick_save(self):

        def onclick_save(change):
            # save dataframe
            dic_price = {k: v for k, v in self.dic_price.items()}
            for name in self.li_ip_name:
                dic_price[name] = self.dic_wi_ip_val[name].value
            save_price(dic_price)
            
            # save html plot
            html = self.wi_plot.value
            save_plot(html)

        return onclick_save


    def attach_events(self):

        for name in self.li_ip_name:
            f = self.build_handle_new_val(name)
            self.dic_wi_ip_val[name].observe(f, names='value')
            
            f = self.build_handle_new_min(name)
            self.dic_wi_ip_min[name].observe(f, names='value')

            f = self.build_handle_new_max(name)
            self.dic_wi_ip_max[name].observe(f, names='value')

        f = self.build_handle_new_graph()
        self.wi_graph.observe(f, names='value')

        f = self.build_handle_new_option()
        self.wi_option.observe(f, names='value')

        f = self.build_handle_new_nbstep()
        self.wi_nbstep.observe(f, names='value')

        f = self.build_handle_new_xy()
        self.wi_x.observe(f, names='value')
        self.wi_y.observe(f, names='value')

        f = self.build_handle_new_z()
        self.wi_z.observe(f, names='value')

        f = self.build_onclick_save()
        self.wi_save.on_click(f)



    # INIT 

    def init_form(self):
        self.update_price()

        self.wi_graph.value = '2D'
        self.wi_y.disabled = True
        
        self.update_plot_data_and_plot()
        

