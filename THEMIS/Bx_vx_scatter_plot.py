#!/usr/bin/env python

# This script plots the x-components of the ion velocities and magnetic field
# seen by a THEMIS spacecraft as a scatter plot to see any correlation.
# It reads in the data from two files, gets the two columns needed and converts
# them into lists, then plots the two relevant variables in a scatter plot.
# The slight time discrepancy between the two datasets is ignored as it is within
# the temporal uncertainty (three-second data).

import pandas as pd
import matplotlib.pyplot as plt
import sys
import numpy as np
from matplotlib import dates
from matplotlib import rc
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter, AutoMinorLocator)

rc('font',**{'family':'serif','serif':['Times']})
rc('text', usetex=True)

# reading THEMIS MOM data into a dataframe -- skiprows and/or footer gives the correct data range

FGM_file = sys.argv[1]
dfB = pd.read_csv(FGM_file,delim_whitespace=True,skiprows=584,skipfooter=3,
                   header=None,names=['D/M/Y','H/m/s/ms','Bx GSM (nT)','By GSM (nT)','Bz GSM (nT)'],engine='python')
dfB.interpolate(method='linear')
MOM_file = sys.argv[2]
dfv = pd.read_csv(MOM_file,delim_whitespace=True,skiprows=84,skipfooter=3,
                   header=None,names=['D/M/Y','H/m/s/ms','Vx GSM (km/s)','Vy GSM (km/s)','Vz GSM (km/s)'],engine='python')
dfv.interpolate(method='linear')

# converting the two relevant variables into lists for plotting

Bx_list = dfB['Bx GSM (nT)'].to_list()
vx_list = dfv['Vx GSM (km/s)'].to_list()

# plotting the data 

fig = plt.figure()
ax = fig.add_subplot(111)

ax.xaxis.set_minor_locator(AutoMinorLocator())
ax.yaxis.set_minor_locator(AutoMinorLocator())
ax.tick_params(which='both',direction='inout')
ax.tick_params(which='major',length=8)
ax.tick_params(which='minor',length=4)
ax.set_xlabel('B$_x$ GSM (km/s)',fontsize=8)
ax.set_ylabel('V$_x$ GSM (km/s)',fontsize=8)

ax.scatter(Bx_list,vx_list,s=2,c='k')
plt.title('B$_x$ vs. V$_x$')
plt.savefig('THB_L2_Bxvx_20080531.png') # CHANGE MANUALLY
plt.show()
