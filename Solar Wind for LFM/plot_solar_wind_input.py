#!/usr/bin/env python

# This script plots data from an OMNI file in the format required by 
# pyLTR's solarWind.py

import pandas as pd
import matplotlib.pyplot as plt
import sys
import numpy as np
from matplotlib import dates
from matplotlib import rc
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter, AutoMinorLocator)

rc('font',**{'family':'serif','serif':['Times']})
rc('text', usetex=True)

# reading solar wind data into a dataframe

sw_file = sys.argv[1]
df = pd.read_csv(sw_file,delim_whitespace=True,skiprows=73,skipfooter=3,
                   header=None,names=['D/M/Y','H/m/s/ms','Bx GSE (nT)','By GSE (nT)','Bz GSE (nT)','Vx GSE (km/s)','Vy GSE (km/s)','Vz GSE (km/s)',
                   'Proton Density (n/cc)','Temperature (K)'],engine='python')
df.replace(to_replace=-2.500000e+30, value=np.nan, inplace=True)
df['Datetime'] = pd.to_datetime(df['D/M/Y'] + ' ' + df['H/m/s/ms'],dayfirst=True)
datetime_index = pd.DatetimeIndex(df['Datetime'].values)
df = df.set_index(datetime_index)
df.drop(columns=['D/M/Y','H/m/s/ms','Datetime'],inplace=True)

# plotting the dataframe, basic pandas version

# df.plot(kind='line',subplots=True, grid=True,layout=(8,1),sharex=True,sharey=False,legend=True,
#         title='Propagated Solar Wind from ACE',figsize=(15,15))
        
# plotting the dataframe, upgraded mpl version

fig,axs = plt.subplots(8,1,sharex=True,figsize=(10,12))
fig.suptitle('Propagated Solar Wind from ACE',fontsize=14)
for i, c in enumerate(df.columns):
    df[c].plot(kind='line',ax=axs[i],legend=False,color='k',linewidth=0.75)
    axs[i].tick_params(which='both',direction='in')
    axs[i].tick_params(axis='x',which='major',length=4,top=True)
    axs[i].tick_params(axis='x',which='minor',length=2,top=True)
    axs[i].tick_params(axis='y',which='major',length=8,right=True)
    axs[i].tick_params(axis='y',which='minor',length=4,right=True)
    axs[i].xaxis.set_minor_locator(AutoMinorLocator())
    axs[i].yaxis.set_minor_locator(AutoMinorLocator())
    axs[i].autoscale(axis='x',tight=True)
    axs[i].set_ylabel(c,fontsize=10)

plt.subplots_adjust(top=0.9,bottom=0.1,hspace=0)
plt.savefig("OMNI_ACE_20151113.png") # CHANGE MANUALLY

# optional section to check the dataframe before plotting

# check_df = open('check_df.txt','w')
# df.to_csv(check_df)
# check_df.close()
