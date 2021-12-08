"""
Author: Mohammad Dehghani Ashkezari <mdehghan@uw.edu>

Date: 2021-11-24

Function: Sample (Colocalize) a custom dataframe given list of target variables.
"""

from .cmap import API 
from .common import (halt, MAX_SAMPLE_SOURCE)
import datetime
import concurrent.futures
import pandas as pd
from dateutil.parser import parse



def alias(varName, tableName):
    """Return an alias for a variable name."""
    return f"__CMAP__{varName}__{tableName}"


def add_target_columns(df, targets):
    """
    Adds new columns (empty) to the dataframe form each target variable.
    """
    for env in targets.values():
        for v in env.get("aliases"):
            if v not in df.columns: df[v] = None
    return df
    

def add_target_meta(api, targets):
    """
    Adds new entries (metadata) to the `targets` dictionary including the 
    temporal coverage of each environmental dataset, if it has depth field, 
    and if it's a climatology dataset.
    """
    for table, env in targets.items():
        df = api.query(f"SELECT MIN([time]) startTime, MAX([time]) endTime FROM {table}")
        if len(df) > 0:
            targets[table]["startTime"] = df.loc[0, "startTime"]
            targets[table]["endTime"] = df.loc[0, "endTime"]
        targets[table]["hasDepth"] = api.has_field(table, "depth")
        targets[table]["isClimatology"] = api.is_climatology(table)
        targets[table]["aliases"] = []
        for varName in targets[table]["variables"]:
            targets[table]["aliases"].append(alias(varName, table))
    return targets


def match(df, api, targets, rowIndex, totalRows):
    """
    Takes a single-row of the source dataframe and colocalizes with the 
    target variables specified by `targets`. The tolerance parametrs 
    are also included in `targets`.
    No match is made between a surface target dataset (such as satellite) and observations deeper than `MAX_SURFACE_DEPTH`.
    """ 
    def get_month(dt):
        return parse(dt).month

    def shift_dt(dt, delta):
        delta = float(delta)
        dt = parse(dt)
        dt += datetime.timedelta(days=delta)
        return dt.strftime("%Y-%m-%d %H:%M:%S")

    def in_time_window(sourceDT, targetMinDT, targetMaxDT):
        targetMinDT = targetMinDT.split(".000Z")[0]
        targetMaxDT = targetMaxDT.split(".000Z")[0]
        return not (
                    parse(sourceDT) < parse(targetMinDT) or 
                    parse(sourceDT) > parse(targetMaxDT)
                    )

    def construc_query(table, env, t, lat, lon, depth):
        variables = env["variables"] 
        aliases = env["aliases"] 
        timeTolerance = env["tolerances"][0] 
        latTolerance = env["tolerances"][1] 
        lonTolerance = env["tolerances"][2]  
        depthTolerance = env["tolerances"][3]  
        hasDepth = env["hasDepth"] 
        isClimatology = env["isClimatology"]
        inTimeRange = True
        if not isClimatology:
            startTime = env["startTime"]
            endTime = env["endTime"]    
            inTimeRange = in_time_window(t, startTime, endTime)
        selectClause = "SELECT " + ", ".join([f"AVG({v}) {a}" for v, a in zip(variables, aliases)]) + " FROM " + table
        timeClause = f" WHERE [time] BETWEEN '{shift_dt(t, -timeTolerance)}' AND '{shift_dt(t, timeTolerance)}' "
        if not inTimeRange or isClimatology: timeClause = f" WHERE [month]={get_month(t)} "
        latClause = f" AND lat BETWEEN {lat-latTolerance} AND {lat+latTolerance} "
        lonClause = f" AND lon BETWEEN {lon-lonTolerance} AND {lon+lonTolerance} "
        depthClause = f" AND depth BETWEEN {depth-depthTolerance} AND {depth+depthTolerance} "
        if not hasDepth: depthClause = ""                
        return selectClause + timeClause + latClause + lonClause + depthClause        


    if len(df) != 1: halt(f"Invalid dataframe input.\nExpected a single row dataframe but received {len(df)} rows.")
    MAX_SURFACE_DEPTH = 10
    rowIndex = df.index.values[0]
    df.reset_index(drop=True, inplace=True)
    t= df.iloc[0]["time"]
    lat = df.iloc[0]["lat"]
    lon = df.iloc[0]["lon"] 
    depth = 0
    if 'depth' in df.columns: depth = df.iloc[0]["depth"]
    for table, env in targets.items():
        print(f"{rowIndex} / {totalRows} ... sampling {table}", end="\r")
        # do the colocalization: if either the target dataset has depth field (it's not sattelite, for example) or 
        # the depth of source measurement is less than `MAX_SURFACE_DEPTH`
        # if env["hasDepth"] or depth <= MAX_SURFACE_DEPTH:       
        if True:  # ignoring `MAX_SURFACE_DEPTH` for now 
            query = construc_query(table, env, t, lat, lon, depth)
            matchedEnv = api.query(query, servers=["rossby"])
            if len(matchedEnv)>0:
                for v in env["aliases"]: df.at[0, v] = matchedEnv.iloc[0][v] 
    return df


def Sample(source, targets):
    """
    placeholder for the `Sample` class.

    Samples the targest datasets using the time-location of the source dataset
    Returns a dataframe containing the original source data and the joined colocalized target variables.

    :param dataframe source: a dataframe containing the source datasets (must have time-location columns).
    :param dictionary targets: dcitionary containing the target table/variables and tolerance parameters.
    The items in `tolerances` list are: temporal tolerance [days], meridional tolerance [deg], 
    zonal tolerance [deg], and vertical tolerance [m], repectively.
    `targets` example:

    targets = {
            "tblSST_AVHRR_OI_NRT": {
                                    "variables": ["sst"],
                                    "tolerances": [1, 0.25, 0.25, 5]
                                    },
            "tblAltimetry_REP": {
                                    "variables": ["sla", "adt", "ugosa", "vgosa"],
                                    "tolerances": [1, 0.25, 0.25, 5]
                                    }
            }

    """
    if len(source) > MAX_SAMPLE_SOURCE: halt(f"Source dataset too large. Maximum allowed number of records is {MAX_SAMPLE_SOURCE}.")
    api = API()       
    print("Gathering metadata .... ")
    targets = add_target_meta(api, targets)
    source = add_target_columns(source, targets)
    dfs = [source.loc[i].to_frame().T for i in range(len(source))]
    colocalizedList, columns = [], []
    print("Sampling starts.")
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futureObjs = executor.map(match, dfs, [api] * len(dfs), [targets] * len(dfs), list(range(len(dfs))), [len(dfs)] * len(dfs))           
        for fo in futureObjs:
            if len(colocalizedList) < 1: columns = list(fo.columns)                                                   
            colocalizedList.append(fo.values.tolist()[0])
    print("\nSampling ends.")
    return pd.DataFrame(colocalizedList, columns=columns)


    # print("Sampling starts ...")
    # with concurrent.futures.ThreadPoolExecutor() as executor:
    #     futureObjs = [executor.submit(match, dfs[i], api, targets, i, len(dfs)) for i in range(len(dfs))]
    #     for res in tqdm(concurrent.futures.as_completed(futureObjs)):
    #        row = res.result() 
    #        if len(colocalizedList) < 1: columns = list(row.columns)                                                   
    #        colocalizedList.append(row.values.tolist()[0])
    #     return pd.DataFrame(colocalizedList, columns=columns)
