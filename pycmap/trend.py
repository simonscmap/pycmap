"""
Author: Mohammad Dehghani Ashkezari <mdehghan@uw.edu>

Date: 2019-07-05

Function: Class definitions for line and scatter graphs.
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
from math import pi
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






class Trend(BaseGraph):
    """Abstracts trend (line/scatter) graphs."""
    def __init__(
                self, 
                data, 
                variable, 
                line=True
                ):

        """
        :param dataframe data: data to be visualized.
        :param str variable: variable name.
        :param bool line: if True, line plot is added to markers.
        """
        super().__init__()
        self.data = data
        self.variable = variable
        self.line = line


    def render(self):
        """Display the graph object."""
        super().render()


    def graph_obj(self):
        """Creates an instance from one of the derived classes of Trend."""
        vizEngine = get_vizEngine().lower().strip()
        obj = None
        if vizEngine == 'bokeh':
            obj = TrendBokeh(self.data, self.variable)
        elif vizEngine == 'plotly':
            obj = TrendPlotly(self.data, self.variable)
        return obj




class TrendBokeh(Trend):
    """
    Use this class to make trend graphs using bokeh library.
    """

    def __init__(
                self, 
                data, 
                variable,
                line=True, 
                toolbarLocation='above',
                fillColor='grey', 
                lineColor='purple', 
                lineWidth=2, 
                hoverFillColor='firebrick',
                hoverLineColor='white',
                fillAlpha=0.3,
                hoverAlpha=0.3,
                msize=20,
                timeSeries=True
                ):

        """
        :param str toolbarLocation: location of graph toolbar.
        :param str fillColor: marker color.
        :param str lineColor: line color.
        :param int lineWidth: line width.
        :param str hoverFillColor: color of markers when mouse hover over.
        :param str hoverLineColor: color of marker's border lines when mouse hover over.
        :param float fillAlpha: marker opacity.
        :param float hoverAlpha: marker opacity when mouse hover over.
        :param int msize: marker size.
        :param bool timeSeries: True if it is timeSeries data.
        """
        super().__init__(data, variable, line)
        self.toolbarLocation = toolbarLocation
        self.fillColor = fillColor
        self.lineColor = lineColor
        self.lineWidth = lineWidth
        self.hoverFillColor = hoverFillColor
        self.hoverLineColor = hoverLineColor
        self.fillAlpha = fillAlpha
        self.hoverAlpha = hoverAlpha
        self.msize = msize
        self.timeSeries = timeSeries
        self.tools = get_bokeh_tools()


    def render(self):
        """Display the graph object."""
        super().render()
        p = figure(
                    tools=self.tools, 
                    toolbar_location=self.toolbarLocation, 
                    plot_width=self.width, 
                    plot_height=self.height,
                    title=self.title
                    )

        if self.timeSeries and (isinstance(self.x[0], str) or isinstance(self.x[0], int) or isinstance(self.x[0], np.int64)):
            self.x = self.x.astype(str)    
            p.xaxis.ticker = np.arange(len(self.x))
            p.xaxis.major_label_overrides =  self.x.to_dict()
            self.x = np.arange(len(self.x))

        p.yaxis.axis_label = self.ylabel
        p.xaxis.axis_label = self.xlabel        
        cr = p.circle(
                    self.x, 
                    self.y, 
                    fill_color=self.fillColor, 
                    line_color=None, 
                    hover_fill_color=self.hoverFillColor, 
                    fill_alpha=self.fillAlpha, 
                    hover_alpha=self.hoverAlpha, 
                    hover_line_color=self.hoverLineColor, 
                    legend=self.legend,
                    size=self.msize
                    )
        if self.line:            
            p.line(
                self.x, 
                self.y, 
                line_color=self.lineColor, 
                line_width=self.lineWidth, 
                legend=self.legend
                )


        if self.timeSeries:
            if not isinstance(self.x[0], str):
                p.xaxis.formatter=DatetimeTickFormatter(
                                                        hours=["%d %B %Y"],
                                                        days=["%d %B %Y"],
                                                        months=["%d %B %Y"],
                                                        years=["%d %B %Y"],
                                                        )
            p.xaxis.major_label_orientation = pi/4


        p.add_tools(HoverTool(tooltips=None, renderers=[cr], mode='hline'))
        if not inline(): output_file(get_figure_dir() + self.variable + ".html", title=self.variable)        
        show(p)





class TrendPlotly(Trend):
    """
    Use this class to make trend graphs using plotly library.
    """    
    def __init__(
                self, 
                data, 
                variable, 
                line=True,
                color='purple', 
                fillAlpha=0.6,
                msize=15
                ):

        """
        :param str color: line and marker color.
        :param float fillAlpha: line and marker opacity.
        :param int msize: marker size.
        """
        super().__init__(data, variable, line)
        self.fillAlpha = fillAlpha
        self.color = color
        self.fillAlpha = fillAlpha
        self.msize = msize


    def render(self):
        """Display the graph object."""
        super().render()

        mode = 'markers'
        if self.line: mode = 'lines+markers'            
        data = [
                go.Scatter(
                             x=self.x,
                             y=self.y,
                             marker=dict(
                                        size=self.msize,
                                        color=self.color,
                                        opacity=self.fillAlpha
                                        ),
                             error_y=dict(
                                         type='data',
                                         array=self.yErr,
                                         color='rgba(7, 7, 7, .2)',                                         
                                         visible=True
                                         ),
                             mode = mode,
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
        self._save_plotly_(go, data, layout)                     
