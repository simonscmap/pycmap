"""
Author: Mohammad Dehghani Ashkezari <mdehghan@uw.edu>

Date: 2019-06-26

Function: Abstraction of base class for graphs.
"""


from abc import ABCMeta, abstractmethod
import os
from .common import inline, get_vizEngine, get_figure_dir 
import numpy as np
import pandas as pd
import matplotlib as plt
import matplotlib.cm as cm
from bokeh.io import output_notebook
import plotly

class ValidationException(Exception):
    pass


class BaseGraph(object):
    """
    This is the base class for other visualization classes.
    Use class for inheritance purposes.
    """
    
    __metaclass__ = ABCMeta

    def __init__(self):        
        """
        :param int width: graph's width in pixels.
        :param int height: graph's height in pixels.
        :param array x: input data to be visualized.
        :param array y: input data to be visualized.
        :param array z: input data to be visualized.
        :param array xErr: uncertainty associated with the input data.
        :param array yErr: uncertainty associated with the input data.
        :param array zErr: uncertainty associated with the input data.
        :param str title: the graphs's title.
        :param str xlabel: the graphs's x-axis label.
        :param str ylabel: the graphs's y-axis label.
        :param str zlabel: the graphs's z-axis label.
        :param str legend: the graphs's legend.
        :param str unit: data unit (if applicable).
        :param float vmin: lower bound of data range (applicable to plots like maps and contours).
        :param float vmax: upper bound of data range (applicable to plots like maps and contours).
        :param str cmap: color map (applicable to plots like maps and contours).
        :param str plotlyConfig: plotly config object (only applicable to plotly graphs).
        """

        self.__width = 800
        self.__height = 400
        self.__x = np.array([])
        self.__y = np.array([])
        self.__z = np.array([])
        self.__xErr = np.array([])
        self.__yErr = np.array([])
        self.__zErr = np.array([])
        self.__title = ''
        self.__xlabel = ''
        self.__ylabel = ''
        self.__zlabel = ''
        self.__legend = ''
        self.__unit = ''
        self.__vmin = None
        self.__vmax = None
        self.__cmap = ''
        self.__plotlyConfig = {
            'showLink': False, 
            'editable':False, 
            'staticPlot': False
            }
        return


    @abstractmethod
    def render(self):
        """Parent render function; will be extended by derived classes."""
        if inline():
            if get_vizEngine().lower().strip() == 'bokeh': output_notebook()
            if get_vizEngine().lower().strip() == 'plotly': plotly.offline.init_notebook_mode(connected=False)
        else:    
            figureDir = get_figure_dir()
            if not os.path.exists(figureDir): os.makedirs(figureDir)


    @staticmethod
    def valid_data(data):
        """validate the input data tye."""
        res = isinstance(data, list) or isinstance(data, np.ndarray) or isinstance(data, pd.core.series.Series)
        msg = 'The input data should be of type list, or numpy array, or pandas series.'
        return res, msg


    @staticmethod
    def enable_plotly_in_cell():
        """
        Enables plotly on colab cells. 
        Presumably, this is not necessay at plotly 4+ (calling fig.show() will be enough).
        Currently, plotly version 3+ is installed on colab.
        """
        import IPython
        from plotly.offline import init_notebook_mode
        display(IPython.core.display.HTML('''
                <script src="/static/components/requirejs/require.js"></script>
        '''))
        init_notebook_mode(connected=False)
  

    def _save_plotly_(self, go, data, layout):
        """
        Saves a plotly figure on local disk.
        Not meant to be called by user.
        """
        fig = go.Figure(data=data, layout=layout)
        if not self.__plotlyConfig.get('staticPlot'):
            if inline(): 
                self.enable_plotly_in_cell()              
                plotly.offline.iplot(fig, config=self.plotlyConfig)    
            else:
                plotly.offline.plot(fig, config=self.plotlyConfig, filename=get_figure_dir() + self.variable + '.html')
        else:
            plotly.io.write_image(fig, get_figure_dir() + self.variable + '.png')


    def _save_figure_factory_(self, fig):
        """
        Saves a plotly figure_factory on local disk.
        Not meant to be called by user.
        """
        fname = 'annotated_heatmap'
        if self.variable is not None and self.variable != '': fname = 'annotated_heatmap_' + self.variable
        if not self.__plotlyConfig.get('staticPlot'):
            if inline():                
                plotly.offline.iplot(fig, config=self.plotlyConfig)
            else:
                plotly.offline.plot(fig, config=self.plotlyConfig, filename=get_figure_dir() + fname + '.html')
        else:
            plotly.io.write_image(fig, get_figure_dir() + fname + '.png')


    @property
    def width(self):
        return self.__width   

    @width.setter
    def width(self, width):
        self.__width = width

    @property
    def height(self):
        return self.__height   

    @height.setter
    def height(self, height):
        self.__height = height


    @property
    def x(self):
        return self.__x    

    @x.setter
    def x(self, x):
        valid, msg = self.valid_data(x)
        if not valid: raise ValidationException(msg)    
        self.__x = x        

    @property
    def y(self):
        return self.__y    
        
    @y.setter
    def y(self, y):
        valid, msg = self.valid_data(y)
        if not valid: raise ValidationException(msg)    
        self.__y = y

    @property
    def z(self):
        return self.__z    
        
    @z.setter
    def z(self, z):
        valid, msg = self.valid_data(z)
        if not valid: raise ValidationException(msg)    
        self.__z = z

    @property
    def xErr(self):
        return self.__xErr    

    @xErr.setter
    def xErr(self, xErr):
        valid, msg = self.valid_data(xErr)
        if not valid: raise ValidationException(msg)    
        self.__xErr = xErr

    @property
    def yErr(self):
        return self.__yErr    

    @yErr.setter
    def yErr(self, yErr):
        valid, msg = self.valid_data(yErr)
        if not valid: raise ValidationException(msg)    
        self.__yErr = yErr

    @property
    def zErr(self):
        return self.__zErr    

    @zErr.setter
    def zErr(self, zErr):
        valid, msg = self.valid_data(zErr)
        if not valid: raise ValidationException(msg)    
        self.__zErr = zErr

    @property
    def title(self):
        return self.__title   
        
    @title.setter
    def title(self, title):
        if not isinstance(title, str): raise ValidationException('title must be of type string.')    
        self.__title = title


    @property
    def xlabel(self):
        return self.__xlabel   
        
    @xlabel.setter
    def xlabel(self, xlabel):
        if not isinstance(xlabel, str): raise ValidationException('xlabel must be of type string.')    
        self.__xlabel = xlabel        

    @property
    def ylabel(self):
        return self.__ylabel   
        
    @ylabel.setter
    def ylabel(self, ylabel):
        if not isinstance(ylabel, str): raise ValidationException('ylabel must be of type string.')    
        self.__ylabel = ylabel                

    @property
    def zlabel(self):
        return self.__zlabel   
        
    @zlabel.setter
    def zlabel(self, zlabel):
        if not isinstance(zlabel, str): raise ValidationException('zlabel must be of type string.')    
        self.__zlabel = zlabel                

    @property
    def legend(self):
        return self.__legend   
        
    @legend.setter
    def legend(self, legend):
        if not isinstance(legend, str): raise ValidationException('legend must be of type string.')    
        self.__legend = legend                        

    @property
    def unit(self):
        return self.__unit   
        
    @unit.setter
    def unit(self, unit):
        if not isinstance(unit, str): raise ValidationException('unit must be of type string.')    
        self.__unit = unit                        

    @property
    def vmin(self):
        return self.__vmin
        
    @vmin.setter
    def vmin(self, vmin):
        if not isinstance(vmin, float) and not isinstance(vmin, int): 
            raise ValidationException('vmin must be of type int or float.')    
        self.__vmin = vmin                        

    @property
    def vmax(self):
        return self.__vmax
        
    @vmax.setter
    def vmax(self, vmax):
        if not isinstance(vmax, float) and not isinstance(vmax, int): 
            raise ValidationException('vmax must be of type int or float.')    
        self.__vmax = vmax                                

    @property
    def cmap(self):
        return self.__cmap   
        
    @cmap.setter
    def cmap(self, cmap):
        """Gets cmap as string (matplotlib colormap names) or cmocean colormap and makes it compatible with suppoerted vizEngine."""
        colormap =cm.get_cmap(cmap)        
        if get_vizEngine().lower().strip() == 'bokeh':     
            paletteName = [plt.colors.rgb2hex(m) for m in colormap(np.arange(colormap.N))]
            cmap = paletteName
        elif get_vizEngine().lower().strip() == 'plotly':
            pl_entries = 255
            h = 1.0/(pl_entries-1)
            pl_colorscale = []
            for k in range(pl_entries):
                C = list(map(np.uint8, np.array(colormap(k*h)[:3])*255))
                pl_colorscale.append([k*h, 'rgb'+str((C[0], C[1], C[2]))])
            cmap = pl_colorscale
        self.__cmap = cmap                        

    @property
    def plotlyConfig(self):
        return self.__plotlyConfig
        
    @plotlyConfig.setter
    def plotlyConfig(self, plotlyConfig):
        if not isinstance(plotlyConfig, dict): 
            raise ValidationException('plotlyConfig must be of type dict.')    
        self.__plotlyConfig = plotlyConfig                                

