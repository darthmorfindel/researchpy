#!/usr/bin/env python

# This script plots data from twos csv files of LFM output generated by Paraview.
# The reason for the two files is the calculator/filter system of Paraview -- 
# I should fix my default state to calculate the currents from BnT instead of B_Tesla.
# EDITS NEEDED: CAN/SHOULD I GET THE VECTOR COMPONENTS
# ON ONE PLOT? SOUNDS A BIT COMPLICATED BUT I COULD PROBABLY DO IT.

import pandas as pd
import matplotlib.pyplot as plt
import sys
from datetime import datetime, timedelta
from matplotlib import dates
from matplotlib.ticker import AutoMinorLocator

plt.style.use('dredger_default')

# reading solar wind data into dataframes and then joining

BnT_file = sys.argv[1]
df_nT = pd.read_csv(BnT_file,usecols=[0,1,2,3,4,5,6,7,19,20,21],header=0,
                 names=['Bx (nT)','By (nT)','Bz (nT)','Density\n(n/cm3)',
                 'Sound Speed\n(cm/s)','Vx (cm/s)','Vy (cm/s)','Vz (cm/s)','X (Re)','Y (Re)','Z (Re)'],engine='python')
x_pos = df_nT.iat[1,8]
y_pos = df_nT.iat[1,9]
z_pos = df_nT.iat[1,10]
position = 'Probe Position in Re: ({},{},{})'.format(x_pos,y_pos,z_pos)
df_nT.drop(columns=['X (Re)','Y (Re)','Z (Re)'],inplace=True)
# SORT OUT THE UNITS FOR THE CURRENTS

BT_file = sys.argv[2]
df_T = pd.read_csv(BT_file,usecols=[0,1,2],header=0,engine='python',
                   names=['Jx','Jy','Jz'])

df = pd.merge(df_nT,df_T,right_index=True,left_index=True)

# getting times for plotting; CHANGE MANUALLY

start = datetime(2015,11,13,12,50,00)
times = [start]
for i in range(1,21):
    last_time = times[i-1]
    this_time = last_time + timedelta(minutes=1)
    times.append(this_time)
df['Time'] = times

# plotting the desired variables

title = 'LFM Output Across Bow Shock\n {}'.format(position)
axs = df.plot(kind='line',x='Time',y=['Bx (nT)','By (nT)','Bz (nT)','Density\n(n/cm3)',
              'Sound Speed\n(cm/s)','Vx (cm/s)','Vy (cm/s)','Vz (cm/s)','Jx','Jy','Jz'],
              subplots=True,grid=False,layout=(11,1),
              sharex=True,sharey=False,legend=False,title=title,
              figsize=(6,13),color='k',linewidth=0.75)
for ax in axs.flat:
    h,l = ax.get_legend_handles_labels()
    ax.set(ylabel=l[0])
    ax.xaxis.set_minor_locator(AutoMinorLocator())

plt.subplots_adjust(top=0.9,bottom=0.1,hspace=0)

plt.savefig("lfmoutput_across_bowshock_MMS_2.png") # CHANGE MANUALLY