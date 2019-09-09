"""
Author: Mohammad Dehghani Ashkezari <mdehghan@uw.edu>

Date: 2019-06-26

Function: Class definitions for histogram graphs.
"""

import os
from .baseGraph import BaseGraph
from .common import (
                     get_bokeh_tools,
                     get_figure_dir,
                     get_vizEngine,
                     inline
                    )
import numpy as np
from bokeh.plotting import figure, show, output_file
from bokeh.models import HoverTool
import plotly
import plotly.graph_objs as go


class Hist(BaseGraph):
    """Abstracts histogram graphs."""
    def __init__(
                self, 
                data, 
                variable, 
                bins=50,
                pdf=False,
                ):

        """
        :param dataframe data: data to be visualized.
        :param str variable: variable name.
        :param int bins: number of bins.
        :param bool pdf: If True the histogram represents a probability density function, otherwise absolute counts are displayed.
        """
        super().__init__()
        self.data = data
        self.variable = variable
        self.bins = bins
        self.pdf = pdf

    def render(self):
        """Display the graph object."""
        super().render()

    def graph_obj(self):
        """Creates an instance from one of the derived classes of Hist."""
        vizEngine = get_vizEngine().lower().strip()
        obj = None
        if vizEngine == 'bokeh':
            obj = HistBokeh(self.data, self.variable, self.bins, self.pdf)
        elif vizEngine == 'plotly':
            obj = HistPlotly(self.data, self.variable, self.bins, self.pdf)
        return obj         



class HistBokeh(Hist):
    """
    Use this class to make histogram graphs using bokeh library.
    """

    def __init__(
                self, 
                data, 
                variable, 
                bins,
                pdf,
                toolbarLocation='above',
                fillColor='dodgerblue', 
                lineColor=None, 
                hoverFillColor='firebrick',
                hoverLineColor='white',
                fillAlpha=0.4,
                hoverAlpha=0.7
                ):

        """
        :param str toolbarLocation: location of graph toolbar.
        :param str fillColor: color of bars.
        :param str lineColor: color of bar's border lines.
        :param str hoverFillColor: color of bars when mouse hover over.
        :param str hoverLineColor: color of bar's border lines when mouse hover over.
        :param float fillAlpha: bar opacity.
        :param float hoverAlpha: bar opacity when mouse hover over.
        """
        super().__init__(data, variable, bins, pdf)
        self.toolbarLocation = toolbarLocation
        self.fillColor = fillColor
        self.lineColor = lineColor
        self.hoverFillColor = hoverFillColor
        self.hoverLineColor = hoverLineColor
        self.fillAlpha = fillAlpha
        self.hoverAlpha = hoverAlpha
        self.tools = get_bokeh_tools()


    def render(self):
        """Display the graph object."""
        super().render()
        y = self.data[self.variable]
        try:    
            y = y[~np.isnan(y)]     
        except:
            pass    
        hist, edges = np.histogram(y, density=self.pdf, bins=self.bins)
        p = figure(
                    tools=self.tools, 
                    toolbar_location=self.toolbarLocation, 
                    plot_width=self.width, 
                    plot_height=self.height,
                    title=self.title
                    )
        p.yaxis.axis_label = self.ylabel
        p.xaxis.axis_label = self.xlabel
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
        if not inline(): output_file(get_figure_dir() + self.variable + ".html", title=self.variable)        
        show(p)





class HistPlotly(Hist):
    """
    Use this class to make histogram graphs using plotly library.
    """
    def __init__(
                self, 
                data, 
                variable, 
                bins,
                pdf,
                fillAlpha=0.8
                ):

        """
        :param float fillAlpha: bar opacity.
        """
        super().__init__(data, variable, bins, pdf)
        self.fillAlpha = fillAlpha


    def render(self):
        """Display the graph object."""
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
                           xaxis={'title': self.xlabel,
                                 'tickformat': '1.1e'
                                 },
                           yaxis={
                                 'title': self.ylabel,
                                 'tickformat': 'd'
                                 }
                          )  
        self._save_plotly_(go, data, layout)                     
