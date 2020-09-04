#!/usr/bin/env python

# This script takes the magnetic field and plasma parameters required to
# run LFM from the two relevant ACE files and uses those to replace the 
# data in an OMNI file. Outputs a fake OMNI file for use by solarWind.py
# after putting a flat time-shift on the ACE data.

import pandas as pd
import sys
import numpy as np
from datetime import timedelta

# read in the ACE data

ACE_mag_file = sys.argv[1]
ACE_plasma_file = sys.argv[2]
df_mag = pd.read_csv(ACE_mag_file,delim_whitespace=True,skiprows=62,skipfooter=3,
                   header=None,names=['Y/M/D','H/m/s/ms','Bx_GSE','By_GSE','Bz_GSE'],engine='python')
df_plasma = pd.read_csv(ACE_plasma_file,delim_whitespace=True,skiprows=70,skipfooter=3,usecols=[0,1,2,3,4,5,6],
                   header=None,names=['Y/M/D','H/m/s/ms','H_density','H_temp_radial','Vx_GSE','Vy_GSE','Vz_GSE'],engine='python')
df_plasma.replace(to_replace=-1.00000E+31, value=np.nan, inplace=True)

# change the indices of both dataframes to datetime objects
df_mag['Datetime'] = pd.to_datetime(df_mag['Y/M/D'] + ' ' + df_mag['H/m/s/ms'],infer_datetime_format=True,unit='ns')
df_mag['Datetime'] = df_mag['Datetime'] + timedelta(minutes=62) # time-shifting the mag data
df_plasma['Datetime'] = pd.to_datetime(df_plasma['Y/M/D'] + ' ' + df_plasma['H/m/s/ms'],infer_datetime_format=True,unit='ns')
df_plasma['Datetime'] = df_plasma['Datetime'] + timedelta(minutes=62)  # time-shifting the plasma data 
df_plasma['Datetime'] = df_plasma['Datetime'] - timedelta(seconds=22) # adjusting to match the mag data times
datetime_index1 = pd.DatetimeIndex(df_mag['Datetime'].values)
datetime_index2 = pd.DatetimeIndex(df_plasma['Datetime'].values)
df_mag = df_mag.set_index(datetime_index1)
df_plasma = df_plasma.set_index(datetime_index2)
df_mag.drop(columns=['Y/M/D','H/m/s/ms'],inplace=True)
df_plasma.drop(columns=['Y/M/D','H/m/s/ms','Datetime'],inplace=True)
df_mag = df_mag.round(3)

# changing the time cadence of both dataframes to match OMNI

df_mag = df_mag.resample('2S',closed='left').asfreq()
pd.to_datetime(pd.to_numeric(df_mag.Datetime).interpolate())
df_plasma = df_plasma.resample('2S',closed='left').asfreq()
df_mag = df_mag.interpolate()
df_plasma = df_plasma.interpolate()

df_mag = df_mag.resample('60S',closed='left').asfreq()
df_mag = df_mag.fillna(method='ffill')
df_plasma = df_plasma.resample('60S',closed='left').asfreq()
df_plasma = df_plasma.fillna(method='bfill')

# join the two dataframes into a single dataframe, order and space columns like OMNI

ACE_df = df_mag.join(df_plasma)
# ACE_df = ACE_df[['Bx_GSE','By_GSE','Bz_GSE','Vx_GSE','Vy_GSE','Vz_GSE','H_density','H_temp_radial']]
ACE_df = ACE_df[['Datetime','Bx_GSE','By_GSE','Bz_GSE','Vx_GSE','Vy_GSE','Vz_GSE','H_density','H_temp_radial']]
ACE_df = ACE_df.round(3)
datetime_list = ACE_df['Datetime'].to_list()
list_range = range(len(datetime_list))
for i in list_range:
    if i > 0:
        previous = datetime_list[i-1]
        datetime_list[i] = previous + timedelta(minutes=1)
    else:
        None
ACE_df['Datetime'] = datetime_list
ACE_df['Datetime'] = ACE_df['Datetime'].dt.strftime('%d-%m-%Y %H:%M:%S.%f')
new_lines = ACE_df.to_string(col_space=14,justify='right',header=False,index=False)

# read an OMNI file to get the proper format

real_OMNI = sys.argv[3]
OMNI_name = real_OMNI[:-4]
with open(real_OMNI, 'r') as data_in: # opening file, making it a Python object
    lines = data_in.readlines() # making the contents a list of strings
    header = lines[:72]
    footer = lines[-3:]

# finally, print ACE data as new "OMNI" file

new_OMNI = open(OMNI_name + '_ACE.txt','w')
new_OMNI.writelines(header)
new_OMNI.write(new_lines)
new_OMNI.write('\n')
new_OMNI.writelines(footer)
new_OMNI.close()

# optional section for pre-checking the ACE data

check_ACE_df = open('check_ACE_df.txt','w')
# df_mag.to_csv(check_ACE_df)
# df_plasma.to_csv(check_ACE_df)
ACE_df.to_csv(check_ACE_df)
check_ACE_df.close()
