"""
Author: Mohammad Dehghani Ashkezari <mdehghan@uw.edu>

Date: 2019-06-23

Function: Data model to query subset of data.
"""


from .common import (
    halt
)


class W3(object):
    """
    Used this class to configure query parameters. The pattern is as follow:
    What: tables/variables
    When: temporal range
    Where: spatial range
    """

    def __init__(self,
                 table=None,
                 variable=None,
                 dt1=None,
                 dt2=None,
                 lat1=None,
                 lat2=None,
                 lon1=None,
                 lon2=None,
                 depth1=None,
                 depth2=None,    
                **kwargs
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

        self.table = table
        self.variable = variable
        self.dt1 = dt1
        self.dt2 = dt2
        self.lat1 = lat1
        self.lat2 = lat2
        self.lon1 = lon1
        self.lon2 = lon2
        self.depth1 = depth1
        self.depth2 = depth2

        valid, msg = self.validate()
        if not valid:
            halt(msg)


    def __repr__(self):
        return """
        W3(
        table={!r}, 
        variable={!r}, 
        dt1={!r}, 
        dt2={!r}, 
        lat1={!r}, 
        lat2={!r}, 
        lon1={!r}, 
        lon2={!r}, 
        depth1={!r}, 
        depth2={!r}
        )
        """.format(
                    self.table, 
                    self.variable, 
                    self.dt1, 
                    self.dt2, 
                    self.lat1, 
                    self.lat2, 
                    self.lon1, 
                    self.lon2, 
                    self.depth1, 
                    self.depth2
                    )


    def validate(self):
        valid = True
        msg = ''
        if not isinstance(self.table, str):
            msg += 'table name should be string. \n'
        if not isinstance(self.variable, str):
            msg += 'variable name should be string. \n'
        if not isinstance(self.dt1, str):
            msg += 'dt1 (start date) should be string. \n'
        if not isinstance(self.dt2, str):
            msg += 'dt2 (end date) should be string. \n'
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
            valid = False    
        return valid, msg
