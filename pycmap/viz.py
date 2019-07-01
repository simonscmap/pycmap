"""
Author: Mohammad Dehghani Ashkezari <mdehghan@uw.edu>

Date: 2019-06-28

Function: Implements the top-level visualization logics.
"""

from .cmap import API  # noqa
from .common import (
                     get_vizEngine,
                     print_tqdm,
                     inline,
                     make_filename_by_table_var,
                     canvas_rect
                    )

from .hist import Hist
from .map import Map
from .export import Export
from tqdm import tqdm 
import numpy as np
if inline(): from tqdm import tqdm_notebook as tqdm




def plot_hist(tables, variables, dt1, dt2, lat1, lat2, lon1, lon2, depth1, depth2, exportDataFlag=False):
    """
    Create histogram graph for each variable.
    Returns the generated graph objects in form of a python list. 
    """   
    gos = []
    for i in tqdm(range(len(tables)), desc='overall'):
        data = API().space_time(tables[i], variables[i], dt1, dt2, lat1, lat2, lon1, lon2, depth1, depth2)
        if len(data) < 1:
            print_tqdm('%d: No matching entry found: Table: %s, Variable: %s ' % (i+1, tables[i], variables[i]), err=True )
            continue
        print_tqdm('%d: %s retrieved (%s).' % (i+1, variables[i], tables[i]), err=False)
        go = Hist(data, variables[i]).graph_obj()        
        go.unit = API().get_unit(tables[i], variables[i])
        go.xlabel = variables[i] + go.unit
        go.ylabel = ''
        go.legend = variables[i]
        go.render()
        gos.append(go)
        if exportDataFlag:
            metadata = API().get_metadata(tables[i], variables[i])
            fname = make_filename_by_table_var(tables[i], variables[i], prefix='Hist')
            Export(data, metadata, fname).save()
    return gos






def plot_map(tables, variables, dt1, dt2, lat1, lat2, lon1, lon2, depth1, depth2, exportDataFlag=False):
    """
    Creates map graph for each variable.
    Returns the generated graph objects in form of a python list. 
    """   
    gos = []
    for i in tqdm(range(len(tables)), desc='overall'):
        data = API().space_time(tables[i], variables[i], dt1, dt2, lat1, lat2, lon1, lon2, depth1, depth2)
        if len(data) < 1:
            print_tqdm('%d: No matching entry found: Table: %s, Variable: %s ' % (i+1, tables[i], variables[i]), err=True )
            continue
        print_tqdm('%d: %s retrieved (%s).' % (i+1, variables[i], tables[i]), err=False)
        go = Map(data, variables[i]).graph_obj()  
        go.unit = API().get_unit(tables[i], variables[i])       
        go.xlabel = 'Longitude'
        go.ylabel = 'Latitude'
        go.width, go.height = canvas_rect(
                                         dw=np.max(data.lon)-np.min(data.lon), 
                                         dh=np.max(data.lat)-np.min(data.lat)
                                         )
        go.render()
        gos.append(go)
        if exportDataFlag:
            metadata = API().get_metadata(tables[i], variables[i])
            fname = make_filename_by_table_var(tables[i], variables[i], prefix='Map')
            Export(data, metadata, fname).save()
    return gos
