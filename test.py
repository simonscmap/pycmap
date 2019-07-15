import pycmap

cmap = pycmap.API('4f101ed0-1f13-41a5-ab7d-2c11a405a326')
cmap = pycmap.API('c7f10130-78f2-11e9-82a6-793e7fd02bc0', vizEngine='plotly')





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
# print(df)



# df = cmap.get_catalog()

# df = cmap.has_field('tblPisces_NRT', 'O2')
# print(df)




# df = cmap.space_time('tblsst_AVHRR_OI_NRT', 'sst', '2016-04-30', '2016-04-30', 10, 70, -180, -80, 0, 0.5)


# df = cmap.get_metadata('tblsst_AVHRR_OI_NRT', 'sst')



#### colocalize
# matched = cmap.match(
#                 'uspMatch', 
#                 'tblSeaFlow', 
#                 'synecho_abundance', 
#                 ['tblCHL_REP', 'tblPisces_NRT'], 
#                 ['chl', 'Fe'], 
#                 '2016-04-20', 
#                 '2016-05-04', 
#                 20, 
#                 40, 
#                 -160, 
#                 -157, 
#                 0, 
#                 5, 
#                 4, 
#                 0.5, 
#                 0.5, 
#                 5
#                 )


# matched.to_csv('matched.csv', index=False)






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


# table = ['tblPisces_NRT', 'tblAltimetry_REP', 'tblsst_AVHRR_OI_NRT', 'tblSSS_NRT']
# variable = ['NO3', 'adt', 'sst', 'sss']

# table = ['tblPisces_NRT']
# variable = ['NO3']


# exportDataFlag = False
# # go = plot_map(table, variable, '2016-04-30', '2016-04-30', 10, 70, -180, -80, 0, 0.5, exportDataFlag, levels=10)
# go = plot_map(table, variable, '2016-04-30', '2016-04-30', -90, 90, -180, 180, 0, 0.5, exportDataFlag, levels=0, surface3D=False)

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
# exportDataFlag=False, show=True, levels=10)

# go[0].xlabel = 'salam'
# go[0].title='new title'
# go[0].width = 300
# go[0].height = 300
# go[0].vmin = 10
# go[0].vmax = 30
# go[0].levels=20
# go[0].render()







########## plot timeseries

# from pycmap.viz import plot_timeseries

# table = ['tblWOA_Climatology' ,'tblPisces_NRT', 'tblArgoMerge_REP']
# variable = ['density_WOA_clim' ,'NO3', 'argo_merge_salinity_adj']



# table = ['tblWOA_Climatology', 'tblDarwin_Nutrient_Climatology', 'tblAltimetry_REP' ,'tblPisces_NRT']
# variable = ['density_WOA_clim', 'ALK_darwin_clim', 'adt' ,'NO3' ]

# # table = ['tblAltimetry_REP']
# # variable = ['adt']

# go = plot_timeseries(table, variable, '2014-04-30', '2016-07-30', 30, 32, -160, -158, 0, 10, 
# exportDataFlag=True, show=True, interval='q')

# go[0].xlabel = 'salam'
# go[0].title='new title'
# go[0].width = 300
# go[0].height = 300
# go[0].msize=10
# go[0].fillAlpha=0.7
# go[0].render()




# st = cmap.subset('uspSpaceTime', 'tblAltimetry_REP', 'adt', '2016-04-30', '2016-07-30', 30, 32, -160, -158, 0, 10)












#### corr plot
# from pycmap.viz import plot_corr_map

# grad1
# go = plot_corr_map(
#                 'tblSeaFlow', 
#                 # 'synecho_abundance', 
#                 # 'prochloro_abundance',
#                 'picoeuk_abundance',
#                 ['tblCHL_REP', 'tblPisces_NRT', 'tblPisces_NRT', 'tblSSS_NRT'], 
#                 ['chl', 'Fe', 'NO3', 'SSS'], 
#                 '2016-04-20', 
#                 '2016-05-04', 
#                 20, 
#                 40, 
#                 -160, 
#                 -157, 
#                 0, 
#                 5, 
#                 4, 
#                 0.25, 
#                 0.25, 
#                 5,
#                 method='spearman', exportDataFlag=True, show=True
#                 )
                
# flombaum
# go = plot_corr_map(
#                 'tblFlombaum', 
#                 # 'prochlorococcus_abundance_flombaum',
#                 'synechococcus_abundance_flombaum',
#                 ['tblCHL_REP', 'tblSST_AVHRR_OI_NRT', 'tblAltimetry_REP', 'tblDarwin_Nutrient_3day', 'tblDarwin_Nutrient_3day'], 
#                 ['chl', 'sst', 'sla', 'FeT_darwin_3day', 'PO4_darwin_3day'], 
#                 '2007-01-01', 
#                 '2008-11-10', 
#                 -90, 
#                 90, 
#                 -180, 
#                 180, 
#                 0, 
#                 5, 
#                 4, 
#                 0.5, 
#                 0.5, 
#                 5,
#                 method='spearman', exportDataFlag=True, show=True
#                 )

# print correlation values
# print(go.z)
# print(go.x)
# print(go.y)
# go.width = 300
# go.height = 300
# go.render()