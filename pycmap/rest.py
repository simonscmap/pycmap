"""
Author: Mohammad Dehghani Ashkezari <mdehghan@uw.edu>

Date: 2019-06-22

Function: Encapsulates RESTful API logic.
"""


import random
import requests
from requests.exceptions import HTTPError
from urllib.parse import urlencode
import numpy as np
import pandas as pd
from io import StringIO
from .common import (
    halt,
    print_tqdm,
    get_base_url,
    get_token,
    remove_angle_brackets,
    save_config, 
    inline
)



class APIError(Exception):
    '''
    Represents API related error.
    error.status_code will have http status code.
    '''

    def __init__(self, error, http_error=None):
        super().__init__(error['message'])
        self._error = error
        self._http_error = http_error

    @property
    def code(self):
        return self._error['code']

    @property
    def status_code(self):
        http_error = self._http_error
        if http_error is not None and hasattr(http_error, 'response'):
            return http_error.response.status_code

    @property
    def request(self):
        if self._http_error is not None:
            return self._http_error.request

    @property
    def response(self):
        if self._http_error is not None:
            return self._http_error.response



class _REST(object):
    """
    Handles RESTful requests to the Simons CMAP API.
    """

    def __init__(self,
                 token=None,
                 baseURL=None,
                 headers=None,
                 vizEngine=None,
                 exportDir=None,
                 exportFormat=None,
                 figureDir=None,
                 ):
        """
        :param str token: access token to make client requests.
        :param str baseURL: root endpoint of Simons CMAP API.
        :param dict headers: additional headers to add to requests.
        :param str vizEngine: data visualization library used to render the graphs.
        :param str exportDir: path to local directory where the exported data are stored.
        :param str exportFormat: file format of the exported files.
        """

        self._token = remove_angle_brackets(token) or get_token()
        self._baseURL = baseURL or get_base_url()
        self._headers = headers
        self._token_prefix = 'Api-Key '
        self._vizEngine = vizEngine
        self._exportDir = exportDir
        self._exportFormat = exportFormat
        self._figureDir = figureDir
        
        save_config(
                    token=self._token, 
                    vizEngine=self._vizEngine, 
                    exportDir=self._exportDir, 
                    exportFormat=self._exportFormat,
                    figureDir=self._figureDir 
                    )

        assert len(self._token) > 0, 'API key cannot be empty.'
        assert self._headers is None or isinstance(self._headers, dict), \
            'Expected dict, got %r' % self._headers


    def _request(
                self,
                route,
                method='GET',
                payload=None,
                baseURL=None
                ):
        baseURL = baseURL or self._baseURL
        headers = {'Authorization': self._token_prefix + self._token}
        if method.upper().strip() == 'GET':
            return self._atomic_get(route, headers, payload)
        else:
            return None


    def _atomic_get(self, route, headers, payload):
        """
        Submits a single GET request. Returns the body in form of pandas dataframe if 200 status.
        """               
        df = pd.DataFrame({})
        try:
            queryString = ''
            if payload is not None:
                queryString = urlencode(payload)
            url = self._baseURL + route + queryString
            resp = requests.get(url, headers=headers)  
            resp_text = resp.text   # not a big fan, a bit slow?
            if len(resp_text) < 50:
                if resp_text.lower().strip()  == 'unauthorized':
                    halt('Unauthorized API key!')
            try:
                if len(resp_text.strip())>0:
                    df = pd.read_csv(StringIO(resp_text))
                    if 'time' in df.columns: 
                        df['time'] = pd.to_datetime(df['time'])
                        df['time'] = df['time'].dt.strftime('%Y-%m-%dT%H:%M:%S')

                    # json_list = [orjson.loads(line) for line in resp_text.splitlines()]
                    # df = pd.DataFrame(json_list, columns=list(json_list[0]))
            except Exception as e:
                print_tqdm('REST API Error (status code {})'.format(resp.status_code), err=True)
                print_tqdm(resp_text, err=True)  
                print('********* Python Error Msg **********')
                print(e)
        except HTTPError as http_error:
            # look for resp.status_code
            raise
        return df




    @staticmethod
    def validate_sp_args(
                        table,
                        variable,
                        dt1,
                        dt2,
                        lat1,
                        lat2,
                        lon1,
                        lon2,
                        depth1,
                        depth2
                        ):

        """
        :param str table: table name (each data set is stored in one or more than one table).
        :param str variable: variable short name which directly corresponds to a field name in the table.
        :param str dt1: start date or datetime.
        :param str dt2: end date or datetime.
        :param float lat1: start latitude [degree N].
        :param float lat2: end latitude [degree N].
        :param float lon1: start longitude [degree E].
        :param float lon2: end longitude [degree E].
        :param float depth1: start depth [m].
        :param float depth2: end depth [m].
        """

        def is_number(val):
            return isinstance(val, float) or isinstance(val, int) or isinstance(val, np.int64)

        msg = ''
        if not isinstance(table, str):
            msg += 'table name should be string. \n'
        if not isinstance(variable, str):
            msg += 'variable name should be string. \n'
        if not isinstance(dt1, str):
            msg += 'dt1 (start date) should be string. \n'
        if not isinstance(dt2, str):
            msg += 'dt2 (end date) should be string. \n'
        if not is_number(lat1): msg += 'lat1 (start latitude) should be float or integer. \n'
        if not is_number(lat2): msg += 'lat2 (end latitude) should be float or integer. \n'
        if not is_number(lon1): msg += 'lon1 (start longitude) should be float or integer. \n'
        if not is_number(lon2): msg += 'lon2 (end longitude) should be float or integer. \n'
        if not is_number(depth1): msg += 'depth1 (start depth) should be float or integer. \n'
        if not is_number(depth2): msg += 'depth2 (end depth) should be float or integer. \n'

        if len(msg) > 0:        
            halt(msg)    
        return msg


    def query(self, query, servers=['rainier']):
        """Takes a custom query and returns the results in form of a dataframe."""
        # route = '/dataretrieval/query?'     # JSON format, deprecated
        route = '/api/data/query?'     # CSV format      
        payload = {'query': query, 'servername': random.choice(servers)}
        return self._request(route, method='GET', payload=payload)        


    def stored_proc(self, query, args):
        """Executes a strored-procedure and returns the results in form of a dataframe."""
        # route = '/dataretrieval/sp?'     # JSON format, deprecated
        route = '/api/data/sp?'     # CSV format
        payload = {
        'tableName': args[0],    
        'fields': args[1],
        'dt1': args[2],
        'dt2': args[3],
        'lat1': args[4],
        'lat2': args[5],
        'lon1': args[6],
        'lon2': args[7],
        'depth1': args[8],
        'depth2': args[9],
        'spName': query.split(' ')[1]
        }
        self.validate_sp_args(args[0], args[1], args[2], args[3], args[4], args[5], args[6], args[7], args[8], args[9])
        df = self._request(route, method='GET', payload=payload)   
        return df           


    def get_catalog(self):
        """Returns a dataframe containing full Simons CMAP catalog of variables."""
        return self.query('EXEC uspCatalog')


    def search_catalog(self, keywords):
        """
        Returns a dataframe containing a subset of Simons CMAP catalog of variables. 
        All variables at Simons CMAP catalog are annotated with a collection of semantically related keywords. 
        This method takes the passed keywords and returns all of the variables annotated with similar keywords.
        The passed keywords should be separated by blank space. The search result is not sensitive to the order of keywords and is not case sensitive.
        The passed keywords can provide any 'hint' associated with the target variables. Below are a few examples: 
        
        * the exact variable name (e.g. NO3), or its linguistic term (Nitrate)

        * methodology (model, satellite ...), instrument (CTD, seaflow), or disciplines (physics, biology ...) 

        * the cruise official name (e.g. KOK1606), or unofficial cruise name (Falkor)

        * the name of data producer (e.g Penny Chisholm) or institution name (MIT)

        If you searched for a variable with semantically-related-keywords and did not get the correct results, please let us know. 
        We can update the keywords at any point.
        """
        return self.query("EXEC uspSearchCatalog '%s'" % keywords)


    def datasets(self):
        """Returns a dataframe containing the list of data sets hosted by Simons CMAP database."""
        return self.query("EXEC uspDatasets")


    def head(self, tableName, rows=5):
        """Returns top records of a data set."""
        return self.query("EXEC uspHead '%s', '%d'" % (tableName, rows))


    def columns(self, tableName):
        """Returns the list of data set columns."""
        return self.query("EXEC uspColumns '%s'" % tableName)


    def get_dataset_ID(self, tableName):
        """
        Returns dataset ID.
        """
        df = self.query("SELECT DISTINCT(Dataset_ID) FROM dbo.udfCatalog() WHERE LOWER(Table_Name)=LOWER('%s') " % tableName)
        if len(df) < 1:
            halt('Invalid table name: %s' % tableName)
        if len(df) > 1:
            halt('More than one table found. Please provide a more specific name: ')
            print(df)
        return df.iloc[0]['Dataset_ID']            


    def get_dataset(self, tableName):
        """
        Returns the entire dataset.
        It is not recommended to retrieve datasets with more than 100k rows using this method.
        For large datasets, please use the 'space_time' method and retrieve the data in smaller chunks.
        Note that this method does not return the dataset metadata. 
        Use the 'get_dataset_metadata' method to get the dataset metadata.
        """
        datasetID = self.get_dataset_ID(tableName)
        maxRow = 2000000
        df = self.query("SELECT JSON_stats FROM tblDataset_Stats WHERE Dataset_ID=%d " % datasetID)
        df = pd.read_json(df['JSON_stats'][0])
        rows = int(df.loc[['count'], 'lat'])
        if rows > maxRow:
            msg = "The requested dataset has %d records.\n" % rows 
            msg += "It is not recommended to retrieve datasets with more than %d rows using this method.\n" % maxRow
            msg += "For large datasets, please use the 'space_time' method and retrieve the data in smaller chunks." 
            halt(msg)
        return self.query("SELECT * FROM %s" % tableName)


    def get_dataset_metadata(self, tableName):
        """Returns a dataframe containing the dataset metadata."""
        return self.query("EXEC uspDatasetMetadata  '%s'" % tableName)


    def get_var(self, tableName, varName):
        """
        Returns a single-row dataframe from tblVariables containing info associated with varName.
        This method is mean to be used internally and will not be exposed at documentations.
        """
        query = "SELECT * FROM tblVariables WHERE Table_Name='%s' AND Short_Name='%s'" % (tableName, varName)
        return self.query(query)


    def get_var_catalog(self, tableName, varName):
        """Returns a single-row dataframe from catalog (udfCatalog) containing all of the variable's info at catalog."""
        query = "SELECT * FROM [dbo].udfCatalog() WHERE Table_Name='%s' AND Variable='%s'" % (tableName, varName)
        return self.query(query)

    def get_var_long_name(self, tableName, varName):
        """Returns the long name of a given variable."""
        return self.query("EXEC uspVariableLongName '%s', '%s'" % (tableName, varName)).iloc[0]['Long_Name']


    def get_unit(self, tableName, varName):
        """Returns the unit for a given variable."""
        return ' [' + self.query("EXEC uspVariableUnit '%s', '%s'" % (tableName, varName)).iloc[0]['Unit'] + ']' 


    def get_var_resolution(self, tableName, varName):
        """Returns a single-row dataframe from catalog (udfCatalog) containing the variable's spatial and temporal resolutions."""
        return self.query("EXEC uspVariableResolution '%s', '%s'" % (tableName, varName))


    def get_var_coverage(self, tableName, varName):
        """Returns a single-row dataframe from catalog (udfCatalog) containing the variable's spatial and temporal coverage."""
        return self.query("EXEC uspVariableCoverage '%s', '%s'" % (tableName, varName))


    def get_var_stat(self, tableName, varName):
        """Returns a single-row dataframe from catalog (udfCatalog) containing the variable's summary statistics."""
        return self.query("EXEC uspVariableStat '%s', '%s'" % (tableName, varName))


    def has_field(self, tableName, varName):
        """Returns a boolean confirming whether a field (varName) exists in a table (data set)."""
        query = "SELECT COL_LENGTH('%s', '%s') AS RESULT " % (tableName, varName)
        df = self.query(query)['RESULT']
        hasField = False
        if len(df)>0: hasField = True
        return hasField


    def is_grid(self, tableName, varName):
        """Returns a boolean indicating whether the variable is a gridded product or has irregular spatial resolution."""
        grid = True
        query = "SELECT Spatial_Res_ID, RTRIM(LTRIM(Spatial_Resolution)) AS Spatial_Resolution FROM tblVariables "
        query = query + "JOIN tblSpatial_Resolutions ON [tblVariables].Spatial_Res_ID=[tblSpatial_Resolutions].ID "
        query = query + "WHERE Table_Name='%s' AND Short_Name='%s' " % (tableName, varName)
        df = self.query(query)
        if len(df) < 1:
            return None
        if df.Spatial_Resolution[0].lower().find('irregular') != -1:
            grid = False
        return grid



    def is_climatology(self, tableName):
        """
        Returns True if the table represents a climatological data set.    
        """
        return True if self.query(f"SELECT * FROM tblDatasets d JOIN tblVariables v ON d.ID=v.Dataset_ID WHERE v.Table_Name='{tableName}'").iloc[0]['Climatology'] == 1 else False


    def get_references(self, datasetID):
        """Returns a dataframe containing refrences associated with a data set."""
        query = "SELECT Reference FROM dbo.udfDatasetReferences(%d)" % datasetID
        return self.query(query)

 
    def get_metadata_noref(self, table, variable):
        """
        Returns a dataframe containing the associated metadata for a single variable.
        The returned metadata does not include the list of references and articles associated with the variable.  
        """
        query = "SELECT * FROM dbo.udfCatalog() WHERE Variable='%s' AND Table_Name='%s'"  % (variable, table)
        return self.query(query)
        

    def get_metadata(self, table, variable):
        """
        Returns a dataframe containing the associated metadata.
        The inputs can be string literals (if only one table, and variable is passed) or a list of string literals.
        """
        if isinstance(table, str): table = [table]
        if isinstance(variable, str): variable = [variable]
        metadata = pd.DataFrame({})    
        for i in range(len(table)):    
            df = self.query("EXEC uspVariableMetaData '%s', '%s'" % (table[i], variable[i]))
            metadata = pd.concat([metadata, df], axis=0, sort=False)
        return metadata 


    def cruises(self):
        """
        Returns a dataframe containing a list of all of the hosted cruise names.
        """
        return self.query('EXEC uspCruises')


    def cruise_by_name(self, cruiseName):
        """
        Returns a dataframe containing cruise info using cruise name.
        """
        df = self.query("EXEC uspCruiseByName '%s' " % cruiseName)
        if len(df) < 1:
            halt('Invalid cruise name: %s' % cruiseName)
        if len(df) > 1:
            if 'Keywords' in df.columns: df.drop('Keywords', axis=1, inplace=True)
            print(df)
            halt('More than one cruise found. Please provide a more specific cruise name: ')
        return df


    def cruise_bounds(self, cruiseName):
        """
        Returns a dataframe containing cruise boundaries in space and time.
        """
        df = self.cruise_by_name(cruiseName)
        return self.query('EXEC uspCruiseBounds %d ' % df.iloc[0]['ID'])


    def cruise_trajectory(self, cruiseName):
        """
        Returns a dataframe containing the cruise trajectory.
        """
        df = self.cruise_by_name(cruiseName)
        return self.query('EXEC uspCruiseTrajectory %d ' % df.iloc[0]['ID'])


    def cruise_variables(self, cruiseName):
        """
        Returns a dataframe containing all registered variables (at Simons CMAP) during a cruise.
        """
        df = self.cruise_by_name(cruiseName)
        return self.query('SELECT * FROM dbo.udfCruiseVariables(%d) ' % df.iloc[0]['ID'])


    def subset(self, spName, table, variable, dt1, dt2, lat1, lat2, lon1, lon2, depth1, depth2):     
        """Returns a subset of data according to space-time constraints."""
        query = 'EXEC {} ?, ?, ?, ?, ?, ?, ?, ?, ?, ?'.format(spName)
        args = [table, variable, dt1, dt2, lat1, lat2, lon1, lon2, depth1, depth2]
        return self.stored_proc(query, args)  


    def space_time(self, table, variable, dt1, dt2, lat1, lat2, lon1, lon2, depth1, depth2):     
        """
        Returns a subset of data according to space-time constraints.
        The results are ordered by time, lat, lon, and depth (if exists).
        """
        return self.subset('uspSpaceTime', table, variable, dt1, dt2, lat1, lat2, lon1, lon2, depth1, depth2)


    @staticmethod
    def _interval_to_uspName(interval):
        if interval is None or interval == '':
            return 'uspTimeSeries'
        interval = interval.lower().strip()
        if interval in ['w', 'week', 'weekly']:
            usp = 'uspWeekly'
        elif interval in ['m', 'month', 'monthly']:
            usp = 'uspMonthly'
        elif interval in ['q', 's', 'season', 'seasonal', 'seasonality', 'quarterly']:
            usp = 'uspQuarterly'
        elif interval in ['y', 'a', 'year', 'yearly', 'annual']:
            usp = 'uspAnnual'
        else:
            halt('Invalid interval: %s' % interval)
        return usp


    def time_series(self, table, variable, dt1, dt2, lat1, lat2, lon1, lon2, depth1, depth2, interval=None):     
        """
        Returns a subset of data according to space-time constraints.
        The results are aggregated by time and ordered by time, lat, lon, and depth (if exists).
        The timeseries data can be binned weekyly, monthly, qurterly, or annualy, if interval variable is set (this feature is not applicable to climatological data sets). 
        """
        usp = self._interval_to_uspName(interval)
        if usp != 'uspTimeSeries' and self.is_climatology(table):
            print_tqdm(
                'Custom binning (monthly, weekly, ...) is not suppoerted for climatological data sets. Table %s represents a climatological data set.' % table, 
                err=True)
            return pd.DataFrame({})
        return self.subset(usp, table, variable, dt1, dt2, lat1, lat2, lon1, lon2, depth1, depth2)


    def depth_profile(self, table, variable, dt1, dt2, lat1, lat2, lon1, lon2, depth1, depth2):     
        """
        Returns a subset of data according to space-time constraints.
        The results are aggregated by depth and ordered by depth.
        """
        return self.subset('uspDepthProfile', table, variable, dt1, dt2, lat1, lat2, lon1, lon2, depth1, depth2)


    def section(self, table, variable, dt1, dt2, lat1, lat2, lon1, lon2, depth1, depth2):     
        """
        Returns a subset of data according to space-time constraints.
        The results are ordered by time, lat, lon, and depth.
        """
        return self.subset('uspSectionMap', table, variable, dt1, dt2, lat1, lat2, lon1, lon2, depth1, depth2)


    @staticmethod
    def _climatology_period(period):
        period = period.lower().strip()
        if period in ['d', 'day', 'dayofyear']:
            climPeriod = 'dayofyear'
        elif period in ['w', 'week', 'weekly']:
            climPeriod = 'week'
        elif period in ['m', 'month', 'monthly']:
            climPeriod = 'month'
        elif period in ['y', 'a', 'year', 'yearly', 'annual']:
            climPeriod = 'year'
        else:
            halt('Invalid climatology period: %s' % period)
        return climPeriod


    def climatology(self, table, variable, period, periodVal, lat1, lat2, lon1, lon2, depth1, depth2):     
        """
        Computes the climatology of a gridded dataset over a spatial domain delimited by (lat1, lat2, lon1, lon2, depth1, depth2). 
        Note this method does not apply to sparse datasets. 
        The parameter `period` specifies the climatology interval (e.g weekly, monthly...) and `periodVal` sets the interval value. 
        For example, to compute the climatology of a variable for the month of October, `period` is set to 'month' and `periodVal` is set to 10. 
        Please avoid using periods that are finner than the temporal resolution of the underlying dataset. 
        For instance, if the dataset is a weekly-averaged product, do not set the `period` to 'dayofyear'.
        The output of this method is a Pandas DataFrame ordered by time, lat, lon, and depth (if exists), respectively.
        """
        period = self._climatology_period(period)
        if self.is_climatology(table):
            print_tqdm(
                'Table %s already contains a climatological dataset.' % table, 
                err=True)
            return pd.DataFrame({})

        if not self.is_grid(table, variable):
            print_tqdm(
                'This method only applies to the uniformly gridded datasets. Table %s represents an irregular dataset.' % table, 
                err=True)
            return pd.DataFrame({})

        if not self.has_field(table, period):
            print_tqdm(
                'Climatology computation is not supported by %s.\nPlease let us know if you think we should enable climatology calculations for this dataset.' % table, 
                err=True)
            return pd.DataFrame({})
                    
        return self.query("uspAggregate '%s', '%s', '%s', %d, %f, %f, %f, %f, %f, %f" % (table, variable, period, periodVal, lat1, lat2, lon1, lon2, depth1, depth2) )


    def match(self, sourceTable, sourceVar, targetTables, targetVars, 
             dt1, dt2, lat1, lat2, lon1, lon2, depth1, depth2, 
             temporalTolerance, latTolerance, lonTolerance, depthTolerance):     
        """
        Colocalizes the source variable (from source table) with the target variable (from target table).
        The tolerance parameters set the matching boundaries between the source and target data sets. 
        Returns a dataframe containing the source variable joined with the target variable.
        """
        from .match import Match 
        return Match('uspMatch', sourceTable, sourceVar, targetTables, targetVars,
                     dt1, dt2, lat1, lat2, lon1, lon2, depth1, depth2,
                     temporalTolerance, latTolerance, lonTolerance, depthTolerance).compile()



    def along_track(self, cruise, targetTables, targetVars, depth1, depth2, temporalTolerance, latTolerance, lonTolerance, depthTolerance):     
        """
        Takes a cruise name and colocalizes the cruise track with the specified variable(s).
        """
        df = self.cruise_bounds(cruise)
        return self.match(
                         sourceTable='tblCruise_Trajectory',
                         sourceVar=str(df.iloc[0]['ID']),
                         targetTables=targetTables,
                         targetVars=targetVars,
                         dt1=df.iloc[0]['dt1'],
                         dt2=df.iloc[0]['dt2'],
                         lat1=df.iloc[0]['lat1'],
                         lat2=df.iloc[0]['lat2'],
                         lon1=df.iloc[0]['lon1'],
                         lon2=df.iloc[0]['lon2'],
                         depth1=depth1,
                         depth2=depth2,
                         temporalTolerance=temporalTolerance,
                         latTolerance=latTolerance,
                         lonTolerance=lonTolerance,
                         depthTolerance=depthTolerance
                         )


