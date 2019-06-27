"""
Author: Mohammad Dehghani Ashkezari <mdehghan@uw.edu>

Date: 2019-06-26

Function: Implementation of bokeh histogram.
"""

from .baseGraph import BaseGraph
from .common import get_bokeh_tools
from .cmap import API  # noqa
import numpy as np
from bokeh.plotting import figure, show, output_file
from bokeh.models import HoverTool



class BokehHist(BaseGraph):
    """
    Use this class to make histogram graphs using bokeh library.
    """

    def __init__(
                self, 
                data, 
                table, 
                variable, 
                width=800, 
                height=400,
                toolbarLocation="above",
                fillColor="dodgerblue", 
                lineColor=None, 
                hoverFillColor="firebrick",
                hoverLineColor="white",
                fillAlpha=0.4,
                hoverAlpha=0.7
                ):

        """
        :param dataframe data: data to be visualized.
        :param str table: table name.
        :param str variable: variable name.
        :param int width: graph's width in pixels.
        :param int height: graph's height in pixels.
        """
        self.data = data
        self.table = table
        self.variable = variable
        self.width = width
        self.height = height
        self.toolbarLocation = toolbarLocation
        self.tools = get_bokeh_tools()
        self.unit = API().get_unit(table, variable)
        self.fillColor = fillColor
        self.lineColor = lineColor
        self.hoverFillColor = hoverFillColor
        self.hoverLineColor = hoverLineColor
        self.fillAlpha = fillAlpha
        self.hoverAlpha = hoverAlpha


    def render(self):
        y = self.data[self.variable]
        try:    
            y = y[~np.isnan(y)]     
        except Exception as e:
            pass    
        hist, edges = np.histogram(y, density=False, bins=50)
        p = figure(
                    tools=self.tools, 
                    toolbar_location=self.toolbarLocation, 
                    plot_width=self.width, 
                    plot_height=self.height
                    )
        p.yaxis.axis_label = self.ylabel
        p.xaxis.axis_label = self.variable + ' ' + self.unit
        cr = p.quad(
                    top=hist, 
                    bottom=0, 
                    left=edges[:-1], 
                    right=edges[1:], 
                    fill_color=self.fillColor, 
                    line_color=self.lineColor, 
                    hover_fill_color=self.hoverFillColor, 
                    fill_alpha=self.fillAlpha, 
                    hover_alpha=self.hoverAlpha, 
                    hover_line_color=self.hoverLineColor, 
                    legend=self.legend
                    )
        p.add_tools(HoverTool(tooltips=None, renderers=[cr], mode='mouse'))
        show(p)
