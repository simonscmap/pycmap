import numpy as np
import pandas as pd
from scipy import stats
from pycmap.trend import Trend
from pycmap.annotatedHeatmap import AnnotatedHeatmap
from pycmap.clean import Clean
from pycmap.common import halt


def all_cruises():
    # cruises = list(api.cruises().Nickname)[:-21]   # remove AMT cruises
    cruises = [ 'TN243',
                'TN248',
                'TN250',
                'TN252',
                'TN257',
                'TN260',
                'TN264-265',
                'Tokyo_1',
                'Tokyo_2',
                'TN268',
                'CN11ID',
                'TN270',
                'TN271',
                'Tokyo_3',
                'Tokyo_4',
                'TN280',
                'CN12ID',
                'TN291',
                'TN292',
                'KN210-04',
                'KM1314',
                'CN13ID',
                'KM1427',
                'KM1502',
                'KM1508',
                'KM1510',
                'KM1512',
                'KM1513',
                'KOK1512',
                'KOK1515',
                'KM1518',
                'KM1601',
                'KM1602',
                'KM1603',
                'KOK1604',
                'KOK1606',
                'KOK1607',
                'KOK1608',
                'KOK1609',
                'MGL1704',
                'KM1708',
                'KM1709',
                'KM1712',
                'KM1713',
                'KM1717',
                'KM1802',
                'KM1805',
                'FK180310-1',
                'FK180310-2',
                'KOK1801',
                'KOK1803',
                'KOK1804',
                'KOK1805',
                'KOK1806',
                'KM1821',
                'KM1823',
                'RR1814',
                'RR1815',
                'KM1901',
                'KM1903',
                'KM1906',
                'KM1909']
                
    cruises.remove('Tokyo_1')
    cruises.remove('Tokyo_2')
    cruises.remove('Tokyo_3')
    cruises.remove('Tokyo_4')
    cruises.remove('KOK1512')
    return cruises


def open_ocean():
    # return ['RR1814', 'RR1815', 'MGL1704', 'KOK1606', 'KM1713', 'KM1712', 'KM1502', 'KM1314', 'KN210-04', 'TN292']
    return ['MGL1704', 'KOK1606', 'KM1713', 'KM1712']


def compile(batch):
    if batch == 'all':
        cruises = all_cruises()
    elif batch == 'open':    
        cruises = open_ocean()
    else:
        halt('invalid cruise batch name!')    

    print('compiling colocalized cruise files ... ')
    df = pd.DataFrame({})
    for index, cruise in enumerate(cruises):
        print('%d: %s' % (index, cruise))
        data = pd.read_csv('export/%s.csv' % cruise)
        if len(df) < 1:
            df = data
        else:
            df = pd.concat([df, data], ignore_index=True)    
        # data.to_csv('export/%s.csv' % cruise, index=False)
    # df.to_csv('export/sfCompile.csv', index=False)      
    return df


def plot_spatial(df):
    import matplotlib.pyplot as plt
    plt.plot(df.lon, df.lat, marker='o', lw=0, alpha=.05, ms=1)
    plt.xlabel, plt.ylabel = 'lon', 'lat'
    plt.show()


def correlation(df, method='spearman'):
    corr = df.corr(method=method)
    corr.reset_index(inplace=True)
    corr.to_csv('export/corr.csv', index=False)
    return corr


def plot_corr(corr, col):
    corr = corr.sort_values(by=col, ascending=False)
    go = Trend(pd.DataFrame({}), col).graph_obj()
    go.x = list(corr['index'])
    go.y = list(corr[col])
    go.title = col
    go.timeSeries = False
    go.ylabel = 'Corr. Coeff. '
    go.width = 1400
    go.height = 700
    go.render()


def plot_corr_matrix(corr, title='title'):
    if 'index' in corr.columns:
        c = corr.drop('index', axis=1, inplace=False)
    go = AnnotatedHeatmap().graph_obj()        
    go.x = list(c.columns)
    go.y = list(c.columns)
    go.z = c.values
    go.cmap = 'coolwarm' 
    go.vmin = -1
    go.vmax = 1
    go.variable = 'SF'
    go.xlabel = ''
    go.ylabel = ''
    go.title = title
    go.width = 2500
    go.height = 2500
    go.render()


