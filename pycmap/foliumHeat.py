"""
Author: Mohammad Dehghani Ashkezari <mdehghan@uw.edu>

Date: 2019-04-15

Function: Create a geospatial heatmap of sparse variables within a predefined space-time domain.
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))
from .common import (
                    normalize,
                    open_HTML,
                    get_figure_dir
                    )
import numpy as np
import folium
from folium.plugins import HeatMap, MarkerCluster, Fullscreen, MousePosition
import branca

colors = ['#FF8C00', '#0A8A9F', '#808080', '#90EE90', '#FFFFFF', '#5F9EA0', '#FF0000', '#0000FF', '#008000', '#800080', '#FFA500', '#8B0000', '#FFFFE0', '#FFC0CB']


def addLayers(m):
    tiles = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}'
    folium.TileLayer(tiles=tiles, attr=(' '), name='Blue Marble').add_to(m)
    folium.TileLayer(tiles='cartoDBdark_matter', name='Black Diamond').add_to(m)
    return m


def addMousePosition(m):
    formatter = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"
    MousePosition(
        position='bottomright',
        separator=' | ',
        empty_string='NaN',
        lng_first=True,
        num_digits=20,
        prefix='Coordinates:',
        lat_formatter=formatter,
        lng_formatter=formatter
    ).add_to(m)
    return m


def addMarkers(m, df, variable, unit):
    normalized = normalize(df[variable])
    mc = MarkerCluster(name=variable+unit, options={'spiderfyOnMaxZoom':'False', 'disableClusteringAtZoom' : '4'})
    for i in range(len(df)):
        folium.CircleMarker(location=[df.lat[i], df.lon[i]], radius=(normalized[i] * 10), tooltip='%s: %f%s <br> date: %s' % (variable, df[variable][i], unit, df['time'][i]), color='darkOrange', fill=True).add_to(mc)
    mc.add_to(m)
    return m


def addFullScreen(m):
    Fullscreen(
        position='topright',
        title='Full Screen',
        title_cancel='Exit',
        force_separate_button=True
    ).add_to(m)
    return m



def addTrackMarkers(m, df, cruise):
    mc = MarkerCluster(name=cruise, options={'spiderfyOnMaxZoom':'False', 'disableClusteringAtZoom' : '4'})
    for i in range(len(df)):
        folium.CircleMarker(location=[df.lat[i], df.lon[i]], radius=(2), color='darkOrange', fill=True).add_to(mc)
    mc.add_to(m)
    return m

def add_cruise_legend(m, cruises, legendColors):
    legendItems = ''
    for i in range(len(cruises)):
        legendItems += '<p><a style="color:'+legendColors[i]+';font-size:150%;margin-left:20px;">o</a>&emsp;'+cruises[i]+'</p>\n' 

    leg_height = 40 * len(cruises)
    legend_html = '''
    {% macro html(this, kwargs) %}
    <div style="
        position: fixed; 
        bottom: 50px;
        left: 10px;
        width: 250px;
        height: ''' + str(leg_height) + '''px;
        z-index:9999;
        font-size:14px;
        ">
    '''    
    legend_html += legendItems
    legend_html += '''</div>
    <div style="
        position: fixed; 
        bottom: 50px;
        left: 10px;
        width: 150px;
        height: ''' + str(leg_height) + '''px; 
        z-index:9998;
        font-size:14px;
        background-color: #ffffff;
        opacity: 0.7;
        ">
    </div>
    {% endmacro %}
    '''
    legend = branca.element.MacroElement()
    legend._template = branca.element.Template(legend_html)
    m.get_root().add_child(legend)
    return m

def folium_map(df, table, variable, unit):
    df.dropna(subset=[variable], inplace=True)
    df.reset_index(drop=True, inplace=True)
    normalized = normalize(df[variable])
    data = list(zip(df.lat, df.lon, normalized))

    m = folium.Map([df.lat.mean(), df.lon.mean()], tiles=None, zoom_start=3, control_scale=True, prefer_canvas=True)
    m.get_root().title = 'Map: ' + variable + unit
    m = addLayers(m)
    HeatMap(data, name='Data Density (%s)' % variable).add_to(m)
    m = addMarkers(m, df, variable, unit)
    m = addMousePosition(m)
    folium.LayerControl(collapsed=True).add_to(m)
    # m = addFullScreen(m)
    figureDir = get_figure_dir()
    if not os.path.exists(figureDir): os.makedirs(figureDir)

    fname = figureDir + 'heatMap.html'
    if os.path.exists(fname):
        os.remove(fname)
    m.save(fname)
    open_HTML(fname)
    return


def folium_cruise_track(df, stations=None):
    df['lon'] = np.where(df['lon'] > 0, df['lon']-360, df['lon'])
    m = folium.Map([df.lat.mean(), df.lon.mean()], tiles=None, zoom_start=3, control_scale=True, prefer_canvas=True)
    cruises = df['cruise'].unique()
    m.get_root().title = 'Cruise: ' + ', '.join(cruises)
    m = addLayers(m)
    legendColors = []
    for i in range(len(df)):
        ind = list(cruises).index(df.cruise[i]) % len(colors)
        if len(legendColors) == 0: legendColors.append(colors[ind])
        if legendColors[-1] != colors[ind]: legendColors.append(colors[ind])
        folium.CircleMarker(location=[df.lat[i], df.lon[i]], radius=(2), color=colors[ind], fill=True).add_to(m)

    if not stations is None:
        for i in range(len(stations)):
            folium.CircleMarker(location=[stations[i][1], stations[i][0]], radius=(8), color='#000000', fill=True).add_to(m)    
            folium.CircleMarker(location=[stations[i][1], stations[i][0]], radius=(5), color='#FFFFFF', fill=True).add_to(m)    

    m = addMousePosition(m)
    folium.LayerControl(collapsed=True).add_to(m)
    m = add_cruise_legend(m, cruises, legendColors)
    figureDir = get_figure_dir()
    if not os.path.exists(figureDir): os.makedirs(figureDir)

    fname = figureDir + 'cruiseTrack.html'
    if os.path.exists(fname):
        os.remove(fname)
    m.save(fname)
    open_HTML(fname)
    return      