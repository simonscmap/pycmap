import pycmap

cmap = pycmap.API('4f101ed0-1f13-41a5-ab7d-2c11a405a326')
cmap = pycmap.API('19e91d80-ae64-11e9-8f77-f3e8f5c1f730', vizEngine='plotly')





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
# print(df)


# df = cmap.has_field('tblPisces_NRT', 'O2')
# print(df)


# df = cmap.head('tblAMT13_Chisholm')
# print(df)


# df = cmap.columns('tblAMT13_Chisholm')
# print(df)


# df = cmap.cruises()
# print(df)



# df = cmap.cruise_bounds('scope_6')
# print(df)


# df = cmap.cruise_trajectory('scope_6')
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




# along = cmap.along_track(
#                         cruise='KOK1606', 
#                         tables=['tblSeaFlow', 'tblSSS_NRT', 'tblCHL_REP'], 
#                         variables=['synecho_abundance', 'sss', 'chl'], 
#                         temporalTolerance=[1, 1, 4], 
#                         latTolerance=[0.1, 0.25, 0.25], 
#                         lonTolerance=[0.1, 0.25, 0.25], 
#                         depthTolerance=5
#                         )
# along.to_csv('along.csv')





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

# # table = ['tblPisces_NRT']
# # variable = ['NO3']


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









# ########## plot XY

# from pycmap.viz import plot_xy
# go = plot_xy(
#             xTables=['tblsst_AVHRR_OI_NRT', 'tblPisces_NRT'], 
#             xVars=['sst', 'NO3'],
#             yTables=['tblAltimetry_REP', 'tblsst_AVHRR_OI_NRT'], 
#             yVars=['adt', 'sst'], 
#             dt1='2016-04-20', 
#             dt2='2016-07-20', 
#             lat1=30, 
#             lat2=32, 
#             lon1=-160, 
#             lon2=-158, 
#             depth1=0, 
#             depth2=5, 
#             temporalTolerances=[ 1, 1],
#             latTolerances=[0.125, 0.125],
#             lonTolerances=[0.125, 0.125],
#             depthTolerances=[5, 5],
#             method='spearman', 
#             exportDataFlag=False, 
#             show=True
#             )

# go[0].xlabel = 'salam'
# go[0].title='new title'
# go[0].width = 300
# go[0].height = 300
# go[0].msize=10
# go[0].fillAlpha=0.7
# go[0].render()





# ########## cruise track
# from pycmap.viz import plot_cruise_track
# plot_cruise_track('SCOPE_6')



# st = cmap.subset('uspSpaceTime', 'tblAltimetry_REP', 'adt', '2016-04-30', '2016-07-30', 30, 32, -160, -158, 0, 10)












#### corr plot
# from pycmap.viz import plot_corr_map

# # grad1
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
                
# # flombaum
# go = plot_corr_map(
#                 'tblFlombaum', 
#                 # 'prochlorococcus_abundance_flombaum',
#                 'synechococcus_abundance_flombaum',
#                 # ['tblCHL_REP', 'tblSST_AVHRR_OI_NRT', 'tblAltimetry_REP', 'tblDarwin_Nutrient_3day', 'tblDarwin_Nutrient_3day'], 
#                 # ['chl', 'sst', 'sla', 'FeT_darwin_3day', 'PO4_darwin_3day'], 
#                 ['tblDarwin_Nutrient_3day'], 
#                 ['FeT_darwin_3day'], 
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
















########## ExtraTrees

# from pycmap.supervised import ExtraTrees, RandomForest
# from pycmap.clean import Clean




# # df = cmap.along_track(
# #                      cruise='KOK1606', 
# #                      tables=['tblSeaFlow', 'tblSST_AVHRR_OI_NRT', 'tblSSS_NRT'], 
# #                      variables=['synecho_abundance', 'sst', 'sss'], 
# #                      depth1=0,
# #                      depth2=5,
# #                      temporalTolerance=[0, 1, 1],
# #                      latTolerance=[0, 0.125, 0.125], 
# #                      lonTolerance=[0, 0.125, 0.125], 
# #                      depthTolerance=5
# #                      )


# df = cmap.along_track(
#                      cruise='KOK1606', 
#                      tables=['tblSeaFlow'], 
#                      variables=['synecho_abundance'], 
#                      depth1=0,
#                      depth2=5,
#                      temporalTolerance=[0],
#                      latTolerance=[0], 
#                      lonTolerance=[0], 
#                      depthTolerance=5
#                      )


# df = Clean(df).remove_nan_time_std()

# model = RandomForest(df, 'synecho_abundance')
# model.learn()
# model.plot_feature_importance()
# model.report()





from pycmap.annotatedHeatmap import AnnotatedHeatmap
from pycmap.clean import Clean
import pandas as pd

def plot_corr_matrix(df, cruise):
    corr = df.corr(method='spearman')
    go = AnnotatedHeatmap().graph_obj()        
    go.x = list(corr.columns)
    go.y = list(corr.columns)
    go.z = corr.values
    go.cmap = 'coolwarm' 
    go.vmin = -1
    go.vmax = 1
    go.variable = 'SeaFlow'
    go.xlabel = ''
    go.ylabel = ''
    go.title = cruise
    go.width = 1500
    go.height = 1500
    go.render()
    
    
cruises = ['Gradients_1', 'Gradients_2', 'KM1712', 'KM1713', 'meso_scope', 'diel']
for cruise in cruises:
    df = pd.read_csv('export/%s.csv' % cruise)
    df = Clean(df).remove_nan_time_std()
    df.drop('year', axis=1, inplace=True) 
    df.drop('month', axis=1, inplace=True) 
    plot_corr_matrix(df, cruise)