#!/usr/bin/env python

# This script takes the magnetic field and plasma parameters required to
# run LFM from the two relevant ACE files (can be in GSM instead) and 
# plots them OMNI style after putting a flat time-shift on the ACE data.

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
df_mag['Datetime'] = pd.to_datetime(df_mag['Y/M/D'] + ' ' + df_mag['H/m/s/ms'],infer_datetime_format=True)
df_mag['Datetime'] = df_mag['Datetime'] + timedelta(minutes=62) # time-shifting the mag data
df_plasma['Datetime'] = pd.to_datetime(df_plasma['Y/M/D'] + ' ' + df_plasma['H/m/s/ms'],infer_datetime_format=True)
df_plasma['Datetime'] = df_plasma['Datetime'] + timedelta(minutes=62)  # time-shifting the plasma data 
df_plasma['Datetime'] = df_plasma['Datetime'] - timedelta(seconds=22) # adjusting to match the mag data times
datetime_index1 = pd.DatetimeIndex(df_mag['Datetime'].values)
datetime_index2 = pd.DatetimeIndex(df_plasma['Datetime'].values)
df_mag = df_mag.set_index(datetime_index1)
df_plasma = df_plasma.set_index(datetime_index2)
df_mag.drop(columns=['Y/M/D','H/m/s/ms'],inplace=True)
df_plasma.drop(columns=['Y/M/D','H/m/s/ms','Datetime'],inplace=True)
df_mag = df_mag.round(3)

# join the two dataframes into a single dataframe, order and space columns like OMNI

ACE_df = df_mag.join(df_plasma)
ACE_df = ACE_df[['Datetime','Bx_GSE','By_GSE','Bz_GSE','Vx_GSE','Vy_GSE','Vz_GSE','H_density','H_temp_radial']]

check_ACE_df = open('check_ACEtogether_df.txt','w')
df_mag.to_csv(check_ACE_df)
df_plasma.to_csv(check_ACE_df)
# ACE_df.to_csv(check_ACE_df)
check_ACE_df.close()
