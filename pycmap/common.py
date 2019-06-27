import os
import sys
from tqdm import tqdm
from colorama import Fore, Back, Style, init
import pandas as pd



def halt(msg):
        init(convert=True)
        print(Fore.RED + msg, file=sys.stderr)    
        print(Style.RESET_ALL, end='')
        sys.exit(1)
        return

def print_tqdm(msg, err=False):
    # init()
    if err:
        tqdm.write(Fore.RED + msg)        
    else:    
        tqdm.write(msg)
    tqdm.write(Style.RESET_ALL, end='')
    return

def get_base_url():
        return os.environ.get(
        'CMAP_API_BASE_URL', 'https://simonscmap.com').rstrip('/')


# def get_token(token=None):        
#         token = token or os.environ.get('CMAP_API_KEY')
#         if token in [None, '']:
#         halt('API Key must be specified to access CMAP API')
#         return token









def config_path():
        return os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config.csv')


def initiate_config_file(token, vizEngine):
        """ Create a .csv file hosting the primary project configs """

        config = {'token': [token], 'vizEngine': [vizEngine]}
        pd.DataFrame(config).to_csv(config_path(), index=False)
        return


def save_config(token=None, vizEngine=None):
        configPath = config_path()    
        if not os.path.isfile(configPath):
                initiate_config_file(token, vizEngine)     
        df = pd.read_csv(configPath)
        if token is not None:
                df['token'] = token
        if vizEngine is not None:
                df['vizEngine'] = vizEngine
        df.to_csv(configPath, index=False)        
        return


def load_config():
        configPath = config_path()
        if not os.path.isfile(configPath):
                msg = '\nAPI key not found!\n'
                msg = msg + 'Please pass the API key using the following code:\n'    
                msg = msg + 'import pycmap\n'    
                msg = msg + 'pycmap.API(<api_key>)\n'    
                halt(msg)
        return pd.read_csv(configPath)    


def get_token():
        return load_config()['token'][0]

def get_vizEngine():
        return load_config()['vizEngine'][0]


def get_bokeh_tools():
        return 'pan,wheel_zoom,zoom_in,zoom_out,box_zoom, undo,redo,reset,tap,save,box_select,poly_select,lasso_select'        