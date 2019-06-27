

from .cmap import API  # noqa
from .common import (
                     get_vizEngine,
                     print_tqdm
                    )
from tqdm import tqdm
from pycmap.bokehHist import BokehHist


def hist_object(data, table, variable):
    """Instantiate a histogram according to the selected vizEngine."""
    vizEngine = get_vizEngine().lower().strip()
    obj = None
    if vizEngine == 'bokeh':
        obj = BokehHist(data, table, variable)
    return obj
   

def plot_hist(tables, variables, dt1, dt2, lat1, lat2, lon1, lon2, depth1, depth2, exportDataFlag):
    """Create histogram graph for each variable."""    
    for i in tqdm(range(len(tables)), desc='overall'):
        data = API().space_time(tables[i], variables[i], dt1, dt2, lat1, lat2, lon1, lon2, depth1, depth2)
        if len(data) < 1:
            print_tqdm('%d: No matching entry found: Table: %s, Variable: %s ' % (i+1, tables[i], variables[i]), err=True )
            continue
        print_tqdm('%d: %s retrieved (%s).' % (i+1, variables[i], tables[i]), err=False)
        hist = hist_object(data, tables[i], variables[i])
        hist.xlabel = variables[i]
        hist.ylabel = ''
        hist.legend = variables[i]
        hist.render()

        # if exportDataFlag:
        #     exportData(y, tables[i], variables[i], startDate, endDate, lat1, lat2, lon1, lon2, depth1, depth2)
    return