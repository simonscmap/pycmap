import pycmap

cmap = pycmap.API('4f101ed0-1f13-41a5-ab7d-2c11a405a326')
cmap = pycmap.API('90d862e0-8d49-11e9-8d22-0f5810db0206', vizEngine='bokeh')





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
# hist = plot_hist(table, variable, '2016-04-30', '2016-04-30', 10, 70, -180, -80, 0, 0.5, exportDataFlag)

# hist.pdf=True
# hist.xlabel = 'salam'
# hist.title='new title'
# hist.width = 300
# hist.height = 300
# hist.render()







########## plot map

from pycmap.viz import plot_map

table = ['tblsst_AVHRR_OI_NRT']
variable = ['sst']
exportDataFlag = True
hist = plot_map(table, variable, '2016-04-30', '2016-04-30', 10, 70, -180, -80, 0, 0.5, exportDataFlag)

hist[0].xlabel = 'salam'
hist[0].title='new title'
hist[0].width = 300
hist[0].height = 300
hist[0].render()