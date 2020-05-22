"""
Author: Mohammad Dehghani Ashkezari <mdehghan@uw.edu>

Date: 2019-07-10

Function: Class abstraction of matching (colocalizing) variables.
"""



from .cmap import API  # noqa
from .common import (
    halt,
    print_tqdm,
    inline
)
import warnings
import numpy as np
import pandas as pd
import datetime
from dateutil.parser import parse
from tqdm import tqdm 
if inline(): from tqdm import tqdm_notebook as tqdm




class Match(object):
    """
    Abstracts the process of matching (colocalizing) a source variable with one or more than one target variables.
    The matching results rely on the spatio-temporal tolerance parameters.
    Notice the source has to be a single variable and cannot be a climatological variable. 
    You may pass empty string ('') as source variable if you only want to get the time and location info from the source table.
    The target variables (one or more) are matched with the source variable, if any match exists.
    Please note that the number of matching entries between each target variable and the source variable might vary depending on the temporal and spatial resolution of the target variable. 
    """

    def __init__(
        self,
        spname,
        sourceTable,
        sourceVariable,
        targetTables,
        targetVariables,
        dt1, 
        dt2, 
        lat1, 
        lat2, 
        lon1, 
        lon2, 
        depth1, 
        depth2,
        timeTolerance,
        latTolerance,
        lonTolerance,
        depthTolerance
        ):

        """
        :param str spname: stored procedure name that executes the matching logic.
        :param str sourceTable: table name of the source data set.
        :param str sourceVariable: the source variable. The target variables are matched (colocalized) with this variable.
        :param list targetTables: table names of the target data sets to be matched with the source data.
        :param list targetVariables: variable names to be matched with the source variable.
        :param str dt1: start date or datetime.
        :param str dt2: end date or datetime.
        :param float lat1: start latitude [degree N].
        :param float lat2: end latitude [degree N].
        :param float lon1: start longitude [degree E].
        :param float lon2: end longitude [degree E].
        :param float depth1: start depth [m].
        :param float depth2: end depth [m].
        :param list timeTolerance: float list of temporal tolerance values between pairs of source and target datasets. The size and order of values in this list should match those of targetTables. If only a single integer value is given, that would be applied to all target datasets. This parameter is in day units except when the target variable represents monthly climatology data in which case it is in month units. Notice fractional values are not supported in the current version.
        :param list latTolerance: float list of spatial tolerance values in meridional direction [deg] between pairs of source and target data sets. If only one value is given, that would be applied to all target data sets.
        :param list lonTolerance: float list of spatial tolerance values in zonal direction [deg] between pairs of source and target data sets. If only one value is given, that would be applied to all target data sets.
        :param list depthTolerance: float list of spatial tolerance values in vertical direction [m] between pairs of source and target data sets. If only one value is given, that would be applied to all target data sets.
        """

        if isinstance(sourceTable, list): 
            if len(sourceTable)>1:
                warnings.warn('Only one source table is allowed. The first item in the list ({}) was used.'.format(str(sourceTable[0])), UserWarning)
            sourceTable = str(sourceTable[0])
        if isinstance(sourceVariable, list): 
            if len(sourceVariable)>1:
                warnings.warn('Only one source variable is allowed. The first item in the list ({}) was used.'.format(str(sourceVariable[0])), UserWarning)
            sourceVariable = str(sourceVariable[0])
        if isinstance(targetTables, str): targetTables = [s.strip() for s in targetTables.split(',')]    
        if isinstance(targetVariables, str): targetVariables = [s.strip() for s in targetVariables.split(',')]    
        if isinstance(timeTolerance, int) or isinstance(timeTolerance, float): timeTolerance = [timeTolerance for _ in range(len(targetVariables))]    
        if isinstance(latTolerance, int) or isinstance(latTolerance, float): latTolerance = [latTolerance for _ in range(len(targetVariables))]    
        if isinstance(lonTolerance, int) or isinstance(lonTolerance, float): lonTolerance = [lonTolerance for _ in range(len(targetVariables))]    
        if isinstance(depthTolerance, int) or isinstance(depthTolerance, float): depthTolerance = [depthTolerance for _ in range(len(targetVariables))]    

        self.spname = spname        
        self.sourceTable = sourceTable
        self.sourceVariable = sourceVariable
        self.targetTables = targetTables
        self.targetVariables = targetVariables
        self.dt1 = dt1
        self.dt2 = dt2
        self.lat1 = lat1
        self.lat2 = lat2
        self.lon1 = lon1
        self.lon2 = lon2
        self.depth1 = depth1
        self.depth2 = depth2
        self.timeTolerance = timeTolerance
        self.latTolerance = latTolerance
        self.lonTolerance = lonTolerance
        self.depthTolerance = depthTolerance

        self.validateInit()
        return


    def validateInit(self):
        def is_number(val):
            return isinstance(val, float) or isinstance(val, int) or isinstance(val, np.int64)

        msg = ''
        if not isinstance(self.spname, str): msg += 'spname (stored procedure name) should be string literal. \n'
        if not isinstance(self.sourceTable, str): msg += 'source table name should be string literal. \n'
        if not isinstance(self.sourceVariable, str): msg += 'source variable name should be string literal. \n'
        if not isinstance(self.targetTables, list): msg += 'target table names should be a list of strings. \n'
        if not isinstance(self.targetVariables, list): msg += 'target variable names should be a list of strings. \n'
        if len(self.targetTables) != len(self.targetVariables): msg += 'targetTables list should have the same length as targetVariables list.'            
        if not isinstance(self.dt1, str): msg += 'dt1 (start date) should be string literal. \n'
        if not isinstance(self.dt2, str): msg += 'dt2 (end date) should be string literal. \n'

        if not is_number(self.lat1): msg += 'lat1 (start latitude) should be float or integer. \n'
        if not is_number(self.lat2): msg += 'lat2 (end latitude) should be float or integer. \n'
        if not is_number(self.lon1): msg += 'lon1 (start longitude) should be float or integer. \n'
        if not is_number(self.lon2): msg += 'lon2 (end longitude) should be float or integer. \n'
        if not is_number(self.depth1): msg += 'depth1 (start depth) should be float or integer. \n'
        if not is_number(self.depth2): msg += 'depth2 (end depth) should be float or integer. \n'

        # if not isinstance(self.lat1, float) and not isinstance(self.lat1, int): msg += 'lat1 (start latitude) should be float or integer. \n'
        # if not isinstance(self.lat2, float) and not isinstance(self.lat2, int) and not isinstance(self.lat2, np.int64): msg += 'lat2 (end latitude) should be float or integer. \n'
        # if not isinstance(self.lon1, float) and not isinstance(self.lon1, int): msg += 'lon1 (start longitude) should be float or integer. \n'
        # if not isinstance(self.lon2, float) and not isinstance(self.lon2, int) and not isinstance(self.lon2, np.int64): msg += 'lon2 (end longitude) should be float or integer. \n'
        # if not isinstance(self.depth1, float) and not isinstance(self.depth1, int): msg += 'depth1 (start depth) should be float or integer. \n'
        # if not isinstance(self.depth2, float) and not isinstance(self.depth2, int): msg += 'depth2 (end depth) should be float or integer. \n'
        if not isinstance(self.timeTolerance, list): msg += 'timeTolerance should be a list of floats or integers. \n'
        if not isinstance(self.latTolerance, list): msg += 'latTolerance should be a list of floats or integers. \n'
        if not isinstance(self.lonTolerance, list): msg += 'lonTolerance should be a list of floats or integers. \n'
        if not isinstance(self.depthTolerance, list): msg += 'depthTolerance should be a list of floats or integers. \n'
        try:
            self.timeTolerance = np.array(self.timeTolerance)   
        except:
            msg += 'timeTolerance should be a list of floats or integers. \n'
        try:
            self.latTolerance = np.array(self.latTolerance)   
        except:
            msg += 'latTolerance should be a list of floats or integers. \n'
        try:
            self.lonTolerance = np.array(self.lonTolerance)   
        except:
            msg += 'lonTolerance should be a list of floats or integers. \n'
        try:
            self.depthTolerance = np.array(self.depthTolerance)   
        except:
            msg += 'depthTolerance should be a list of floats or integers. \n'
        if len(self.timeTolerance) != len(self.targetTables) or len(self.timeTolerance) != len(self.targetVariables):
            msg += 'timeTolerance list should have the same length as target data sets list.'            
        if len(self.latTolerance) != len(self.targetTables) or len(self.latTolerance) != len(self.targetVariables):
            msg += 'latTolerance list should have the same length as target data sets list.'            
        if len(self.lonTolerance) != len(self.targetTables) or len(self.lonTolerance) != len(self.targetVariables):
            msg += 'lonTolerance list should have the same length as target data sets list.'            
        if len(self.depthTolerance) != len(self.targetTables) or len(self.depthTolerance) != len(self.targetVariables):
            msg += 'depthTolerance list should have the same length as target data sets list.'            

        if len(msg) > 0:        
            halt(msg)    
        return msg


    @staticmethod
    def _atomic_match(
                     spName, sourceTable, sourceVar, targetTable, targetVar, 
                     dt1, dt2, lat1, lat2, lon1, lon2, depth1, depth2, 
                     temporalTolerance, latTolerance, lonTolerance, depthTolerance
                     ):

        """
        Colocalizes the source variable (from source table) with a single target variable (from target table).
        The tolerance parameters set the matching boundaries between the source and target data sets. 
        Returns a dataframe containing the source variable joined with the target variable.
        """

        args = [spName, sourceTable, sourceVar, targetTable, targetVar, 
                dt1, dt2, lat1, lat2, lon1, lon2, depth1, depth2, 
                temporalTolerance, latTolerance, lonTolerance, depthTolerance]
        args = [str(arg) for arg in args]        
        query = "EXEC %s '%s', '%s','%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'" % tuple(args)
        return API().query(query)  



    def compile(self):
        """ 
        Loops through the target data sets and match them with the source data set according to the the accosiated tolerance parameters.
        Returns a compiled dataframe of the source and matched target data sets.
        """
        def shift_dt(dt, delta):
            delta = float(delta)
            dt = parse(dt)
            dt += datetime.timedelta(days=delta)
            # TODO: Handel monthly climatology data sets
            return dt.strftime("%Y-%m-%d %H:%M:%S")


        df = pd.DataFrame({})
        for i in tqdm(range(len(self.targetTables)), desc='overall'):
            data = self._atomic_match(
                                     self.spname, 
                                     self.sourceTable, 
                                     self.sourceVariable, 
                                     self.targetTables[i], 
                                     self.targetVariables[i], 
                                     shift_dt(self.dt1, -self.timeTolerance[i]),
                                     shift_dt(self.dt2, self.timeTolerance[i]),
                                     self.lat1 - self.latTolerance[i], 
                                     self.lat2 + self.latTolerance[i], 
                                     self.lon1 - self.latTolerance[i], 
                                     self.lon2 + self.latTolerance[i], 
                                     self.depth1 - self.depthTolerance[i], 
                                     self.depth2 + self.depthTolerance[i],
                                     self.timeTolerance[i], 
                                     self.latTolerance[i], 
                                     self.lonTolerance[i], 
                                     self.depthTolerance[i]
                                     )
            if len(data) < 1:
                print_tqdm('%d: No matching entry associated with %s.' % (i+1, self.targetVariables[i]), err=True)
                continue
            print_tqdm('%d: %s matched.' % (i+1, self.targetVariables[i]), err=False)
               
            if len(df) == 0:
                df = data
            elif (
                  df[df.columns[0]].equals(data[df.columns[0]]) and 
                  df['lat'].equals(data['lat']) and 
                  df['lon'].equals(data['lon'])
                  ):
                df[self.targetVariables[i]] = data[self.targetVariables[i]]
                df[self.targetVariables[i]+'_std'] = data[self.targetVariables[i]+'_std']
            else:
                print_tqdm('The matched dataframe corresponding to %s does not have the same size as the first targert variable. Please change the tolerance parameters.' % self.targetVariables[i], err=True)    

        return df
