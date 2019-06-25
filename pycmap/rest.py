"""
Author: Mohammad Dehghani Ashkezari <mdehghan@uw.edu>

Date: 2019-06-22

Function: Encapsulates RESTful API logic.
"""


import sys
import requests
from requests.exceptions import HTTPError
import orjson
from urllib.parse import urlencode
import pandas as pd
from .common import (
    halt,
    get_base_url,
    get_token,
    save_config
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
                 base_url=None,
                 headers=None,
                 vizEngine='bokeh'):
        """
        :param str token: access token to make client requests.
        :param str base_url: root endpoint of Simons CMAP API.
        :param dict headers: Additional headers to add to requests.
        """

        self._token = token or get_token()
        self._base_url = base_url or get_base_url()
        self._headers = headers
        self._token_prefix = 'Api-Key '
        self._vizEngine = vizEngine

        save_config(token=self._token, vizEngine=self._vizEngine)

        assert len(self._token) > 0, \
            'API key cannot be empty.'
        assert self._headers is None or isinstance(self._headers, dict), \
            'Expected dict, got %r' % self._headers


    def _request(
        self,
        route,
        method='GET',
        payload=None,
        base_url=None
    ):
        base_url = base_url or self._base_url
        headers = {'Authorization': self._token_prefix + self._token}
        if method.upper().strip() == 'GET':
            return self._atomic_get(route, headers, payload)
        else:
            return None

    def _atomic_get(self, route, headers, payload):
        '''
        Submits a single GET request. Returns the body in form of pandas dataframe if 200 status.
        '''
        
        df = None
        try:
            url_safe_query = ''
            if payload is not None:
                url_safe_query = urlencode(payload)
            url = self._base_url + route + url_safe_query
            resp = requests.get(url, headers=headers)  
            if resp.text.lower().strip() == 'unauthorized':
                halt('Unauthorized API key!')
            if resp.text != '':
                json_list = [orjson.loads(line) for line in resp.text.splitlines()]
                df = pd.DataFrame(json_list)
        except HTTPError as http_error:
            # look for resp.status_code
            raise
        return df

    @staticmethod
    def time_first(df):
        def swap_first_col(df, col, cols):            
            if col in cols:
                oldIndex = cols.index(col)
                firstCol = cols[0]
                cols[0] = col
                cols[oldIndex] = firstCol
                df = df[cols]
            return df    
        cols = list(df.columns)
        df = swap_first_col(df, 'year', cols)
        df = swap_first_col(df, 'month', cols)
        df = swap_first_col(df, 'time', cols)
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

        valid = True
        msg = ''
        if not isinstance(table, str):
            msg += 'table name should be string. \n'
        if not isinstance(variable, str):
            msg += 'variable name should be string. \n'
        if not isinstance(dt1, str):
            msg += 'dt1 (start date) should be string. \n'
        if not isinstance(dt2, str):
            msg += 'dt2 (end date) should be string. \n'
        if not isinstance(lat1, float) and not isinstance(lat1, int):
            msg += 'lat1 (start latitude) should be float or integer. \n'
        if not isinstance(lat2, float) and not isinstance(lat2, int):
            msg += 'lat2 (end latitude) should be float or integer. \n'
        if not isinstance(lon1, float) and not isinstance(lon1, int):
            msg += 'lon1 (start longitude) should be float or integer. \n'
        if not isinstance(lon2, float) and not isinstance(lon2, int):
            msg += 'lon2 (end longitude) should be float or integer. \n'
        if not isinstance(depth1, float) and not isinstance(depth1, int):
            msg += 'depth1 (start depth) should be float or integer. \n'
        if not isinstance(depth2, float) and not isinstance(depth2, int):
            msg += 'lat2 (end depth) should be float or integer. \n'

        if len(msg) > 0:        
            halt(msg)    
        return msg

    def query(self, query):
        route = '/dataretrieval/query?'
        payload = {'query': query}
        return self._request(route, method='GET', payload=payload)        

    def stored_proc(self, query, args):
        route = '/dataretrieval/sp?'
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
        return self.time_first(df)           

    def get_catalog(self):
        return self.query('SELECT * FROM dbo.udfCatalog()')

    def get_var(self, tableName, varName):
        query = "SELECT * FROM tblVariables WHERE Table_Name='%s' AND Short_Name='%s'" % (tableName, varName)
        return self.query(query)

    def has_field(self, tableName, varName):
        query = "SELECT COL_LENGTH('%s', '%s') AS RESULT " % (tableName, varName)
        return False if self.query(query)['RESULT'][0] == None else True




    def subset(self, spName, table, variable, dt1, dt2, lat1, lat2, lon1, lon2, depth1, depth2):     
        query = 'EXEC {} ?, ?, ?, ?, ?, ?, ?, ?, ?, ?'.format(spName)
        args = [table, variable, dt1, dt2, lat1, lat2, lon1, lon2, depth1, depth2]
        return self.stored_proc(query, args)  

    def space_time(self, table, variable, dt1, dt2, lat1, lat2, lon1, lon2, depth1, depth2):     
        return self.subset('uspSpaceTime', table, variable, dt1, dt2, lat1, lat2, lon1, lon2, depth1, depth2)

    def time_series(self, table, variable, dt1, dt2, lat1, lat2, lon1, lon2, depth1, depth2):     
        return self.subset('uspTimeSeries', table, variable, dt1, dt2, lat1, lat2, lon1, lon2, depth1, depth2)

    def depth_profile(self, table, variable, dt1, dt2, lat1, lat2, lon1, lon2, depth1, depth2):     
        return self.subset('uspDepthProfile', table, variable, dt1, dt2, lat1, lat2, lon1, lon2, depth1, depth2)

    def section(self, table, variable, dt1, dt2, lat1, lat2, lon1, lon2, depth1, depth2):     
        return self.subset('uspSectionMap', table, variable, dt1, dt2, lat1, lat2, lon1, lon2, depth1, depth2)
