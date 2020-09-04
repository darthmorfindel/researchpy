#!/usr/bin/env python

# This script plots the field-aligned currents from AMPERE.
# It outputs a series of pngs for each timestamp for stitching
# together into a movie. The DMSP track for each time is plotted
# over the AMPERE currents.

# Inputs: sys.argv[1] is the AMPERE file, sys.argv[2] is the DMSP file.

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import sys

# trying to fix the pyproj error...

# import os
# os.environ['PROJ_LIB']='/home/pdredger/anaconda3/share'

# importing the AMPERE data into a DataFrame

AMPERE_file = sys.argv[1]
Adf = pd.read_csv(AMPERE_file,header=None,names=['Time(UTC)','GeoLon','GeoLat','Jr(micro-A/m^2)'],
                  usecols=[0,3,4,5],delim_whitespace=True,skiprows=2,engine='python')
Adf['Time(UTC)'] = pd.to_datetime(Adf['Time(UTC)'],infer_datetime_format=True)
start_time = Adf['Time(UTC)'].iloc[0]
end_time = Adf['Time(UTC)'].iloc[-1]

# importing the DMSP data into a DataFrame

DMSP_file = sys.argv[2]
Ddf = pd.read_csv(DMSP_file,delim_whitespace=True,header=0,engine='python')
Ddf['Datetime'] = pd.to_datetime(Ddf['YEAR'] + Ddf['MONTH'] + Ddf['DAY']
                                 + Ddf['HOUR'] + Ddf['MIN'] + Ddf['SEC'],
                                 infer_datetime_format=True)
Ddf.drop(columns=['YEAR','MONTH','DAY','HOUR','MIN','SEC'],inplace=True)

# splitting the AMPERE data into dfs for each timestamp and plotting each

for time in pd.date_range(start_time,end_time,freq='T'):
    condition1 = Adf['Time(UTC)'] == time
    condition2 = Ddf['Datetime'] == time
    temp_Adf = Adf.loc[condition1]
    temp_Ddf = Ddf.loc[condition2]
    
    # making the sub-dfs into gdfs
    
    temp_Agdf = gpd.GeoDataFrame(temp_Adf,crs="EPSG:4326",
                geometry=gpd.points_from_xy(temp_Adf.GeoLon,temp_Adf.GeoLat))
    # temp_Agdf = temp_Agdf.drop(['GeoLon','GeoLat'],inplace=True)
    temp_Dgdf = gpd.GeoDataFrame(temp_Ddf,crs="EPSG:3031",
                geometry=gpd.points_from_xy(temp_Ddf.GLON,temp_Ddf.GDLAT))
    # temp_Dgdf = temp_Dgdf.drop(['GLON','GDLAT'],inplace=True)
    
    # plotting the background
    
    fig = plt.figure(figsize=(8,8))
    ax = plt.subplot(111,projection=ccrs.SouthPolarStereo())
    ax.set_extent([-180,180,-40,-90],crs=ccrs.PlateCarree())
    # ax.stock_img()
    ax.coastlines()
    plt.suptitle(time)

    # plotting the AMPERE and DMSP data
    
    # cpyversion = ccrs.SouthPolarStereo()
    # cpy_proj4 = cpyversion.proj4_init
    temp_Agdf = temp_Agdf.to_crs(epsg=4326) # WGS84
    temp_Agdf.plot(column='Jr(micro-A/m^2)',ax=ax,legend=True)
    # ax.add_geometries(temp_Agdf.geometry,crs=ccrs.PlateCarree(),edgecolor='blue')
    plt.show()

    sys.exit()


# websites I was using:
# https://github.com/pyproj4/pyproj/issues/134
# https://matplotlib.org/3.1.0/tutorials/colors/colormaps.html
# https://geopandas.org/projections.html
# https://geopandas.readthedocs.io/en/latest/gallery/cartopy_convert.html
# https://www.reddit.com/r/learnpython/comments/a9vof0/there_is_a_corepyx_file_in_the_package_folder_but/
# https://proj.org/install.html
# https://github.com/pyproj4/pyproj
