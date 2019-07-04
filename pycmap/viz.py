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
from .section import Section
from .export import Export
from .foliumHeat import folium_map
from tqdm import tqdm 
import numpy as np
if inline(): from tqdm import tqdm_notebook as tqdm



def no_data_reaction(itnum, table, variable, dt1, dt2, lat1, lat2, lon1, lon2, depth1, depth2):
    """Behavior when no data is retrieved."""
    print_tqdm(
                """%d: No data found: 
                Table: %s, 
                Variable: %s,
                Time span: (%s, %s),
                Latitude span: (%2.2f, %2.2f), 
                Longitude span: (%2.2f, %2.2f),
                Depth span: (%2.2f, %2.2f)
                """ % 
                (itnum, table, variable, dt1, dt2, lat1, lat2, lon1, lon2, depth1, depth2), 
                err=True 
                )
    return    


def plot_hist(tables, variables, dt1, dt2, lat1, lat2, lon1, lon2, depth1, depth2, exportDataFlag=False, show=True):
    """
    Create histogram graph for each variable within a predefined space-time domain. 
    Returns the generated graph objects in form of a python list. 
    """   
    gos = []
    for i in tqdm(range(len(tables)), desc='overall'):
        data = API().space_time(tables[i], variables[i], dt1, dt2, lat1, lat2, lon1, lon2, depth1, depth2)
        if len(data) < 1:
            no_data_reaction(i+1, tables[i], variables[i], dt1, dt2, lat1, lat2, lon1, lon2, depth1, depth2)
            continue
        print_tqdm('%d: %s retrieved (%s).' % (i+1, variables[i], tables[i]), err=False)

        if exportDataFlag:
            metadata = API().get_metadata(tables[i], variables[i])
            fname = make_filename_by_table_var(tables[i], variables[i], prefix='Hist')
            Export(data, metadata, fname).save()

        go = Hist(data, variables[i]).graph_obj()        
        go.unit = API().get_unit(tables[i], variables[i])
        go.xlabel = variables[i] + go.unit
        go.ylabel = ''
        go.legend = variables[i]
        if show: go.render()
        gos.append(go)
    return gos



def plot_map(tables, variables, dt1, dt2, lat1, lat2, lon1, lon2, depth1, depth2, exportDataFlag=False, show=True, levels=0):
    """
    Create individual map graphs per each depth level using gridded data. 
    In the case of sparse data set, data is superimposed on a geospatial map.
    Returns the generated graph objects in form of a python list. 
    """   
    gos = []
    for i in tqdm(range(len(tables)), desc='overall'):
        data = API().space_time(tables[i], variables[i], dt1, dt2, lat1, lat2, lon1, lon2, depth1, depth2)
        if len(data) < 1:
            no_data_reaction(i+1, tables[i], variables[i], dt1, dt2, lat1, lat2, lon1, lon2, depth1, depth2)
            continue
        print_tqdm('%d: %s retrieved (%s).' % (i+1, variables[i], tables[i]), err=False)

        if exportDataFlag:
            metadata = API().get_metadata(tables[i], variables[i])
            fname = make_filename_by_table_var(tables[i], variables[i], prefix='Map')
            Export(data, metadata, fname).save()

        if API().is_grid(tables[i], variables[i]):
            go = Map(data, variables[i], levels).graph_obj()  
            go.unit = API().get_unit(tables[i], variables[i])       
            go.xlabel = 'Longitude'
            go.ylabel = 'Latitude'
            go.width, go.height = canvas_rect(
                                            dw=np.max(data.lon)-np.min(data.lon), 
                                            dh=np.max(data.lat)-np.min(data.lat)
                                            )
            if show: go.render()
            gos.append(go)
        else:
            folium_map(data, tables[i], variables[i], API().get_unit(tables[i], variables[i]) )
                
    return gos



def plot_section(tables, variables, dt1, dt2, lat1, lat2, lon1, lon2, depth1, depth2, exportDataFlag=False, show=True, levels=0):
    """
    Create section maps using gridded data. Does not apply to sparse data sets. 
    If the selected longitude range is larger than latitude range, a zonal section map is generated, 
    otherwise meridional section maps are created.
    Returns the generated graph objects in form of a python list. 
    """   
    gos = []
    for i in tqdm(range(len(tables)), desc='overall'):
        if not API().is_grid(tables[i], variables[i]):
            print_tqdm('%d: Table %s represents a sparse data set which is not supported for section map.' % (i+1, tables[i]), err=True)
            continue

        if not API().has_field(tables[i], 'depth'):
            print_tqdm('%d: Table %s does not have "depth" field.' % (i+1, tables[i]), err=True)
            continue

        data = API().section(tables[i], variables[i], dt1, dt2, lat1, lat2, lon1, lon2, depth1, depth2)
        if len(data) < 1:
            no_data_reaction(i+1, tables[i], variables[i], dt1, dt2, lat1, lat2, lon1, lon2, depth1, depth2)
            continue
        print_tqdm('%d: %s retrieved (%s).' % (i+1, variables[i], tables[i]), err=False)

        if exportDataFlag:
            metadata = API().get_metadata(tables[i], variables[i])
            fname = make_filename_by_table_var(tables[i], variables[i], prefix='Section')
            Export(data, metadata, fname).save()

        go = Section(data, variables[i], levels).graph_obj()  
        go.unit = API().get_unit(tables[i], variables[i])       
        go.ylabel = 'depth [m]'
        go.width, go.height = 1000, 500
        if show: go.render()
        gos.append(go)
                
    return gos
