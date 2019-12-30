"""
Author: Mohammad Dehghani Ashkezari <mdehghan@uw.edu>

Date: 2019-07-01

Function: Associate colormap to variables.
"""


import cmocean





def getPalette(varName):
    paletteName = cmocean.cm.balance
    if varName.find('picoeukaryote') != -1:
        paletteName = 'magma'
    elif varName.find('prokaryote') != -1:
        paletteName = 'inferno'
    elif varName.find('zooplankton') != -1:
        paletteName = 'plasma'
    elif varName.find('POC') != -1:
        paletteName = 'viridis'
    elif varName.find('POFe') != -1:
        paletteName = 'viridis'
    elif varName.find('PON') != -1:
        paletteName = 'viridis'
    elif varName.find('POSi') != -1:
        paletteName = 'viridis'
    elif varName.find('DOFe') != -1:
        paletteName = 'viridis'
    elif varName.find('DON') != -1:
        paletteName = 'viridis'
    elif varName.find('DOP') != -1:
        paletteName = 'viridis'
    elif varName.find('SiO2') != -1:
        paletteName = 'viridis'
    elif varName.find('FeT') != -1:
        paletteName = cmocean.cm.curl
    elif varName.find('Fe') != -1:
        paletteName = cmocean.cm.curl
    elif varName.find('CDOM') != -1:
        paletteName = 'plasma'
    elif varName.find('PHYC') != -1:
        paletteName = 'viridis'
    elif varName.find('PP') != -1:
        paletteName = 'viridis'
    elif varName.find('Si') != -1:
        paletteName = 'viridis'
    elif varName.find('NO3') != -1:
        paletteName = 'RdBu'
    elif varName.find('NO2') != -1:
        paletteName = 'plasma'
    elif varName.find('NH4') != -1:
        paletteName = 'plasma'
    elif varName.find('PO4') != -1:
        paletteName = 'viridis'
    elif varName.find('O2') != -1:
        paletteName = cmocean.cm.curl
    elif varName.find('ALK') != -1:
        paletteName = 'magma'
    elif varName.find('PIC') != -1:
        paletteName = 'plasma'
    elif varName.find('chl') != -1:
        paletteName = cmocean.cm.algae
    elif varName.find('CHL') != -1:
        paletteName = cmocean.cm.curl
    elif varName.find('diazotroph') != -1:
        paletteName = 'inferno'
    elif varName.find('dinoflagellate') != -1:
        paletteName = 'magma'
    elif varName.find('diatom') != -1:
        paletteName = 'viridis'
    elif varName.find('cocco') != -1:
        paletteName = 'plasma'
    elif varName.find('DIC') != -1:
        paletteName = 'viridis'
    elif varName.find('DOC') != -1:
        paletteName = 'viridis'
    elif varName.find('wind_stress') != -1:
        paletteName = 'plasma'
    elif varName.find('mld_nrt') != -1:
        paletteName = 'plasma'
    elif varName.find('ftle_nrt') != -1:
        paletteName = 'inferno'
    elif varName.find('disp_nrt') != -1:
        paletteName = 'inferno'
    elif varName.find('sst') != -1:
        paletteName = 'inferno'
    elif varName.find('sss') != -1:
        paletteName = 'inferno'
    elif varName.find('AOD') != -1:
        paletteName = 'inferno'
    elif varName.find('sla') != -1:
        paletteName = cmocean.cm.balance
    elif varName.find('AOD') != -1:
        paletteName = 'inferno'
    elif varName.find('PAR') != -1:
        paletteName = 'Spectral_r'
    return paletteName
