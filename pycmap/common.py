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
