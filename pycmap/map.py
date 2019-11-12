"""
Author: Mohammad Dehghani Ashkezari <mdehghan@uw.edu>

Date: 2019-06-30

Function: Class definitions for histogram graphs.
"""

import os
from .baseGraph import BaseGraph
from .common import (
                     get_bokeh_tools,
                     get_figure_dir,
                     get_vizEngine,
                     canvas_rect,
                     get_data_limits,
                     inline
                    )
from .colorMaps import getPalette
from datetime import datetime
import warnings
import numpy as np
from bokeh.plotting import figure, show, output_file
from bokeh.layouts import column
from bokeh.palettes import all_palettes
from bokeh.models import (
                          HoverTool, 
                          LinearColorMapper, 
                          BasicTicker, 
                          ColorBar, 
                          DatetimeTickFormatter
                          )
import plotly
import plotly.graph_objs as go






class Map(BaseGraph):
    """Abstracts map (image) graphs."""
    def __init__(
                self, 
                data, 
                variable,
                levels=0,
                surface3D=False
                ):

        """
        :param dataframe data: data to be visualized.
        :param str variable: variable name.
        :param int levels: number of contour levels. If zero, heatmap is created. If greater than zero, contour lines are superimposed on the heatmap. Currently, contour graphs are created by plotly library.
        :param bool surface3D: if true, creates a 3D surface plot (only available through plotly library).
        """
        super().__init__()
        self.data = data
        self.variable = variable
        self.vmin, self.vmax = get_data_limits(self.data[self.variable])
        self.cmap = getPalette(self.variable)
        self.levels = int(np.abs(levels))       
        self.surface3D = surface3D 


    def render(self):
        """Display the graph object."""
        super().render()

    def graph_obj(self):
        """Creates an instance from one of the derived classes of Map."""
        vizEngine = get_vizEngine().lower().strip()
        obj = None
        if self.levels > 0 and vizEngine=='bokeh':
            warnings.warn('Please switch the vizEngine to "plotly" to create contour plots.', UserWarning)
        if self.surface3D and vizEngine!='plotly':
            warnings.warn('Please switch the vizEngine to "plotly" to create 3D surface plots.', UserWarning)

        if vizEngine == 'bokeh':
            obj = MapBokeh(self.data, self.variable, self.levels, self.surface3D)
        elif vizEngine == 'plotly':
            obj = MapPlotly(self.data, self.variable, self.levels, self.surface3D)
        return obj         


    def make_layers(self):
        """Creates separate layers per each day, and depth level."""
        #assuming temporal field is always the first column!
        timeCol = self.data.columns[0]
        times = self.data[timeCol].unique()  
        lat = self.data.lat.unique()
        lon = self.data.lon.unique()
        shape = (len(lat), len(lon))
        depths, hours =  [None], [None]
        if 'depth' in self.data.columns:
            depths = self.data.depth.unique()
        if 'hour' in self.data.columns:
            hours = self.data.hour.unique()
        layers, titles = [], []
        for t in times:
            for h in hours:
                for z in depths:
                    frame = self.data[self.data[timeCol] == t]

                    if timeCol == 'time':
                        sub = self.variable + self.unit + ', ' + str(datetime.strptime(t, '%Y-%m-%dT%H:%M:%S').date())
                    else:
                        sub = self.variable + self.unit + ', ' + timeCol + ': ' + str(t)    

                    if h != None:
                        frame = frame[frame['hour'] == h]
                        sub = sub + ', hour: ' + str(h) + 'hr'
                    if z != None:
                        frame = frame[frame['depth'] == z] 
                        sub = sub + ', depth: %2.2f' % z + ' [m]'  
                    try:    
                        layers.append(frame[self.variable].values.reshape(shape))
                        titles.append(sub)
                    except Exception as e:
                        continue    
        return layers, titles, lat, lon





