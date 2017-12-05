"Plot a PNG using matplotlib in a web request, using Flask."

from app import app
from forms import PlotForm, Params, all_lines

from flask import Flask, make_response, render_template, request

import xsct_plots
import StringIO
import ast
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    
@app.route('/', methods = ['GET','POST'])
def main():
    form = PlotForm()
    parameters = Params()
    for line in all_lines:
        if line in form.choice_lines.data:
            parameters.lines.add(line)
        else:
            parameters.lines.discard(line)
    parameters.R = float(form.choice_R.data)
    parameters.ymin = float(form.choice_rap.data)
    parameters.K = float(form.choice_K.data)
    if form.choice_ptbin.data == 'highpt':
        parameters.highpt = True
    else:
        parameters.highpt = False
    if form.choice_scalevar.data == 'correl':
        parameters.narrowband = True
    else:
        parameters.narrowband = False
    return render_template('index.html',form=form, params=parameters)

@app.route('/form_prefill', methods = ['GET','POST'])
def form_prefill():
    form = PlotForm()
    parameters = Params()
    # transform to list by removing 'set' (doesn't work for python 2.7)
    parameters.lines = set(ast.literal_eval(request.args.get('lines')[3:]))
    parameters.R = ast.literal_eval(request.args.get('R'))
    parameters.ymin = ast.literal_eval(request.args.get('ymin'))
    parameters.K = ast.literal_eval(request.args.get('K'))
    parameters.highpt = ast.literal_eval(request.args.get('highpt'))
    parameters.narrowband = ast.literal_eval(request.args.get('narrowband'))
    # set the form values
    form.choice_lines.data = list(parameters.lines)
    form.choice_R.data = str(parameters.R)
    form.choice_rap.data = '%1.1f' % (parameters.ymin)
    form.choice_K.data = '%1.2f' % (parameters.K)
    if parameters.highpt:
        form.choice_ptbin.data = 'highpt'
    else:
        form.choice_ptbin.data = 'fullpt'
    if parameters.narrowband:
        form.choice_scalevar = 'correl'
    else:
        form.choice_scalevar = 'uncorrel'
    return render_template('index.html', form=form, params=parameters)
    
    
@app.route('/xsct_v_R.png')
def plot_vR():
    norm = 'LO'
    # transform to list by removing 'set' (doesn't work for python 2.7)
    vals = set(ast.literal_eval(request.args.get('lines')[3:]) )
    ymin = ast.literal_eval(request.args.get('ymin'))
    K = ast.literal_eval(request.args.get('K'))
    highpt = ast.literal_eval(request.args.get('highpt'))
    narrowband = ast.literal_eval(request.args.get('narrowband'))
    fig = xsct_plots.plot_vR(highpt, ymin, K, narrowband, vals, norm)
    canvas = FigureCanvas(fig)
    output = StringIO.StringIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    plt.close(fig)
    return response

@app.route('/xsct_v_pt.png')
def plot_vpt():
    norm = 'LO'
    # transform to list by removing 'set' (doesn't work for python 2.7)
    vals = set(ast.literal_eval(request.args.get('lines')[3:]))
    R = ast.literal_eval(request.args.get('R'))
    ymin = ast.literal_eval(request.args.get('ymin'))
    K = ast.literal_eval(request.args.get('K'))
    narrowband = ast.literal_eval(request.args.get('narrowband'))
    fig = xsct_plots.plot_vpt(R, ymin, K, narrowband, vals, norm)
    canvas = FigureCanvas(fig)
    output = StringIO.StringIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    plt.close(fig)
    return response

if __name__ == '__main__':
    app.run()
