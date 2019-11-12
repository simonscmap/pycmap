"""
Author: Mohammad Dehghani Ashkezari <mdehghan@uw.edu>

Date: 2019-07-02

Function: Class definitions for section graphs.
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
from scipy.interpolate import griddata
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






class Section(BaseGraph):
    """Abstracts section graphs."""
    def __init__(
                self, 
                data, 
                variable, 
                levels=0
                ):

        """
        :param dataframe data: data to be visualized.
        :param str variable: variable name.
        :param int levels: number of contour levels. If zero, heatmap is created. If greater than zero, contour lines are superimposed on the heatmap. Currently, contour graphs are created by plotly library.
        """
        super().__init__()
        self.data = data
        self.variable = variable
        self.vmin, self.vmax = get_data_limits(self.data[self.variable])
        self.cmap = getPalette(self.variable)
        self.levels = int(np.abs(levels))        


    def render(self):
        """Display the graph object."""
        super().render()

    def graph_obj(self):
        """Creates an instance from one of the derived classes of Section."""
        vizEngine = get_vizEngine().lower().strip()
        obj = None
        if self.levels > 0 and vizEngine=='bokeh':
            warnings.warn('Please switch the vizEngine to "plotly" to create contour plots.', UserWarning)

        if vizEngine == 'bokeh':
            obj = SectionBokeh(self.data, self.variable, self.levels)
        elif vizEngine == 'plotly':
            obj = SectionPlotly(self.data, self.variable, self.levels)
        return obj         


    @staticmethod
    def interpolate(data, lat, lon, depth):
        """Interpolate the section data on a uniform grid."""
        depth = -1* depth 
        deltaZ = np.min( np.abs( depth - np.roll(depth, -1) ) )
        newDepth =  np.arange(np.min(depth), np.max(depth), deltaZ)        
        if len(lon) > len(lat):
            lon1, depth1 = np.meshgrid(lon, depth)
            lon2, depth2 = np.meshgrid(lon, newDepth)
            lon1 = lon1.ravel()
            lon1 = list(lon1[lon1 != np.isnan])
            depth1 = depth1.ravel()
            depth1 = list(depth1[depth1 != np.isnan])
            data = data.ravel()
            data = list(data[data != np.isnan])
            data = griddata((lon1, depth1), data, (lon2, depth2), method='linear')
        else:   
            lat1, depth1 = np.meshgrid(lat, depth)
            lat2, depth2 = np.meshgrid(lat, newDepth)
            lat1 = lat1.ravel()
            lat1 = list(lat1[lat1 != np.isnan])
            depth1 = depth1.ravel()
            depth1 = list(depth1[depth1 != np.isnan])
            data = data.ravel()
            data = list(data[data != np.isnan])
            data = griddata((lat1, depth1), data, (lat2, depth2), method='linear')
        return data, newDepth


    def squeez(self, data, lat, lon, depth):
        """Collapses the data array along either zonal or meridional direction, whichever is shorter in length."""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)       
            if len(lon) > len(lat):
                x_range=(np.min(lon), np.max(lon)) 
                y_range=(-np.max(depth), -np.min(depth))
                data = np.mean(data, axis=0)
                data = np.transpose(data)
                data = np.squeeze(data)
                xLabel = 'Longitude'
                averagedAlong = 'Latitude %2.2f N' % np.mean(lat) 
                x=np.min(lon) 
                y=-np.max(depth) 
                dw=np.max(lon)-np.min(lon) 
                dh=np.max(depth)-np.min(depth)
            else:
                x_range=(np.min(lat), np.max(lat)) 
                y_range=(-np.max(depth), -np.min(depth))
                data = np.mean(data, axis=1)
                data = np.transpose(data)
                data = np.squeeze(data)
                xLabel = 'Latitude'      
                averagedAlong = 'Longitude %2.2f E' % np.mean(lon) 
                x=np.min(lat) 
                y=-np.max(depth) 
                dw=np.max(lat)-np.min(lat)
                dh=np.max(depth)-np.min(depth)
        return data, xLabel, averagedAlong, x_range, y_range, x, y, dw, dh


    def make_layers(self):
        """Creates separate layers per each day."""
        #assuming temporal field is always the first column!
        timeCol = self.data.columns[0]
        times = self.data[timeCol].unique()  
        lat = self.data.lat.unique()
        lon = self.data.lon.unique()
        depths = self.data.depth.unique()
        shape = (len(lat), len(lon), len(depths))
        hours =  [None]
        if 'hour' in self.data.columns:
            hours = self.data.hour.unique()
        layers, titles = [], []
        for t in times:
            for h in hours:
                frame = self.data[self.data[timeCol] == t]
                if timeCol == 'time':
                    sub = self.variable + self.unit + ', ' + str(datetime.strptime(t, '%Y-%m-%dT%H:%M:%S').date())
                else:
                    sub = self.variable + self.unit + ', ' + timeCol + ': ' + str(t)    
                if h != None:
                    frame = frame[frame['hour'] == h]
                    sub = sub + ', hour: ' + str(h) + 'hr'
                try:    
                    layers.append(frame[self.variable].values.reshape(shape))
                    titles.append(sub)
                except Exception as e:
                    continue    
        return layers, titles, lat, lon, depths




class SectionBokeh(Section):
    """
    Use this class to make section graphs using bokeh library.
    """

    def __init__(
                self, 
                data, 
                variable,
                levels,
                toolbarLocation='right'
                ):

        """
        :param dataframe data: data to be visualized.
        :param str variable: variable name.
        :param int levels: number of contour levels. Not applicable to Bokeh library.
        :param str toolbarLocation: location of graph toolbar.
        """
        super().__init__(data, variable, levels)
        self.toolbarLocation = toolbarLocation
        self.tools = get_bokeh_tools()


    def render(self):
        """Display the graph object."""
        super().render()
        layers, titles, lat, lon, depth = self.make_layers()        
        plots = []
        for i in range(len(layers)):
            data, self.xlabel, averagedAlong, x_range, y_range, x, y, dw, dh = self.squeez(layers[i], lat, lon, depth)
            data, _ = self.interpolate(data, lat, lon, depth)
            p = figure(
                    tools=self.tools, 
                    toolbar_location=self.toolbarLocation, 
                    plot_width=self.width, 
                    plot_height=self.height,
                    x_range=x_range,
                    y_range=y_range,
                    title=titles[i] + ', ' + averagedAlong
                    )
            p.xaxis.axis_label = self.xlabel
            p.yaxis.axis_label = self.ylabel
            colorMapper = LinearColorMapper(palette=self.cmap, low=self.vmin, high=self.vmax)
            p.image(
                    image=[data], 
                    color_mapper=colorMapper, 
                    x=x, 
                    y=y, 
                    dw=dw, 
                    dh=dh
                    )

            p.add_tools(HoverTool(
                                tooltips=[
                                    (self.xlabel, '$x'),
                                    ('depth [m]', '$y'),
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






class SectionPlotly(Section):
    """
    Use this class to make section graphs using plotly library.
    """

    def __init__(
                self, 
                data, 
                variable,
                levels
                ):

        """
        :param dataframe data: data to be visualized.
        :param str variable: variable name.
        """
        super().__init__(data, variable, levels)
        
        

    def render(self):
        """Display the graph object."""
        super().render()
        layers, titles, lat, lon, depth = self.make_layers()
        for i in range(len(layers)):
            data, self.xlabel, averagedAlong, _, _, _, _, _, _ = self.squeez(layers[i], lat, lon, depth)
            if len(lon)>len(lat):
                LON, DEP = np.meshgrid(lon, depth)
                xvals = LON.flatten()
                yvals = -1 * DEP.flatten()
            else:
                LAT, DEP = np.meshgrid(lat, depth)
                yvals = -1 * DEP.flatten()
                xvals = LAT.flatten()
            vals = data.flatten()
            hovertext = []
            for k in range(len(vals)):
                if len(lon)>len(lat):
                    hovertext.append('lon: {:.2f}<br>depth [m]: {:.2f}<br>{}: {:.1e}'.format(xvals[k], yvals[k], self.variable + self.unit,vals[k]))
                else:    
                    hovertext.append('lat: {:.2f}<br>depth [m]: {:.2f}<br>{}: {:.1e}'.format(xvals[k], yvals[k], self.variable + self.unit,vals[k]))
            if self.levels == 0:
                data = [
                        go.Heatmap(
                                    x=xvals,
                                    y=yvals,
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
                                    x=xvals,
                                    y=yvals,
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
                            title=titles[i] + ', ' + averagedAlong,
                            width=self.width,
                            height=self.height,
                            xaxis={'title': self.xlabel},
                            yaxis={'title': self.ylabel}
                            )  
            self._save_plotly_(go, data, layout)                     
