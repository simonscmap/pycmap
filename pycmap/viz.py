"""
Author: Mohammad Dehghani Ashkezari <mdehghan@uw.edu>

Date: 2019-06-28

Function: Implements the top-level visualization logic.
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
from .trend import Trend
from .annotatedHeatmap import AnnotatedHeatmap
from .export import Export
from .foliumHeat import folium_map, folium_cruise_track
import numpy as np
import pandas as pd
from tqdm import tqdm 
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



def plot_map(tables, variables, dt1, dt2, lat1, lat2, lon1, lon2, depth1, depth2, exportDataFlag=False, show=True, levels=0, surface3D=False):
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
            go = Map(data, variables[i], levels, surface3D).graph_obj()  
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




def plot_timeseries(tables, variables, dt1, dt2, lat1, lat2, lon1, lon2, depth1, depth2, exportDataFlag=False, show=True, interval=None):
    """
    Create timeseries graph for each variable within a predefined space-time domain. 
    Returns the generated graph objects in form of a python list. 
    """   
    gos = []
    for i in tqdm(range(len(tables)), desc='overall'):
        if API().is_climatology(tables[i]):
            data = API().time_series(tables[i], variables[i], dt1, dt2, lat1, lat2, lon1, lon2, depth1, depth2, interval=None)
        else:    
            data = API().time_series(tables[i], variables[i], dt1, dt2, lat1, lat2, lon1, lon2, depth1, depth2, interval=interval)
        if len(data) < 1:
            no_data_reaction(i+1, tables[i], variables[i], dt1, dt2, lat1, lat2, lon1, lon2, depth1, depth2)
            continue
        print_tqdm('%d: %s retrieved (%s).' % (i+1, variables[i], tables[i]), err=False)

        if exportDataFlag:
            metadata = API().get_metadata(tables[i], variables[i])
            fname = make_filename_by_table_var(tables[i], variables[i], prefix='TimeSeries')
            df = data.copy()
            df['lat1'] = lat1
            df['lat2'] = lat2
            df['lon1'] = lon1
            df['lon2'] = lon2
            if API().has_field(tables[i], 'depth'):
                df['depth1'] = depth1
                df['depth2'] = depth2
            Export(df, metadata, fname).save()

        go = Trend(data, variables[i]).graph_obj()
        go.unit = API().get_unit(tables[i], variables[i]) 
        go.y = data[variables[i]]  
        go.yErr = data[variables[i]+'_std']  

        if API()._interval_to_uspName(interval) == 'uspTimeSeries':    
            go.x = pd.to_datetime(data[data.columns[0]])
        elif API()._interval_to_uspName(interval) == 'uspAnnual':    
            go.x = data['year']
        elif API()._interval_to_uspName(interval) == 'uspQuarterly':    
            go.x = data['year'].astype(str) + '-quarter ' + data['quarter'].astype(str)
        elif API()._interval_to_uspName(interval) == 'uspMonthly':    
            go.x = data['year'].astype(str) + '-' + data['month'].astype(str)
        elif API()._interval_to_uspName(interval) == 'uspWeekly':    
            go.x = data['year'].astype(str) + '-week ' + data['week'].astype(str)

        if API().is_climatology(tables[i]):
            go.timeSeries = False
            go.x = data[data.columns[0]]
            if 'month' in data.columns:
                go.xlabel = 'Month' 
        go.ylabel = variables[i] + go.unit
        go.legend = variables[i]
        if show: go.render()
        gos.append(go)
    return gos


def plot_depth_profile(tables, variables, dt1, dt2, lat1, lat2, lon1, lon2, depth1, depth2, exportDataFlag=False, show=True):
    """
    Create depth profile graph for each variable within a predefined space-time domain. 
    Returns the generated graph objects in form of a python list. 
    """   
    gos = []
    for i in tqdm(range(len(tables)), desc='overall'):
        if not API().has_field(tables[i], 'depth'):
            print_tqdm('%d: Table %s does not have depth field.' % (i+1, tables[i]), err=True)
            continue
        data = API().depth_profile(tables[i], variables[i], dt1, dt2, lat1, lat2, lon1, lon2, depth1, depth2)
        if len(data) < 1:
            no_data_reaction(i+1, tables[i], variables[i], dt1, dt2, lat1, lat2, lon1, lon2, depth1, depth2)
            continue
        print_tqdm('%d: %s retrieved (%s).' % (i+1, variables[i], tables[i]), err=False)

        if exportDataFlag:
            metadata = API().get_metadata(tables[i], variables[i])
            fname = make_filename_by_table_var(tables[i], variables[i], prefix='DepthProfile')
            df = data.copy()
            df['time1'] = dt1
            df['time2'] = dt2
            df['lat1'] = lat1
            df['lat2'] = lat2
            df['lon1'] = lon1
            df['lon2'] = lon2
            Export(df, metadata, fname).save()

        go = Trend(data, variables[i]).graph_obj()
        go.unit = API().get_unit(tables[i], variables[i]) 
        go.x = data['depth']
        go.y = data[variables[i]]  
        go.yErr = data[variables[i]+'_std']  
        go.timeSeries = False
        go.xlabel = 'Depth [m]'
        go.ylabel = variables[i] + go.unit
        go.legend = variables[i]
        if show: go.render()
        gos.append(go)
    return gos



def plot_corr_map(
                 sourceTable, sourceVar, targetTables, targetVars, 
                 dt1, dt2, lat1, lat2, lon1, lon2, depth1, depth2, 
                 temporalTolerance, latTolerance, lonTolerance, depthTolerance, 
                 method='spearman', exportDataFlag=False, show=True
                 ):
    """
    Creates an annotated hestmap illustrating the degree of correlation between each pair of the variables within the resulting matched dataframe.
    Returns the generated heatmap objects.
    """   

    data = API().match(
                      sourceTable, sourceVar, targetTables, targetVars, 
                      dt1, dt2, lat1, lat2, lon1, lon2, depth1, depth2, 
                      temporalTolerance, latTolerance, lonTolerance, depthTolerance
                      )
    if len(data) < 1:
        print_tqdm('No matching results returned!', err=True)
        return
    data_org = data.copy()
    # remove time and standard deviation columns
    if 'time' in data.columns: data.drop('time', axis=1, inplace=True)
    for col in data.columns:
        if col[-4:] == '_std': data.drop(col, axis=1, inplace=True)   
    corr = data.corr(method=method)
    corr = corr.dropna(axis=0, how='all')   
    corr = corr.dropna(axis=1, how='all')      

    if exportDataFlag:
        metadata = API().get_metadata([sourceTable] + targetTables , [sourceVar] + targetVars)
        fname_corr = make_filename_by_table_var(sourceTable, sourceVar, prefix='Annotated_Heatmap')
        fname_matched = make_filename_by_table_var(sourceTable, sourceVar, prefix='matched')
        Export(data_org, metadata, fname_matched).save()
        Export(corr, metadata, fname_corr).save()

    go = AnnotatedHeatmap().graph_obj()        
    go.x = list(corr.columns)
    go.y = list(corr.columns)
    go.z = corr.values
    go.cmap = 'coolwarm' 
    go.vmin = -1
    go.vmax = 1
    go.variable = sourceVar
    # go.title = 'Correlation Matrix'
    go.xlabel = ''
    go.ylabel = ''
    go.width = 700
    go.height = 700
    if show: go.render()
    return go







def plot_cruise_corr_map(
                 cruise, targetTables, targetVars,
                 depth1, depth2, 
                 temporalTolerance, latTolerance, lonTolerance, depthTolerance, 
                 method='spearman', exportDataFlag=False, show=True
                 ):
    """
    Creates an annotated hestmap illustrating the degree of correlation between each pair of the variables colocalized with the cruise track.
    Returns the generated heatmap objects.
    """   

    data = API().along_track(
                            cruise, 
                            targetTables, 
                            targetVars, 
                            depth1,
                            depth2,
                            temporalTolerance, 
                            latTolerance, 
                            lonTolerance, 
                            depthTolerance
                      )
    if len(data) < 1:
        print_tqdm('No matching results returned!', err=True)
        return
    data_org = data.copy()
    # remove time and standard deviation columns
    if 'time' in data.columns: data.drop('time', axis=1, inplace=True)
    for col in data.columns:
        if col[-4:] == '_std': data.drop(col, axis=1, inplace=True)   
    corr = data.corr(method=method)
    corr = corr.dropna(axis=0, how='all')   
    corr = corr.dropna(axis=1, how='all')      

    if exportDataFlag:
        metadata = API().get_metadata(targetTables , targetVars)
        fname_corr = make_filename_by_table_var(cruise, '', prefix='Annotated_Heatmap')
        fname_matched = make_filename_by_table_var(cruise, '', prefix='matched')
        Export(data_org, metadata, fname_matched).save()
        Export(corr, metadata, fname_corr).save()

    go = AnnotatedHeatmap().graph_obj()        
    go.x = list(corr.columns)
    go.y = list(corr.columns)
    go.z = corr.values
    go.cmap = 'coolwarm' 
    go.vmin = -1
    go.vmax = 1
    go.variable = 'Along Track ' + cruise
    # go.title = 'Correlation Matrix: ' + cruise
    go.xlabel = ''
    go.ylabel = ''
    go.width = 700
    go.height = 700
    if show: go.render()
    return go



def plot_xy(
            xTables, xVars, yTables, yVars, 
            dt1, dt2, lat1, lat2, lon1, lon2, depth1, depth2, 
            temporalTolerances, latTolerances, lonTolerances, depthTolerances, 
            method='spearman', exportDataFlag=False, show=True
            ):
    """
    Plots one variable against the other.
    Returns the generated graph objects.
    """   

    # TO DO: add input validation here

    gos = []
    for i in tqdm(range(len(xTables)), desc='overall'):
        data = API().match(
                        xTables[i], xVars[i], yTables[i], yVars[i], 
                        dt1, dt2, lat1, lat2, lon1, lon2, depth1, depth2, 
                        temporalTolerances[i], latTolerances[i], lonTolerances[i], depthTolerances[i]
                        )
        if len(data) < 1:
            print_tqdm('No matching results for %s and %s was returend.' % (xVars[i], yVars[i]) , err=True)
            continue
        print_tqdm('%s and %s retrieved .' % (xVars[i], yVars[i]), err=False)

        if exportDataFlag:
            metadata = API().get_metadata([xTables[i]] + [yTables[i]], [xVars[i]] + [yVars[i]])
            fname = make_filename_by_table_var(xVars[i], yVars[i], prefix='XY')
            Export(data, metadata, fname).save()

        go = Trend(data, yVars[i]).graph_obj()
        go.line = False
        go.timeSeries = False
        go.x = data[xVars[i]]  
        go.xErr = data[xVars[i]+'_std']  
        go.y = data[yVars[i]]  
        go.yErr = data[yVars[i]+'_std']  

        go.xlabel = xVars[i] + API().get_unit(xTables[i], xVars[i]) 
        go.ylabel = yVars[i] + API().get_unit(yTables[i], yVars[i]) 
        go.legend = xVars[i] + ' / ' + yVars[i]
        if show: go.render()
        gos.append(go)    
    return gos



def plot_cruise_track(cruise, stations=None):
    """Plots cruise track on folium map."""
    if isinstance(cruise, str): cruise = [cruise]
    df = pd.DataFrame({})
    for cru in cruise:
        track = API().cruise_trajectory(cru)
        track['cruise'] = cru
        print_tqdm('%s cruise track retrieved.' % cru, err=False)
        df = df.append(track, ignore_index=True)
    folium_cruise_track(df, stations)
    return