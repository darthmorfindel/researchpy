#!/usr/bin/env python

import sys
import operator
import os
from os.path import join 
import glob
import numpy as np
import datetime
import matplotlib.pyplot as plt
from matplotlib import dates
from matplotlib import rc
from matplotlib.ticker import AutoMinorLocator
from operator import truediv

rc('font',**{'family':'serif','serif':['Times']})
rc('text', usetex=True)

# reading AMPERE file

current_total_north_values = [] # initializing lists for loop
times = []
directory = os.getcwd()
file_locationA = os.path.join(directory, '*.dat') # reading all the files in the directory
filenamesA = sorted(glob.glob(file_locationA))
first_fileA = filenamesA[0] # for naming the plots later
file_date = first_fileA[:-4]
for f in filenamesA:
    with open(f,'r') as data_in:
        lines = data_in.readlines() # making the contents a list of strings
        end_of_data = len(lines)
        data_range = range(1,end_of_data) # actual data in file
        for i in data_range: # looping over only data
            current_linei = lines[i] # picking out one line at a time
            if float(current_linei[21:29])==9999.00: # checking for bad data
                I_total_up_north = np.nan
            else:
                I_total_up_north = float(current_linei[23:29])
            if float(current_linei[29:37])==9999.00:
                I_total_down_north = np.nan
            else:
                I_total_down_north = float(current_linei[30:37])            
            total_current_north = (I_total_up_north + abs(I_total_down_north))/2
            current_total_north_values.append(total_current_north) # list to be plotted
            year = int(current_linei[0:4])
            month = int(current_linei[5:7])
            day = int(current_linei[8:10])
            hour = int(current_linei[11:13])
            minute = int(current_linei[14:16])
            second = int(current_linei[17:19])
            timei_formatted = datetime.datetime(year,month,day,hour,minute,second)
            times.append(timei_formatted)

# reading SuperMAG file

file_locationS = os.path.join(directory, '*supermag.txt')
filenamesS = sorted(glob.glob(file_locationS))
times_S = []
for f in filenamesS:
    file_S = open(f,'r')
    data = np.genfromtxt(file_S, skip_header=105, usecols=(0,1,2,3,4,5,6), missing_values='999999') # putting the data into a numpy array
    for row in data:
        year = int(row[0])
        month = int(row[1])
        day = int(row[2])
        hour = int(row[3])
        minute = int(row[4])
        second = int(row[5])
        timei_formatted = datetime.datetime(year,month,day,hour,minute,second)
        times_S.append(timei_formatted)
    SME = data[:,6]

SME_two_min = [item for index, item in enumerate(SME) if (index + 1) % 2 != 0]

# nT_per_MA = [i/j for i,j in zip(SME, current_total_north_values)]
nT_per_MA = list(map(truediv, SME_two_min, current_total_north_values))

fig1,axs = plt.subplots(3,1,tight_layout=True)
    
# ax1.xaxis.tick_top()
# ax1.xaxis.set_label_position('top')

# subplot for northern total current

axs[0].tick_params(which='both',direction='inout')
axs[0].tick_params(which='major',length=8,right=True)
axs[0].tick_params(which='minor',length=4,right=True)
axs[0].xaxis.set_major_locator(dates.HourLocator(interval=4))
axs[0].xaxis.set_minor_locator(AutoMinorLocator())
axs[0].yaxis.set_minor_locator(AutoMinorLocator())
axs[0].xaxis.set_major_formatter(dates.DateFormatter('%H:%M\n%m/%d'))

# ax1.text(-10,-20, 'B$_y$ vs B$_z$',fontsize=18,bbox={'facecolor':'white', 'alpha':0.5,'pad':10})
axs[0].plot(times, current_total_north_values, c='k',linewidth=0.5)
# axs[0].set_title('North Total')
axs[0].autoscale(axis='x',tight=True)
axs[0].set_ylabel(R'Total Current \textit{(MA)}',fontsize=12)

# subplot for SME

axs[1].tick_params(which='both',direction='inout')
axs[1].tick_params(which='major',length=8,right=True)
axs[1].tick_params(which='minor',length=4,right=True)
axs[1].xaxis.set_major_locator(dates.HourLocator(interval=4))
axs[1].xaxis.set_minor_locator(AutoMinorLocator())
axs[1].yaxis.set_minor_locator(AutoMinorLocator())
axs[1].xaxis.set_major_formatter(dates.DateFormatter('%H:%M\n%m/%d'))
axs[1].plot(times_S, SME, c='b',linewidth=0.5)
# axs[1].set_title('SME')

axs[1].set_ylabel(R'SME \textit{(nT)}',fontsize=12)
axs[1].autoscale(axis='x',tight=True)

# subplot for SME/North Total Current

axs[2].tick_params(which='both',direction='inout')
axs[2].tick_params(which='major',length=8,right=True)
axs[2].tick_params(which='minor',length=4,right=True)
axs[2].xaxis.set_major_locator(dates.HourLocator(interval=4))
axs[2].xaxis.set_minor_locator(AutoMinorLocator())
axs[2].yaxis.set_minor_locator(AutoMinorLocator())
axs[2].xaxis.set_major_formatter(dates.DateFormatter('%H:%M\n%m/%d'))
axs[2].plot(times, nT_per_MA, c='r',linewidth=0.5)
# axs[2].set_title('SME/Current')

axs[2].set_ylabel(R'SME/Current \textit{(nT/MA)}',fontsize=12)
axs[2].autoscale(axis='x',tight=True)

plt.savefig(file_date + '_north_total_current_SME.pdf')
plt.show()
