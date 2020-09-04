#!/usr/bin/env python

# This script plots the x- and y-components of the ion velocities 
# seen by a THEMIS spacecraft as a scatter plot to see any correlation.

import pandas as pd
import matplotlib.pyplot as plt
import sys
import numpy as np
from matplotlib import dates
from matplotlib import rc
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter, AutoMinorLocator)

rc('font',**{'family':'serif','serif':['Times']})
rc('text', usetex=True)

# reading THEMIS data into a dataframe -- skiprows and/or footer gives the correct data range

sw_file = sys.argv[1]
df = pd.read_csv(sw_file,delim_whitespace=True,skiprows=84,skipfooter=3,
                   header=None,names=['D/M/Y','H/m/s/ms','Vx GSM (km/s)','Vy GSM (km/s)','Vz GSM (km/s)'],engine='python')
df['Datetime'] = pd.to_datetime(df['D/M/Y'] + ' ' + df['H/m/s/ms'],dayfirst=True)
datetime_index = pd.DatetimeIndex(df['Datetime'].values)
df = df.set_index(datetime_index)
df.drop(columns=['D/M/Y','H/m/s/ms','Datetime'],inplace=True)

# plotting the data -- ADJUST COLOR/SIZE/TICKS 

fig = plt.figure()
ax = fig.add_subplot(111)
df.plot(kind='scatter',x='Vx GSM (km/s)',y='Vy GSM (km/s)',ax=ax,s=2,c='k')
ax.xaxis.set_minor_locator(AutoMinorLocator())
ax.yaxis.set_minor_locator(AutoMinorLocator())
ax.tick_params(which='both',direction='inout')
ax.tick_params(which='major',length=8)
ax.tick_params(which='minor',length=4)
ax.set_xlabel(R'V$_x$ GSM (km/s)',fontsize=8)
ax.set_ylabel(R'V$_y$ GSM (km/s)',fontsize=8)
plt.title('V$_y$ vs. V$_x$')
plt.savefig('THB_L2_MOM_vxvy_20080531.png')
plt.show()
