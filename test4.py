from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go

import matplotlib.pyplot as plt
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

path = 'C:\\Users\\datph\\Downloads\\countries.geojson'
#path = 'geoData.geojson'
mapData = gpd.read_file(path, driver='GeoJSON',
                        #rows=10
                        )
print(len(mapData))

s_time = t.time_ns()
# fig = px.choropleth(#mapData,
#                     # zoom=2, center= {'lat': -70, 'lon': 20},
#                     geojson=mapData.geometry,
#                     locations=mapData.index,
# )

# fig = px.choropleth_mapbox(mapData,
#                     zoom=1, #center= {'lat': -70, 'lon': 20},
#                     geojson=mapData.geometry,
#                     locations=mapData.index,mapbox_style="carto-positron"
# )

# (shapes only)
# arr = [[] for i in range(2)]
# for i in range(len(mapData)):
#     if mapData.geometry[i].geom_type == 'MultiPolygon':
#         count = 0
#         for poly in list(mapData.geometry[i].geoms):
#             xx, yy = poly.exterior.coords.xy
#             arr[0].append(xx.tolist())
#             arr[1].append(yy.tolist())
#             if count > 6:
#                 break
#             count+=1
#     else:
#         xx, yy = mapData.geometry[i].exterior.coords.xy
#         arr[0].append(xx.tolist())
#         arr[1].append(yy.tolist())
# #print(arr)
# print(len(arr[0]))

# s_time = t.time_ns()
# fig = go.Figure()
# for i in range(len(arr[0])):
#     #fig.add_trace(go.Scatter(x=arr[0][i], y=arr[1][i], fill='toself'))
#     fig.add_trace(go.Scattermapbox(lon=arr[0][i], lat=arr[1][i], mode="lines", fill ="toself"))
#
# fig.update_layout(
#     mapbox = {'style': "carto-positron", 'center': {'lon': 30, 'lat': 30}, 'zoom': 2},
#     showlegend = False,
#     margin = {'l':0, 'r':0, 'b':0, 't':0})

ax = mapData.geometry.plot(cmap='OrRd')
ax.set_axis_off();
#
# e_time = t.time_ns()
# print(e_time-s_time)
#
# plt.show()

plt.savefig("images/map.jpg", bbox_inches='tight', transparent=True)
#fig.write_image("images/fig.jpg")

#fig.update_geos(fitbounds="locations", visible=False)
#fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
#fig.show()
