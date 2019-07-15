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
import pandas as pd
from tqdm import tqdm 
if inline(): from tqdm import tqdm_notebook as tqdm




class Match(object):
    """
    Abstracts the process of matching (colocalizing) a source variable with one or more than one target variables.
    The matching results rely on the spatio-temporal tolerance parameters.
    Notice the source has to be a single variable and cannot be a climatological variable.
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
        :param list targetTable: table names of the target data sets to be matched with the source data.
        :param list targetVariable: variable names to be matched with the source variable.
        :param str dt1: start date or datetime.
        :param str dt2: end date or datetime.
        :param float lat1: start latitude [degree N].
        :param float lat2: end latitude [degree N].
        :param float lon1: start longitude [degree E].
        :param float lon2: end longitude [degree E].
        :param float depth1: start depth [m].
        :param float depth2: end depth [m].
        :param int timeTolerance: temporal matching tolerance between the source and target. timeTolerance is in day units excpet when the target variable represents monthly climatology data in which case it is in month units. 
        :param float latTolerance: spatial tolerance in meridional direction [deg].
        :param float lonTolerance: spatial tolerance in zonal direction [deg].
        :param float depthTolerance: spatial tolerance in vertical direction [m].
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



    def validateInit(self):
        msg = ''
        if not isinstance(self.spname, str):
            msg += 'spname (stored procedure name) should be string literal. \n'
        if not isinstance(self.sourceTable, str):
            msg += 'source table name should be string literal. \n'
        if not isinstance(self.sourceVariable, str):
            msg += 'source variable name should be string literal. \n'
        if not isinstance(self.targetTables, list):
            msg += 'target table names should be a list of strings. \n'
        if not isinstance(self.targetVariables, list):
            msg += 'target variable names should be a list of strings. \n'
        if not isinstance(self.dt1, str):
            msg += 'dt1 (start date) should be string literal. \n'
        if not isinstance(self.dt2, str):
            msg += 'dt2 (end date) should be string literal. \n'
        if not isinstance(self.lat1, float) and not isinstance(self.lat1, int):
            msg += 'lat1 (start latitude) should be float or integer. \n'
        if not isinstance(self.lat2, float) and not isinstance(self.lat2, int):
            msg += 'lat2 (end latitude) should be float or integer. \n'
        if not isinstance(self.lon1, float) and not isinstance(self.lon1, int):
            msg += 'lon1 (start longitude) should be float or integer. \n'
        if not isinstance(self.lon2, float) and not isinstance(self.lon2, int):
            msg += 'lon2 (end longitude) should be float or integer. \n'
        if not isinstance(self.depth1, float) and not isinstance(self.depth1, int):
            msg += 'depth1 (start depth) should be float or integer. \n'
        if not isinstance(self.depth2, float) and not isinstance(self.depth2, int):
            msg += 'lat2 (end depth) should be float or integer. \n'

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
        """ """

        df = pd.DataFrame({})
        for i in tqdm(range(len(self.targetTables)), desc='overall'):
            data = self._atomic_match(
                                     self.spname, self.sourceTable, self.sourceVariable, self.targetTables[i], self.targetVariables[i], 
                                     self.dt1, self.dt2, self.lat1, self.lat2, self.lon1, self.lon2, self.depth1, self.depth2,
                                     self.timeTolerance, self.latTolerance, self.lonTolerance, self.depthTolerance)
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

        return df
