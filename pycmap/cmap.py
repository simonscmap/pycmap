
"""
Author: Mohammad Dehghani Ashkezari <mdehghan@uw.edu>

Date: 2019-06-22

Function: Top-level API client entry class.
"""


from .rest import _REST


class API(_REST):
    """
    Use this class to make requests to the Simons CMAP API using a user's access
    token (api_key). This class inherits from base API implementation(s).
    """
    pass

