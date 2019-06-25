import pycmap

cmap = pycmap.API('4f101ed0-1f13-41a5-ab7d-2c11a405a326')
cmap = pycmap.API('90d862e0-8d49-11e9-8d22-0f5810db0206')

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




df = cmap.space_time('tblsst_AVHRR_OI_NRT', 'sst', '2016-04-30', '2016-04-30', 10, 70, -180, -80, 0, 0.5)
print(df)

