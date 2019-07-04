import pycmap

cmap = pycmap.API('4f101ed0-1f13-41a5-ab7d-2c11a405a326')
cmap = pycmap.API('90d862e0-8d49-11e9-8d22-0f5810db0206', vizEngine='plotly')





# df = cmap.query('select * from tblSensors')



# tablesName = 'tblsst_AVHRR_OI_NRT'
# field = 'sst'
# dt1 = '2016-04-30'
# dt2 = '2016-04-30'
# lat1, lat2 = 10, 70
# lon1, lon2 = -180, -80
# depth1, depth2 = 0, 0.5
# args = [tablesName, field, dt1, dt2, lat1, lat2, lon1, lon2, depth1, depth2]
# query = 'EXEC uspSpaceTime ?, ?, ?, ?, ?, ?, ?, ?, ?, ?'
# df = cmap.stored_proc(query, args)



# df = cmap.get_catalog()

# df = cmap.has_field('tblPisces_NRT', 'O2')
# print(df)




# df = cmap.space_time('tblsst_AVHRR_OI_NRT', 'sst', '2016-04-30', '2016-04-30', 10, 70, -180, -80, 0, 0.5)


# df = cmap.get_metadata('tblsst_AVHRR_OI_NRT', 'sst')




# from pycmap.bokehHist import BokehHist
# table = 'tblsst_AVHRR_OI_NRT'
# variable = 'sst'
# df = cmap.space_time(table, variable, '2016-04-30', '2016-04-30', 10, 70, -180, -80, 0, 0.5)
# hist = BokehHist(df, table, variable)
# hist.xlabel = variable
# hist.ylabel = 'Density'
# hist.legend = variable
# hist.render()




# ########## plot hitogram

# from pycmap.viz import plot_hist

# table = ['tblsst_AVHRR_OI_NRT']
# variable = ['sst']
# exportDataFlag = True
# go = plot_hist(table, variable, '2016-04-30', '2016-04-30', 10, 70, -180, -80, 0, 0.5, exportDataFlag)

# go.pdf=True
# go.xlabel = 'salam'
# go.title='new title'
# go.width = 300
# go.height = 300
# go.render()







# ########## plot map

# from pycmap.viz import plot_map

# table = ['tblsst_AVHRR_OI_NRT', 'tblPisces_NRT', 'tblWind_NRT', 'tblWOA_Climatology', 'tblAltimetry_REP', 'tblAltimetry_REP']
# variable = ['sst', 'Fe', 'wind_stress', 'density_WOA_clim', 'sla', 'adt']

# table = [ 'tblPisces_NRT', 'tblArgoMerge_REP']
# variable = [ 'O2', 'argo_merge_salinity_adj']

# table = ['tblArgoMerge_REP']
# variable = ['argo_merge_salinity_adj']


# table = [ 'tblPisces_NRT', 'tblPisces_NRT', 'tblCHL_REP', 'tblAltimetry_rep']
# variable = [ 'CHL', 'Fe', 'chl', 'vgosa']


# table = ['tblPisces_NRT']
# variable = ['NO3']


# exportDataFlag = False
# go = plot_map(table, variable, '2016-04-30', '2016-04-30', 10, 70, -180, -80, 0, 0.5, exportDataFlag, levels=10)

# # # go[0].xlabel = 'salam'
# # # go[0].title='new title'
# # # go[0].width = 300
# # # go[0].height = 300
# go[0].vmin=0
# go[0].vmax=10
# go[0].levels = 10.3
# go[0].render()







########## plot section

# from pycmap.viz import plot_section

# table = ['tblWOA_Climatology' ,'tblPisces_NRT', 'tblArgoMerge_REP']
# variable = ['density_WOA_clim' ,'NO3', 'argo_merge_salinity_adj']


# table = ['tblPisces_NRT']
# variable = ['NO3']


# go = plot_section(table, variable, '2016-04-30', '2016-04-30', 10, 60, -160, -158, 0, 5000, 
# exportDataFlag=False, show=True, levels=0)

# go[0].xlabel = 'salam'
# go[0].title='new title'
# go[0].width = 300
# go[0].height = 300
# go[0].vmin = 10
# go[0].vmax = 30
# go[0].levels=20
# go[0].render()