def plot_corr_trend(corr):
    plot_corr(corr, 'prochloro_diameter')
    plot_corr(corr, 'prochloro_abundance')
    plot_corr(corr, 'prochloro_biomass')
    plot_corr(corr, 'synecho_diameter')
    plot_corr(corr, 'synecho_abundance')
    plot_corr(corr, 'synecho_biomass')
    plot_corr(corr, 'picoeuk_diameter')
    plot_corr(corr, 'picoeuk_abundance')
    plot_corr(corr, 'picoeuk_biomass')
    plot_corr(corr, 'total_biomass')

    plot_corr(corr, 'adt')
    plot_corr(corr, 'chl')
    plot_corr(corr, 'sss')
    plot_corr(corr, 'vel')

    plot_corr(corr, 'NO3')
    plot_corr(corr, 'PO4')
    plot_corr(corr, 'O2')
    plot_corr(corr, 'Si')
    plot_corr(corr, 'Fe')
    plot_corr(corr, 'ALK_darwin_clim')
    plot_corr(corr, 'Fe_div_NO3')
    plot_corr(corr, 'Si_div_O2')
    plot_corr(corr, 'Si_div_NO3')
    plot_corr(corr, 'PO4_div_NO3')


def seaflow_nan_to_zero(df):    
    for sp in ['prochloro', 'synecho', 'picoeuk']:
        df['%s_abundance' % sp].fillna(0, inplace=True)
        df['%s_diameter' % sp].fillna(0, inplace=True)
        df['%s_carbon_content' % sp].fillna(0, inplace=True)
        df['%s_biomass' % sp].fillna(0, inplace=True)

        # df['%s_abundance_std' % sp].fillna(0, inplace=True)
        # df['%s_diameter_std' % sp].fillna(0, inplace=True)
        # df['%s_carbon_content_std' % sp].fillna(0, inplace=True)
        # df['%s_biomass_std' % sp].fillna(0, inplace=True)

    df['total_biomass'].fillna(0, inplace=True)
    # df['total_biomass_std'].fillna(0, inplace=True)
    return df


def data_transform(df):
    def power(col):
        shift = df[col].min()
        if shift < 0:
            shift = -shift
        else:
            shift = 0             
        df['%s_2' % col] = df[col] ** 2 
        df['%s_0.5' % col] = df[col] ** 0.5 
#         df['1_%s' % col] = df[col] ** -1 
#         df['log_%s' % col] = stats.boxcox(df[col]+shift+1, lmbda=0) 
        df['boxcox_%s' % col], _ = stats.boxcox(df[col]+shift+1)        




    df = Clean(df).remove_nan_time_std()
    df.drop('year', axis=1, inplace=True) 
    df.drop('month', axis=1, inplace=True)


    # power('sst') 
    # # power('sss') 
    # power('NO3') 
    # power('Fe') 
    df['vel'] = ( (df.ugos ** 2) + (df.vgos ** 2) ) ** 0.5    

    df['Fe_div_NO3'] = df.Fe / df.NO3
    df['Fe_mul_NO3'] = df.Fe * df.NO3

    df['Fe_div_PO4'] = df.Fe / df.PO4
    df['Fe_mul_PO4'] = df.Fe * df.PO4

    df['Fe_div_O2'] = df.Fe / df.O2
    df['Fe_mul_O2'] = df.Fe * df.O2

    df['PO4_div_NO3'] = df.PO4 / df.NO3
    df['PO4_mul_NO3'] = df.PO4 * df.NO3

    df['NO3_div_O2'] = df.NO3 / df.O2
    df['NO3_mul_O2'] = df.NO3 * df.O2

    df['Si_div_NO3'] = df.Si / df.NO3
    df['Si_mul_NO3'] = df.Si * df.NO3

    df['Si_div_Fe'] = df.Si / df.Fe
    df['Si_mul_Fe'] = df.Si * df.Fe

    df['Si_div_O2'] = df.Si / df.O2
    df['Si_mul_O2'] = df.Si * df.O2

    df['Si_div_PO4'] = df.Si / df.PO4
    df['Si_mul_PO4'] = df.Si * df.PO4

    df['O2_div_PO4'] = df.O2 / df.PO4
    df['O2_mul_PO4'] = df.O2 * df.PO4
    # 1/lat?
    return df








# print('loading colocalized data ...')
# df = pd.read_csv('export/sfCompile.csv')
df = compile('open')
print('Number of data points: %d' % len(df))


#############################################################################
df.drop('par', axis=1, inplace=True)
df.drop('par_std', axis=1, inplace=True)
# df.drop('sss', axis=1, inplace=True)
df.drop('sss_std', axis=1, inplace=True)
# df.drop('AOD', axis=1, inplace=True)
df.drop('AOD_std', axis=1, inplace=True)

for col in df.columns:
    if col[-4:] == '_std': df.drop(col, axis=1, inplace=True)   
################ replace missing/nan values of seaflow with zero ################
df = seaflow_nan_to_zero(df)
#################################################################################

#############################################################################


print('**************************')
print('The column with most nan values:')
print(df.count().idxmin())
print('**************************')

print('data transformation ...')
df = data_transform(df)
plot_spatial(df)
print('Number of data points after cleaning/transformation: %d' % len(df))
print('computing correlations ...')

corr = correlation(df, method='spearman')  
plot_corr_matrix(corr, title='SF Compiled')
plot_corr_trend(corr)

