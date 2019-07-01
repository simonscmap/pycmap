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
import numpy as np
from bokeh.plotting import figure, show, output_file
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
                variable
                ):

        """
        :param dataframe data: data to be visualized.
        :param str variable: variable name.
        """
        super().__init__()
        self.data = data
        self.variable = variable
        self.vmin, self.vmax = get_data_limits(self.data[self.variable])

    def render(self):
        super().render()

    def graph_obj(self):
        """Creates an instance from one of the derived classes of Map."""
        vizEngine = get_vizEngine().lower().strip()
        obj = None
        if vizEngine == 'bokeh':
            obj = MapBokeh(self.data, self.variable)
        elif vizEngine == 'plotly':
            obj = MapPlotly(self.data, self.variable)
        return obj         




class MapBokeh(Map):
    """
    Use this class to make map graphs using bokeh library.
    """

    def __init__(
                self, 
                data, 
                variable, 
                toolbarLocation='right'
                ):

        """
        :param str toolbarLocation: location of graph toolbar.
        """

        super().__init__(data, variable)
        self.cmap = all_palettes['Viridis'][256]
        self.toolbarLocation = toolbarLocation
        self.tools = get_bokeh_tools()


    def render(self):

        ###############################
        times = self.data[self.data.columns[0]].unique()  
        lat = self.data.lat.unique()
        lon = self.data.lon.unique()
        shape = (len(lat), len(lon))
        # ############################    

        super().render()
        p = figure(
                  tools=self.tools, 
                  toolbar_location=self.toolbarLocation, 
                  plot_width=self.width, 
                  plot_height=self.height,
                  x_range=(np.min(self.data.lon), np.max(self.data.lon)),
                  y_range=(np.min(self.data.lat), np.max(self.data.lat)),
                  title=self.title
                  )
        p.xaxis.axis_label = self.xlabel
        p.yaxis.axis_label = self.ylabel
        colorMapper = LinearColorMapper(palette=self.cmap, low=self.vmin, high=self.vmax)
        p.image(
                image=[self.data[self.variable].values.reshape(shape)], 
                color_mapper=colorMapper, 
                x=np.min(self.data.lon), 
                y=np.min(self.data.lat), 
                dw=np.max(self.data.lon)-np.min(self.data.lon), 
                dh=np.max(self.data.lat)-np.min(self.data.lat)
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
        if not inline(): output_file(get_figure_dir() + self.variable + ".html", title=self.variable)        
        show(p)





class MapPlotly(Map):
    """
    Use this class to make map graphs using plotly library.
    """

    def __init__(
                self, 
                data, 
                variable 
                ):

        """
        """

        super().__init__(data, variable)


    def render(self):
        super().render()

        histnorm = 'probability density' if self.pdf else ''
        data = [
                go.Histogram(
                             x=self.data[self.variable],
                             nbinsx=self.bins,
                             histnorm=histnorm,
                             name=self.legend,
                             opacity=self.fillAlpha
                            )
               ]

        layout = go.Layout(
                           autosize=False,
                           title=self.title,
                           width=self.width,
                           height=self.height,
                           xaxis={'title': self.xlabel},
                           yaxis={'title': self.ylabel}
                          )  
                 
        fig = go.Figure(data=data, layout=layout)
        if inline():
            plotly.offline.iplot(fig)
        else:
            plotly.offline.plot(fig, filename=get_figure_dir() + self.variable + ".html")