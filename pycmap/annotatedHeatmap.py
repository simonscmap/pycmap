"""
Author: Mohammad Dehghani Ashkezari <mdehghan@uw.edu>

Date: 2019-07-11

Function: Class definitions for annotated heatmap graphs.
"""

import os
from .baseGraph import BaseGraph
from .common import (
                     get_figure_dir,
                     get_vizEngine,
                     inline
                    )
import warnings
import numpy as np
import plotly.figure_factory as ff



class AnnotatedHeatmap(BaseGraph):
    """Abstracts annotated heatmap graphs."""
    def __init__(self):
        super().__init__()


    def render(self):
        """Display the graph object."""
        super().render()

    def graph_obj(self):
        """Creates an instance from one of the derived classes of Hist."""
        vizEngine = get_vizEngine().lower().strip()
        obj = None
        if vizEngine != 'plotly':
            warnings.warn('Please switch the vizEngine to "plotly" to create annotated heatmap plots.', UserWarning)

        if vizEngine == 'plotly':
            obj = AnnotatedHeatmapPlotly()
        return obj         



class AnnotatedHeatmapPlotly(AnnotatedHeatmap):
    """
    Use this class to make annotated heatmap graphs using plotly library.
    """
    def __init__(self):
        super().__init__()


    def render(self):
        """Display the graph object."""
        super().render()

        fig = ff.create_annotated_heatmap(
                                         self.z,
                                         annotation_text = np.around(self.z, decimals=2),   
                                         x=self.x,
                                         y=self.y,
                                         colorscale=self.cmap,
                                         zmin=self.vmin,
                                         zmax=self.vmax
                                         )

        fig.layout.title = self.title
        fig.layout.autosize = False
        fig.layout.width = self.width
        fig.layout.height = self.height
        fig.layout.xaxis.title = self.xlabel
        fig.layout.yaxis.title = self.ylabel
        fig.layout.yaxis.autorange = 'reversed'

        self._save_figure_factory_(fig)                     
