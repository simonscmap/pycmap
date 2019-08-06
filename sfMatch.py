"""
Author: Mohammad Dehghani Ashkezari <mdehghan@uw.edu>

Date: 2019-08-05

Function: Colocalize (match) Seaflow cruises with a given list of CMAP variables.
"""

import pycmap
from collections import namedtuple
import pandas as pd




def all_cruises():
    cruises = list(api.cruises().Name)[:-21]   # remove AMT cruises
    cruises.remove('Tokyo_1')
    cruises.remove('Tokyo_2')
    cruises.remove('Tokyo_3')
    cruises.remove('Tokyo_4')
    return cruises


def open_ocean_cruises():
    return ['RR1814', 'RR1815', 'MGL1704', 'KOK1606', 'KM1713', 'KM1712', 'KM1502', 'KM1314', 'KN210-04', 'TN292']        


def not_open_ocean_cruises():
    all = all_cruises()
    open = open_ocean_cruises()
    return list(set(all) - set(open))    


def match_params():
    Param = namedtuple('Param', ['table', 'variable', 'temporalTolerance', 'latTolerance', 'lonTolerance', 'depthTolerance'])
    params = []
    params.append(Param('tblSeaFlow', 'prochloro_abundance', 0, 0.1, 0.1, 5))
    params.append(Param('tblSeaFlow', 'prochloro_diameter', 0, 0.1, 0.1, 5))
    params.append(Param('tblSeaFlow', 'prochloro_carbon_content', 0, 0.1, 0.1, 5))
    params.append(Param('tblSeaFlow', 'prochloro_biomass', 0, 0.1, 0.1, 5))
    params.append(Param('tblSeaFlow', 'synecho_abundance', 0, 0.1, 0.1, 5))
    params.append(Param('tblSeaFlow', 'synecho_diameter', 0, 0.1, 0.1, 5))
    params.append(Param('tblSeaFlow', 'synecho_carbon_content', 0, 0.1, 0.1, 5))
    params.append(Param('tblSeaFlow', 'synecho_biomass', 0, 0.1, 0.1, 5))
    params.append(Param('tblSeaFlow', 'picoeuk_abundance', 0, 0.1, 0.1, 5))
    params.append(Param('tblSeaFlow', 'picoeuk_diameter', 0, 0.1, 0.1, 5))
    params.append(Param('tblSeaFlow', 'picoeuk_carbon_content', 0, 0.1, 0.1, 5))
    params.append(Param('tblSeaFlow', 'picoeuk_biomass', 0, 0.1, 0.1, 5))
    # params.append(Param('tblSeaFlow', 'croco_abundance', 0, 0.1, 0.1, 5))
    # params.append(Param('tblSeaFlow', 'croco_diameter', 0, 0.1, 0.1, 5))
    # params.append(Param('tblSeaFlow', 'croco_carbon_content', 0, 0.1, 0.1, 5))
    # params.append(Param('tblSeaFlow', 'croco_biomass', 0, 0.1, 0.1, 5))
    params.append(Param('tblSeaFlow', 'total_biomass', 0, 0.1, 0.1, 5))
    params.append(Param('tblSeaFlow', 'par', 0, 0.1, 0.1, 5))

    ######## satellite
    params.append(Param('tblSST_AVHRR_OI_NRT', 'sst', 1, 0.25, 0.25, 5))
    params.append(Param('tblSSS_NRT', 'sss', 1, 0.25, 0.25, 5))
    params.append(Param('tblCHL_REP', 'chl', 4, 0.25, 0.25, 5))
    params.append(Param('tblModis_AOD_REP', 'AOD', 15, 1, 1, 5))
    params.append(Param('tblAltimetry_REP', 'sla', 1, 0.25, 0.25, 5))
    params.append(Param('tblAltimetry_REP', 'adt', 1, 0.25, 0.25, 5))
    params.append(Param('tblAltimetry_REP', 'ugos', 1, 0.25, 0.25, 5))
    params.append(Param('tblAltimetry_REP', 'vgos', 1, 0.25, 0.25, 5))
    # params.append(Param('tblLCS_REP', 'ftle_bw_sla', 1, 0.125, 0.125, 5))
    # params.append(Param('tblLCS_REP', 'ftle_fw_sla', 1, 0.125, 0.125, 5))
    # params.append(Param('tblLCS_REP', 'disp_bw_sla', 1, 0.125, 0.125, 5))

    ######## model
    params.append(Param('tblPisces_NRT', 'Fe', 4, 0.5, 0.5, 5))
    params.append(Param('tblPisces_NRT', 'NO3', 4, 0.5, 0.5, 5))
    params.append(Param('tblPisces_NRT', 'O2', 4, 0.5, 0.5, 5))
    params.append(Param('tblPisces_NRT', 'PO4', 4, 0.5, 0.5, 5))
    params.append(Param('tblPisces_NRT', 'Si', 4, 0.5, 0.5, 5))
    params.append(Param('tblDarwin_Nutrient_Climatology', 'NH4_darwin_clim', 0, 0.5, 0.5, 5))
    params.append(Param('tblDarwin_Nutrient_Climatology', 'NO2_darwin_clim', 0, 0.5, 0.5, 5))
    params.append(Param('tblDarwin_Nutrient_Climatology', 'SiO2_darwin_clim', 0, 0.5, 0.5, 5))
    params.append(Param('tblDarwin_Nutrient_Climatology', 'DOC_darwin_clim', 0, 0.5, 0.5, 5))
    params.append(Param('tblDarwin_Nutrient_Climatology', 'DON_darwin_clim', 0, 0.5, 0.5, 5))
    params.append(Param('tblDarwin_Nutrient_Climatology', 'DOP_darwin_clim', 0, 0.5, 0.5, 5))
    params.append(Param('tblDarwin_Nutrient_Climatology', 'DOFe_darwin_clim', 0, 0.5, 0.5, 5))
    params.append(Param('tblDarwin_Nutrient_Climatology', 'PIC_darwin_clim', 0, 0.5, 0.5, 5))
    params.append(Param('tblDarwin_Nutrient_Climatology', 'ALK_darwin_clim', 0, 0.5, 0.5, 5))
    params.append(Param('tblDarwin_Nutrient_Climatology', 'FeT_darwin_clim', 0, 0.5, 0.5, 5))

    ####### WOA
    params.append(Param('tblWOA_Climatology', 'density_WOA_clim', 0, .75, .75, 5))
    params.append(Param('tblWOA_Climatology', 'nitrate_WOA_clim', 0, 0.75, 0.75, 5))
    params.append(Param('tblWOA_Climatology', 'phosphate_WOA_clim', 0, 0.75, 0.75, 5))
    params.append(Param('tblWOA_Climatology', 'silicate_WOA_clim', 0, 0.75, 0.75, 5))
    params.append(Param('tblWOA_Climatology', 'oxygen_WOA_clim', 0, 0.75, 0.75, 5))

    tables, variables, temporalTolerance, latTolerance, lonTolerance, depthTolerance = [], [], [], [], [], []
    for i in range(len(params)):
        tables.append(params[i].table)
        variables.append(params[i].variable)
        temporalTolerance.append(params[i].temporalTolerance)
        latTolerance.append(params[i].latTolerance)
        lonTolerance.append(params[i].lonTolerance)
        depthTolerance.append(params[i].depthTolerance)
    
    return tables, variables, temporalTolerance, latTolerance, lonTolerance, depthTolerance







api = pycmap.API(token='', vizEngine='plotly')
cruises = not_open_ocean_cruises()



tables, variables, temporalTolerance, latTolerance, lonTolerance, depthTolerance = match_params()
df = pd.DataFrame({})
for cruise in cruises:
    print('\n********************************')
    print('Preparing %s cruise...' % cruise)
    print('********************************\n')
    data = api.along_track(
                          cruise=cruise,     
                          tables=tables,
                          variables=variables,
                          temporalTolerance=temporalTolerance, 
                          latTolerance=latTolerance, 
                          lonTolerance=lonTolerance, 
                          depthTolerance=depthTolerance,
                          depth1=0,
                          depth2=5
                          )

    if len(df) < 1:
        df = data
    else:
        df = pd.concat([df, data], ignore_index=True)
    
    data.to_csv('export/%s.csv' % cruise, index=False)

df.to_csv('export/sfMatch.csv', index=False)    