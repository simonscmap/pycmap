"""
Author: Mohammad Dehghani Ashkezari <mdehghan@uw.edu>

Date: 2019-06-28

Function: Host a collection of shared multi-purpose helper functions.
"""

import os
import sys
from tqdm import tqdm
from colorama import Fore, Back, Style, init
import numpy as np
import pandas as pd
import webbrowser
import IPython

MAX_ROWS = 2000000
MAX_SAMPLE_SOURCE = 500000

def halt(msg):
        """Prints an error message and terminates the program."""
        msg = '\n' + msg
        init(convert=True)
        print(Fore.RED + msg, file=sys.stderr)    
        print(Style.RESET_ALL, end='')
        sys.exit(1)
        return

def print_tqdm(msg, err=False):
        """Print helper function compatible with tqdmm progressbar."""
        # init()
        msg = '\n' + msg
        if err:
                tqdm.write(Fore.RED + msg)        
        else:    
                tqdm.write(msg)
        tqdm.write(Style.RESET_ALL, end='')
        return

def get_base_url():
        """Returns API root endpoint."""
        return os.environ.get(
        'CMAP_API_BASE_URL', 'https://simonscmap.com').rstrip('/')


def jupytered():
        """Returns True if jupyter notebook has invoked the package."""
        jup = False
        import __main__ as main
        if not hasattr(main, '__file__'):
                jup = True 
        return jup

def inline():
        """
        Checks if the package results should get prepared for an "inline" context.        
        Currently, just calls the jupytered function.
        """            
        return jupytered() 


def make_filename_by_table_var(table, variable, prefix=''):
        """Generate a filename (without extention) using table and variable names."""
        if prefix != '': prefix += '_'                
        return prefix + variable + '_' + table


def canvas_rect(dw, dh):
        """Resizes a canvas dimensions so that it better fits on client browser.""" 
        ar = dw / dh 
        h = 400 if ar > 3 else 500
        w_min = 300
        w_max = 1000
        w = int(ar * h)
        if w > w_max: w = w_max
        if w < w_min: w = w_min
        return w, h


def get_data_limits(data, quant=0.05):
        """Returns low and high quantile limits of a numeric array."""
        data = np.array(data).flatten()
        return np.nanquantile(data, quant), np.nanquantile(data, 1-quant)



# def get_token(token=None):        
#         token = token or os.environ.get('CMAP_API_KEY')
#         if token in [None, '']:
#         halt('API Key must be specified to access CMAP API')
#         return token









def config_path():
        """Returns the path to the config spreadsheet file."""
        return os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config.csv')


def initiate_config_file(token, vizEngine, exportDir, exportFormat, figureDir):
        """Creates a .csv file hosting the primary project configs """
        if vizEngine is None: vizEngine = 'plotly'
        if exportDir is None: exportDir = './export/'
        if exportFormat is None: exportFormat = '.csv'
        if figureDir is None: figureDir = './figure/'
        config = {
                  'token': [token], 
                  'vizEngine': [vizEngine], 
                  'exportDir': [exportDir], 
                  'exportFormat': [exportFormat],
                  'figureDir': [figureDir]
                  }
        pd.DataFrame(config).to_csv(config_path(), index=False)
        return

def remove_angle_brackets(token):
        """Removes angle brackets at start and end of the token, if exist."""
        if token is not None:
                if token[0] == '<': token = token[1:]
                if token[-1] == '>': token = token[:-1]
        return token


def save_config(token=None, vizEngine=None, exportDir=None, exportFormat=None, figureDir=None):
        """Updates the project's configs at the config spreadsheet."""
        configPath = config_path()    
        if not os.path.isfile(configPath):
                initiate_config_file(token, vizEngine, exportDir, exportFormat, figureDir)     
        df = pd.read_csv(configPath)
        if token is not None:
                df['token'] = remove_angle_brackets(token)
        if vizEngine is not None:
                supportedVizEngines = ['bokeh', 'plotly']
                if vizEngine not in supportedVizEngines:
                        halt('%s is not a supported visualization library' % vizEngine)
                df['vizEngine'] = vizEngine
        if exportDir is not None:
                df['exportDir'] = exportDir
        if exportFormat is not None:
                df['exportFormat'] = exportFormat
        if figureDir is not None:
                df['figureDir'] = figureDir
        df.to_csv(configPath, index=False)        
        return


