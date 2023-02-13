from dash import Dash, dcc, html, Input, Output

import plotly.express as px
import plotly.graph_objects as go

import matplotlib.pyplot as plt
from PIL import Image
import pandas as pd
import numpy as np

import geopandas as gpd
from geojson import Polygon, Feature, FeatureCollection, dump

from shapely.geometry import Polygon

import os
# import sys
import json
import time as t

if not os.path.exists("images"):
    os.mkdir("images")

colors = {
    '1': 'red',
     '2': 'green',
     '3': 'blue',
     '4': 'yellow',
     '5': 'purple',
     '6': 'pink',
     '7': 'black',
     '8': 'pink',
     '9': 'orange'
}

# df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')
df = pd.read_csv('data.csv',
                 #delimiter=',',
                 #skipcols=1,
                 usecols=['x','y','t','category'],
                 nrows=1000
                 )
#print(df)
df["category"] = df["category"].astype(str)
#(numpy)
arr = df.to_numpy()
arr2 = arr.transpose()

path = 'C:\\Users\\datph\\Downloads\\countries.geojson'
#path = 'geoData.geojson'
mapData = gpd.read_file(path, driver='GeoJSON',
                        rows=10
                        )
image = Image.open('images/map.jpg')

fig = go.Figure()

app = Dash(__name__)

app.layout = html.Div([
    dcc.Graph(id='graph-with-slider', figure=fig, config={'scrollZoom':True}),
    dcc.Slider(
        min=df['t'].min(),
        max=df['t'].max(),
        step=None,
        value=df['t'].min(),
        #marks={str(t): str(t) for t in df['t'].unique()},
        marks=None,
        id='time-slider'
    ),
    html.Div(id='time'),
    #html.Div(id='signal'),
    html.Div(id='click-data')
])

@app.callback(
    Output('graph-with-slider', 'figure'),
    Output('time','children'),
    Input('time-slider', 'value'))
    #Input('click-data')
def update_figure(selected_time):
    start = t.time_ns()
    #(pandas)
    filtered_df = df[df.t <= selected_time]
    #(numpy)
    # idx = np.where(arr2[2] <= selected_time)[0]
    # filtered_df = pd.DataFrame(arr[idx, :], columns=['x', 'y', 't', 'category'])

    #(plotly)
    fig.data = []
    fig.add_trace(
        px.scatter(filtered_df, x="x", y="y", color = 'category',
                     # color_discrete_map={
                     #     '1': 'red',
                     #     '2': 'green',
                     #     '3': 'blue',
                     #     '4': 'yellow',
                     #     '5': 'purple',
                     #     '6': 'pink',
                     #     '7': 'black',
                     #     '8': 'pink',
                     #     '9': 'orange'},
                     title='test'))

    #(webgl/scattergl)
    # fig = go.Figure()
    # df_arr = []
    # for k in list(colors.keys()):
    #     category_df = filtered_df.loc[filtered_df['category'] == k]
    #     df_arr.append(category_df)
    #
    # i = 0
    # for k in list(colors.keys()):
    #     fig.add_trace(
    #         go.Scattergl(x=df_arr[i]['x'], y=df_arr[i]['y'],
    #                      mode='markers',
    #                      fillcolor=colors[k])
    #     )
    #     i+= 1

    #(add graph background img)
    fig.add_layout_image(
        source=image,
        xref="x",
        yref="y",
        x=0,
        y=0,
        yanchor='bottom',
        #xanchor='right',
        sizex=10000,
        sizey=-10000,
        sizing="stretch",
        opacity=0.5,
        layer="below"
    )
    #fig.update_layout(template="plotly_white")
    end = t.time_ns()
    print(end - start)

    fig.update_layout(transition_duration=100)

    #mouse click on pts event
    #fig.update_layout(clickmode='event+select')

    return fig, f'time: {selected_time}'

# @app.callback(
#     Output('graph-with-slider', 'children'),
#     Input('click-data', 'clickData'))
# def display_click_data(clickData):
#     print(clickData)
#     return json.dumps(clickData, indent=2)

if __name__ == '__main__':
    app.run_server(debug=True, threaded=True)

