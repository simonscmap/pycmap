"""
Author: Mohammad Dehghani Ashkezari <mdehghan@uw.edu>

Date: 2019-07-27

Function: Data preparation for ML procedures.
"""

import pandas as pd
from .common import halt



class Clean(object):
    """ 
    Implements various data pre-processing procedures.

    :param dataframe data: generic dataframe containing the data.
    """

    def __init__(self, data):
        self.data = data
        self.validateInit()


    def validateInit(self):
        msg = ''
        if not isinstance(self.data, pd.core.frame.DataFrame): msg += 'data should be a pandas dataframe object. \n'
        if len(msg) > 0:        
            halt(msg)    
        return msg


    def remove_nan_time_std(self):
        """
        A selection of basic data preparation steps: 
        Removes missing values, time column, and columns representing standard deviation values.

        Returns the processed dataframe.
        """
        self.breakTime()
        self.dropSTD()
        self.remove_all_nans()
        self.remove_any_nans()
        return self.data


    def remove_any_nans(self):
        """Removes rows which have at least one nan value."""     
        self.data.dropna(axis=0, how='any', inplace=True)   


    def remove_all_nans(self):
        """Removes columns and rows whose all of their values are nans."""        
        self.data.dropna(axis=0, how='all', inplace=True)   
        self.data.dropna(axis=1, how='all', inplace=True)  


    def breakTime(self):
        """
        Breaks the 'time' column into separate columns (year, month) and removes the time column itself.
        """
        if 'time' in self.data.columns: 
            self.data['time'] = pd.to_datetime(self.data['time']) 
            self.data['year'] = self.data['time'].dt.year 
            self.data['month'] = self.data['time'].dt.month 
            # self.data['dayOfYear'] = self.data['time'].dt.dayofyear 
            self.data.drop('time', axis=1, inplace=True)    


    def dropSTD(self):
        """Removes all columns representing standard deviation values, if exists."""
        for col in self.data.columns:
            if col[-4:] == '_std': self.data.drop(col, axis=1, inplace=True)   

