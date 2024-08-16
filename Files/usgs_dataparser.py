import numpy as np
import pandas as pd

path = r'F:\Hazard_Article_Sum2024\Files\USGS_Turkiye_Deprem_Listesi.csv'
def usgs_dataparser(path):
    pd.set_option("expand_frame_repr", True)
    pd.set_option("display.max_columns", 10)
    pd.set_option("large_repr", "truncate")
    
    catalogdf = pd.read_csv(path, sep=',', quotechar='"',encoding='utf-8')
    
    print('Raw earthquake catalogue from USGS')
    display(catalogdf.loc[catalogdf['magType'] == 'm'])
    
    catalogdf['time'] = [pd.Timestamp(timestamp) for timestamp in catalogdf['time']]
    catalogdf['year'] = [pd.Timestamp(timestamp).year for timestamp in catalogdf['time']]
    catalogdf['month'] = [pd.Timestamp(timestamp).month for timestamp in catalogdf['time']]
    catalogdf['day'] = [pd.Timestamp(timestamp).day for timestamp in catalogdf['time']]
    catalogdf['date_decimal']= catalogdf['year']+((catalogdf['month']-1)/12)+((catalogdf['day']-1)/365)
    
    catalogdf = catalogdf[['date_decimal','year','month','day','latitude','longitude','depth','mag','magType','place']]

    #['mwr' 'mb' 'mww' 'ml' 'mwb' 'mw' 'mwc' 'mblg' 'm' 'md' 'ms']    
    print(catalogdf['magType'].unique())
    catalogdf['magType'] = catalogdf['magType'].str[:2].str.lower()
    #['mw' 'mb' 'ml' 'm' 'md' 'ms']        
    print(catalogdf['magType'].unique())
    
    
    # unifying magnitudes
    catalogdf.loc[catalogdf.query('magType == "mw" or magType == "m"').index,'mag']= [MW for MW in catalogdf.query('magType == "mw" or magType == "m"')['mag']]
    catalogdf.loc[catalogdf.query('magType == "ms" and mag < 5.5').index,'mag']= [0.5716*ms1+2.4980 for ms1 in catalogdf.query('magType == "ms" and mag < 5.5')['mag']]
    catalogdf.loc[catalogdf.query('magType == "ms" and mag >= 5.5').index,'mag']= [0.8126*ms2+1.1723 for ms2 in catalogdf.query('magType == "ms" and mag >= 5.5')['mag']]
    catalogdf.loc[catalogdf.query('magType == "mb"').index,'mag']= [1.0319*mb+0.0223 for mb in catalogdf.query('magType == "mb"')['mag']]
    catalogdf.loc[catalogdf.query('magType == "md"').index,'mag']= [0.7947*md+1.3420 for md in catalogdf.query('magType == "md"')['mag']]
    catalogdf.loc[catalogdf.query('magType == "ml"').index,'mag']= [0.8095*ml+1.3003 for ml in catalogdf.query('magType == "ml"')['mag']]
    catalogdf['mag'] = np.round(catalogdf['mag'],2)
    
    # dropping unnecessary columns
    #catalogdf = catalogdf[['Date','year','month','day','hour','minute','second','Latitude','Longitude','Depth','magnitude','Location','Type']]
    #catalogdf['Date_decimal']= catalogdf['year']+((catalogdf['month']-1)/12)+((catalogdf['day']-1)/365)
    
    
    print('Earthquake catalogue after manipulation')
    
    catalogdf.insert(loc=0,column='ID',value=(catalogdf.index.to_list()))
    catalogdf.drop(['magType'],axis=1,inplace=True)
    display(catalogdf.sort_values(by=['date_decimal'], ascending=False))
    return catalogdf

catalogdf = usgs_data(path)
catalogdf