class MapBokeh(Map):
    """
    Use this class to make map graphs using bokeh library.
    """

    def __init__(
                self, 
                data, 
                variable, 
                levels,
                surface3D,
                toolbarLocation='right'
                ):

        """
        :param dataframe data: data to be visualized.
        :param str variable: variable name.
        :param int levels: number of contour levels. Not applicable to Bokeh library.
        :param str toolbarLocation: location of graph toolbar.
        """

        super().__init__(data, variable, levels, surface3D)
        self.toolbarLocation = toolbarLocation
        self.tools = get_bokeh_tools()


    def render(self):
        """Display the graph object."""
        super().render()
        layers, titles, lat, lon = self.make_layers()
        plots = []
        for i in range(len(layers)):
            p = figure(
                    tools=self.tools, 
                    toolbar_location=self.toolbarLocation, 
                    plot_width=self.width, 
                    plot_height=self.height,
                    x_range=(np.min(lon), np.max(lon)),
                    y_range=(np.min(lat), np.max(lat)),
                    title=titles[i]
                    )
            p.xaxis.axis_label = self.xlabel
            p.yaxis.axis_label = self.ylabel
            colorMapper = LinearColorMapper(palette=self.cmap, low=self.vmin, high=self.vmax)
            p.image(
                    image=[layers[i]], 
                    color_mapper=colorMapper, 
                    x=np.min(lon), 
                    y=np.min(lat), 
                    dw=np.max(lon)-np.min(lon), 
                    dh=np.max(lat)-np.min(lat)
                    )

            p.add_tools(HoverTool(
                                tooltips=[
                                    ('longitude', '$x'),
                                    ('latitude', '$y'),
                                    (self.variable + self.unit, '@image'),
                                ],
                                mode='mouse'
                                )
                        )

            colorBar = ColorBar(
                                color_mapper=colorMapper, 
                                ticker=BasicTicker(),
                                label_standoff=12, 
                                border_line_color=None, 
                                location=(0,0)
                                )

            p.add_layout(colorBar, 'right')
            plots.append(p)
        
        
        if not inline(): output_file(get_figure_dir() + self.variable + ".html", title=self.variable)        
        show(column(plots))    








class MapPlotly(Map):
    """
    Use this class to make map graphs using plotly library.
    """

    def __init__(
                self, 
                data, 
                variable,
                levels,
                surface3D
                ):

        """
        :param dataframe data: data to be visualized.
        :param str variable: variable name.
        :param int levels: number of contour levels. if zero, heatmap is created.
        :param bool surface3D: if true, creates a 3D surface plot (only available through plotly library).
        """
        super().__init__(data, variable, levels, surface3D)


    def render(self):
        """Display the graph object."""
        super().render()
        layers, titles, latVect, lonVect = self.make_layers()
        LON, LAT = np.meshgrid(lonVect, latVect)
        lon = LON.flatten()
        lat = LAT.flatten()
        for i in range(len(layers)):
            vals = layers[i].flatten()
            hovertext = []
            for k in range(len(vals)):
                hovertext.append('lon: {:.2f}<br>lat: {:.2f}<br>{}: {:.1e}'.format(lon[k], lat[k], self.variable + self.unit,vals[k]))
            if self.levels == 0:
                data = [
                        go.Heatmap(
                                    x=lon,
                                    y=lat,
                                    z=vals,
                                    colorscale=self.cmap,
                                    zmin=self.vmin,
                                    zmax=self.vmax,
                                    hoverinfo='text',
                                    text=hovertext            
                                    )
                        ]
            elif self.levels > 0:
                data = [
                        go.Contour(
                                    x=lon,
                                    y=lat,
                                    z=vals,
                                    colorscale=self.cmap,
                                    hoverinfo='text',
                                    text=hovertext,             
                                    connectgaps=False,
                                    contours=dict(
                                        coloring='heatmap',
                                        showlabels=True,
                                        start=self.vmin,
                                        end=self.vmax,
                                        size=(self.vmax-self.vmin) / float(self.levels)
                                        )
                                    # line=dict(smoothing=0.85)             
                                    )
                        ]                


            layout = go.Layout(
                            autosize=False,
                            title=titles[i],
                            width=self.width,
                            height=self.height,
                            xaxis={'title': self.xlabel},
                            yaxis={'title': self.ylabel}
                            )  



            if self.surface3D:
                data = [
                        go.Surface(
                                    x=lonVect,
                                    y=latVect,
                                    z=layers[i],
                                    colorscale=self.cmap,
                                    # hoverinfo='text',
                                    # text=hovertext            
                                    )
                        ]

                layout = go.Layout(
                                  autosize=False,
                                  title=titles[i],
                                  width=self.width,
                                  height=self.height,
                                  scene = dict(
                                              xaxis={'title': self.xlabel},
                                              yaxis={'title': self.ylabel},
                                              zaxis={'title': self.variable + self.unit}
                                              )
                                  )  


            self._save_plotly_(go, data, layout)                     
