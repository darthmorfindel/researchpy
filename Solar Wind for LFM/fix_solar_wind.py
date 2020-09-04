#!/usr/bin/env python

# This script takes solar wind ion density from THEMIS, time-shifted
# to the ACE location, smoothes out any gaps, and then resamples it 
# to make the cadence match with that of ACE. It next replaces the 
# ACE fill density with the THEMIS density and returns a new ACE file
# for use in LFM.

import sys
import pandas as pd
import numpy as np

# reading and cleaning up THEMIS data

THEMIS_file = sys.argv[1]
THdf = pd.read_csv(THEMIS_file,delim_whitespace=True,skiprows=137,skipfooter=3,
                   header=None,names=['Y/M/D','H/m/s/ms','Density'],engine='python')
THdf.replace(to_replace=-1.00000E+31, value=np.nan, inplace=True)
THdf['Datetime'] = pd.to_datetime(THdf['Y/M/D'] + ' ' + THdf['H/m/s/ms'], infer_datetime_format=True)
THdf['Datetime'] = THdf.Datetime.dt.round('1s')
datetime_index = pd.DatetimeIndex(THdf['Datetime'].values)
THdf = THdf.set_index(datetime_index)
THdf.drop(columns=['Y/M/D','H/m/s/ms','Datetime'],inplace=True)
THdf = THdf.resample('1S').asfreq()
THdf = THdf.interpolate()
THdf = THdf.resample('64S',base=16).asfreq()
THdf = THdf.fillna(method='bfill')
THdf = THdf.round(2)
shape = THdf.shape
THdf = THdf.set_index(np.arange(0,shape[0]))

# reading ACE data

ACE_file = sys.argv[2]
new_lines = []
with open(ACE_file, 'r') as data_in: # opening file, making it a Python object
    lines = data_in.readlines() # making the contents a list of strings
    header = lines[:70]
    footer = lines[-3:]
    end_of_data = len(lines)-3
    data_range = range(70,end_of_data) # actual data in file
    for i in data_range:
        current_line = lines[i]
        THEMIS_index = i - 70
        new_line = current_line[0:25] + '{:2f}'.format(THdf.iat[THEMIS_index,0]) + current_line[37:]
        new_lines.append(new_line)
    
new_ACE_file = open('AC_H0_SWE_updated.txt','w')
new_ACE_file.writelines(header)
new_ACE_file.writelines(new_lines)
new_ACE_file.writelines(footer)
new_ACE_file.close()