def load_config():
        """Loads the config spreadsheet and returns it as a dataframe."""
        configPath = config_path()
        if not os.path.isfile(configPath):
                msg = '\nAPI key not found!\n'
                msg = msg + 'Please pass the API key using the following code:\n'    
                msg = msg + 'import pycmap\n'    
                msg = msg + 'pycmap.API(<api_key>)\n'    
                halt(msg)
        return pd.read_csv(configPath)    


def get_token():
        """Returns the API key."""
        return remove_angle_brackets(load_config()['token'][0])

def get_vizEngine():
        """Returns the visualization library name."""
        return load_config()['vizEngine'][0]

def get_export_dir():
        """Returns the path to the export directory."""
        return load_config()['exportDir'][0]

def get_export_format():
        """Returns the file format of the exported files."""
        return load_config()['exportFormat'][0]

def get_figure_dir():
        """Returns the path to the figure directory."""
        return load_config()['figureDir'][0]

def get_bokeh_tools():
        """Returns a list tools used along with a bokeh graph."""
        return 'crosshair,pan,zoom_in,wheel_zoom,zoom_out,box_zoom,reset,save'        



def normalize(vals, min_max=False):
    """Takes an array and either normalize to min/max, standardize it (remove the mean and divide by standard deviation)."""      
    if min_max:
        normalized_vals=(vals-np.nanmin(vals))/(np.nanmax(vals)-np.nanmin(vals))
    else:    
        normalized_vals=(vals-np.nanmean(vals))/np.nanstd(vals)
    return normalized_vals


def open_HTML(path):
    """Display HTML file by defaut browser or inline in case jupyter is the caller."""    
    if jupytered():
        vObj = IPython.display.IFrame(path, width=800, height=400)
        IPython.display.display(vObj)
    else:
        path = 'file://' + os.path.realpath(path)
        webbrowser.open(path, new=2)
    return

