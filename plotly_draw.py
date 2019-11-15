import plotly
import plotly.offline as py
import plotly.graph_objs as go
py.init_notebook_mode(connected = True)

def getColorsList():
    return '''aliceblue, antiquewhite, aqua, aquamarine, azure,
beige, bisque, black, blanchedalmond, blue,
blueviolet, brown, burlywood, cadetblue,
chartreuse, chocolate, coral, cornflowerblue,
cornsilk, crimson, cyan, darkblue, darkcyan,
darkgoldenrod, darkgray, darkgrey, darkgreen,
darkkhaki, darkmagenta, darkolivegreen, darkorange,
darkorchid, darkred, darksalmon, darkseagreen,
darkslateblue, darkslategray, darkslategrey,
darkturquoise, darkviolet, deeppink, deepskyblue,
dimgray, dimgrey, dodgerblue, firebrick,
floralwhite, forestgreen, fuchsia, gainsboro,
ghostwhite, gold, goldenrod, gray, grey, green,
greenyellow, honeydew, hotpink, indianred, indigo,
ivory, khaki, lavender, lavenderblush, lawngreen,
lemonchiffon, lightblue, lightcoral, lightcyan,
lightgoldenrodyellow, lightgray, lightgrey,
lightgreen, lightpink, lightsalmon, lightseagreen,
lightskyblue, lightslategray, lightslategrey,
lightsteelblue, lightyellow, lime, limegreen,
linen, magenta, maroon, mediumaquamarine,
mediumblue, mediumorchid, mediumpurple,
mediumseagreen, mediumslateblue, mediumspringgreen,
mediumturquoise, mediumvioletred, midnightblue,
mintcream, mistyrose, moccasin, navajowhite, navy,
oldlace, olive, olivedrab, orange, orangered,
orchid, palegoldenrod, palegreen, paleturquoise,
palevioletred, papayawhip, peachpuff, peru, pink,
plum, powderblue, purple, red, rosybrown,
royalblue, saddlebrown, salmon, sandybrown,
seagreen, seashell, sienna, silver, skyblue,
slateblue, slategray, slategrey, snow, springgreen,
steelblue, tan, teal, thistle, tomato, turquoise,
violet, wheat, white, whitesmoke, yellow,
yellowgreen'''

def line(y, x = None, name = None):
    return go.Scatter(x = x, y = y, name = name)

def scutter(y, x = None, name = None):
    return go.Scatter(x = x, y = y, mode = 'markers', name = name)

def lineFill(y, x = None, name = None):
    return go.Scatter(x = x, y = y, fill = 'tozeroy', name = name)

def hist(x, nbins = None):
    return go.Histogram(x = x, nbinsx = nbins)

def box(x, name = None, rotation = 'vert', color = None, boxpoints = False):
    '''
    box(x, [name], [rotation], [boxpoints])
    x: input data
    name : name of graph
    rotation : {'vert', 'horiz'}
    color : marker color
    '''
    if rotation == 'vert':
        return go.Box(y = x, name = name, marker_color = color, boxpoints = boxpoints)
    elif rotation == 'horiz':
        return go.Box(x = x, name = name, marker_color = color, boxpoints = boxpoints)
    else:
        raise Exception('rotation have wrong value (%s)' % str(rotation))

def scutter3d(x, y, z, marker = None):
    if marker is None:
        marker = dict(
            size = 5,
            line = dict(
                color='rgba(217, 217, 217, 0.14)',
                width = 0.5),
            opacity = 0.8)

    trace = go.Scatter3d(
        x = x, y = y, z = z,
        mode = 'markers',
        marker = marker)
    return trace

def plot(data, title = None, xtitle = None, ytitle = None):
    fig = go.Figure()
    if type(data) == list:
        for _data in data:
            fig.add_trace(_data)
    else:
        fig.add_trace(data)

    fig['layout']['title'] = { 'text' : title }
    fig['layout']['xaxis'] = { 'title' : xtitle }
    fig['layout']['yaxis'] = { 'title' : ytitle }
    fig['layout']['hovermode'] = 'x'
    fig.show()

def plotSlider(data, labels = None, prefix = None, title = None, xtitle = None, ytitle = None):
    fig = go.Figure()

    if type(data) == list:
        for _data in data:
            _data.visible = False
            fig.add_trace(_data)
    else:
        fig.add_trace(data)

    fig.data[0].visible = True

    if labels is None:
        labels = [i for i in range(len(fig.data))]
    steps = []
    for i in range(len(fig.data)):
        step = dict(
            method = 'restyle',
            args = ['visible', [False] * len(fig.data)],
            label = str(labels[i])
        )
        step['args'][1][i] = True
        steps.append(step)

    if prefix is None:
        prefix = 'Select: '

    sliders = [dict(
        active = 0,
        currentvalue = {'prefix' : prefix},
            pad = {'t' : 50},
            steps = steps
        )]

    fig['layout']['sliders'] = sliders
    fig['layout']['title'] = { 'text' : title }
    fig['layout']['xaxis'] = { 'title' : xtitle }
    fig['layout']['yaxis'] = { 'title' : ytitle }
    fig['layout']['hovermode'] = 'x'
    fig.show()

def plotMultipleY(data, title = None, xtitle = None, ytitle = None):
    fig = go.Figure()
    if type(data) == list:
        if len(data) > 4:
            raise IOError('number of data more than 4')
        for i,_data in enumerate(data):
            _data.yaxis = 'y%d' % (i + 1)
            fig.add_trace(_data)

        fig['layout']['xaxis'] = dict(domain = [0, 1.0 - 0.1*(len(fig.data) - 2)])

        for i in range(1, len(fig.data)):
            fig['layout']['yaxis%d' % (i + 1)] = dict(
                side = 'right',
                overlaying = 'y',
                position = 1.0 - (i - 1)*0.1)

    else:
        fig.add_trace(_data)

    fig['layout']['title'] = { 'text' : title }
    fig['layout']['xaxis'] = { 'title' : xtitle }
    fig['layout']['yaxis'] = { 'title' : ytitle }
    fig['layout']['hovermode'] = 'x'
    fig.show()


#========================================================================================
#old functions for compatibility with old code
def pyPlot(x, y = None, text = None):
    if y is None:
        _line = line(y = x)
    else:
        _line = line(x = x, y = y)
    plot(_line, title = text)

def pyPlotFill(x, y = None):
    if y is None:
        _line = lineFill(y = x)
    else:
        _line = lineFill(x = x, y = y)
    plot(_line)
    
def pyScutter(x, y):
    plot(scutter(x = x, y = y))

def pyScutter3D(x, y, z):
    plot(scutter3d(x = x, y = y, z = z))

def pyPlotInOne(plot_arr, text = None):
    plot_data = []
    for data in plot_arr:
        plot_data.append(line(y = data))
    plot(plot_data, title = text)

def pyPlotInOneWY(plot_arr):
    plot_data = []
    for data in plot_arr:
        plot_data.append(line(x = data[0], y = data[1]))

    plot(plot_data)

def pyHist(x, nbins = None):
    plot(hist(x, nbins))
#========================================================================================
