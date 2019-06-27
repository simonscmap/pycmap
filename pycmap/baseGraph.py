"""
Author: Mohammad Dehghani Ashkezari <mdehghan@uw.edu>

Date: 2019-06-26

Function: Abstraction of base class for graphs.
"""


from abc import ABCMeta, abstractmethod
import numpy as np
import pandas as pd
from .common import halt


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
        :param array x: input data to be visualized.
        :param array y: input data to be visualized.
        :param array z: input data to be visualized.
        :param str title: the graphs's title.
        :param str xlabel: the graphs's x-axis label.
        :param str ylabel: the graphs's y-axis label.
        :param str zlabel: the graphs's z-axis label.
        :param str legend: the graphs's legend.
        :param float vmin: lower bound of data range (applicable to plots like maps and contours).
        :param float vmax: upper bound of data range (applicable to plots like maps and contours).
        :param str cmap: color map (applicable to plots like maps and contours).
        """
        pass


    @abstractmethod
    def render(self):
        pass

    @staticmethod
    def valid_data(data):
        """validate the input data tye."""
        res = isinstance(data, list) or isinstance(data, np.ndarray) or isinstance(data, pd.core.series.Series)
        msg = 'The input data should be of type list, or numpy array, or pandas series.'
        return res, msg


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
        if not isinstance(cmap, str): raise ValidationException('cmap must be of type string.')    
        self.__cmap = cmap                        