def catalog_sql():
        return """
        SELECT RTRIM(LTRIM(Short_Name)) AS Variable,
        [tblVariables].Table_Name AS [Table_Name],
        RTRIM(LTRIM(Long_Name)) AS [Long_Name],
        RTRIM(LTRIM(Unit)) AS [Unit],
        RTRIM(LTRIM(Make)) AS [Make],
        RTRIM(LTRIM(Sensor)) AS [Sensor],
        RTRIM(LTRIM(Process_Stage_Long)) AS [Process_Level],
        RTRIM(LTRIM(Study_Domain)) AS [Study_Domain],
        RTRIM(LTRIM(Temporal_Resolution)) AS [Temporal_Resolution],
        RTRIM(LTRIM(Spatial_Resolution)) AS [Spatial_Resolution],
        JSON_VALUE(JSON_stats,'$.time.min') AS [Time_Min],
        JSON_VALUE(JSON_stats,'$.time.max') AS [Time_Max],
        CAST(JSON_VALUE(JSON_stats,'$.lat.min') AS float) AS [Lat_Min],
        CAST(JSON_VALUE(JSON_stats,'$.lat.max') AS float) AS [Lat_Max],
        CAST(JSON_VALUE(JSON_stats,'$.lon.min') AS float) AS [Lon_Min],
        CAST(JSON_VALUE(JSON_stats,'$.lon.max') AS float) AS [Lon_Max],
        CAST(JSON_VALUE(JSON_stats,'$.depth.min') AS float) AS [Depth_Min],
        CAST(JSON_VALUE(JSON_stats,'$.depth.max') AS float) AS [Depth_Max],
        CAST(JSON_VALUE(JSON_stats,'$."'+[Short_Name]+'"."25%"') AS float) AS [Variable_25th],
        CAST(JSON_VALUE(JSON_stats,'$."'+[Short_Name]+'"."50%"') AS float) AS [Variable_50th],
        CAST(JSON_VALUE(JSON_stats,'$."'+[Short_Name]+'"."75%"') AS float) AS [Variable_75th],
        CAST(JSON_VALUE(JSON_stats,'$."'+[Short_Name]+'".count') AS float) AS [Variable_Count],
        CAST(JSON_VALUE(JSON_stats,'$."'+[Short_Name]+'".mean') AS float) AS [Variable_Mean],
        CAST(JSON_VALUE(JSON_stats,'$."'+[Short_Name]+'".std') AS float) AS [Variable_Std],
        CAST(JSON_VALUE(JSON_stats,'$."'+[Short_Name]+'".min') AS float) AS [Variable_Min],
        CAST(JSON_VALUE(JSON_stats,'$."'+[Short_Name]+'".max') AS float) AS [Variable_Max],
        --RTRIM(LTRIM(Comment)) AS [Comment],
        RTRIM(LTRIM(Dataset_Long_Name)) AS [Dataset_Name],
        RTRIM(LTRIM(Dataset_Name)) AS [Dataset_Short_Name],
        RTRIM(LTRIM([Data_Source])) AS [Data_Source],
        RTRIM(LTRIM(Distributor)) AS [Distributor],
        RTRIM(LTRIM([Description])) AS [Dataset_Description],
        RTRIM(LTRIM([Acknowledgement])) AS [Acknowledgement],
        [tblVariables].Dataset_ID AS [Dataset_ID],
        [tblVariables].ID AS [ID],
        --[tblVariables].Visualize AS [Visualize],
        --[keywords_agg].Keywords AS [Keywords],
        [Dataset_Metadata].Unstructured_Dataset_Metadata as [Unstructured_Dataset_Metadata],
        [Variable_Metadata].Unstructured_Variable_Metadata as [Unstructured_Variable_Metadata]
        FROM tblVariables
        JOIN tblDataset_Stats ON [tblVariables].Dataset_ID = [tblDataset_Stats].Dataset_ID
        JOIN tblDatasets ON [tblVariables].Dataset_ID=[tblDatasets].ID
        JOIN tblTemporal_Resolutions ON [tblVariables].Temporal_Res_ID=[tblTemporal_Resolutions].ID
        JOIN tblSpatial_Resolutions ON [tblVariables].Spatial_Res_ID=[tblSpatial_Resolutions].ID
        JOIN tblMakes ON [tblVariables].Make_ID=[tblMakes].ID
        JOIN tblSensors ON [tblVariables].Sensor_ID=[tblSensors].ID
        JOIN tblProcess_Stages ON [tblVariables].Process_ID=[tblProcess_Stages].ID
        JOIN tblStudy_Domains ON [tblVariables].Study_Domain_ID=[tblStudy_Domains].ID
        --JOIN (SELECT var_ID, STRING_AGG (CAST(keywords as NVARCHAR(MAX)), ', ') AS Keywords FROM tblVariables var_table
        --JOIN tblKeywords key_table ON [var_table].ID = [key_table].var_ID GROUP BY var_ID)
        --AS keywords_agg ON [keywords_agg].var_ID = [tblVariables].ID
        LEFT JOIN (SELECT Dataset_ID, STRING_AGG (CAST(JSON_Metadata as NVARCHAR(MAX)), ', ') AS Unstructured_Dataset_Metadata FROM tblDatasets dataset_table
        JOIN tblDatasets_JSON_Metadata meta_table ON [dataset_table].ID = [meta_table].Dataset_ID GROUP BY Dataset_ID)
        AS Dataset_Metadata ON [Dataset_Metadata].Dataset_ID = [tblDatasets].ID
        LEFT JOIN (SELECT Var_ID, STRING_AGG (CAST(JSON_Metadata as NVARCHAR(MAX)), ', ') AS Unstructured_Variable_Metadata FROM tblVariables var_meta_table
        JOIN tblVariables_JSON_Metadata meta_table ON [var_meta_table].ID = [meta_table].Var_ID GROUP BY Var_ID)
        AS Variable_Metadata ON [Variable_Metadata].Var_ID = [tblVariables].ID
        """
