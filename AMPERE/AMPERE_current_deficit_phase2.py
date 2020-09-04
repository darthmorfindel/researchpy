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
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter, AutoMinorLocator)

rc('font',**{'family':'serif','serif':['Times']})
rc('text', usetex=True)

current_deficit_north_values = [] # initializing lists for loop
norm_deficit_north_values = []
current_deficit_south_values = []
norm_deficit_south_values = []
times = []
directory = os.getcwd()
file_location = os.path.join(directory, '*.dat') # reading all the files in the directory
filenames = sorted(glob.glob(file_location))
first_file = filenames[0] # for naming the plots later
file_date = first_file[:-4]
last_file = filenames[-1]
for f in filenames:
    with open(f,'r') as data_in:
        lines = data_in.readlines() # making the contents a list of strings
        end_of_data = len(lines) # skipping last three lines of file
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
            if float(current_linei[69:77])==9999.00:
                I_total_up_south = np.nan
            else:
                I_total_up_south = float(current_linei[71:77])
            if float(current_linei[77:86])==9999.00:
                I_total_down_south = np.nan
            else:
                I_total_down_south = float(current_linei[78:85])
            I_deficit_north = I_total_up_north + I_total_down_north
            I_deficit_south = I_total_up_south + I_total_down_south
            current_deficit_north_values.append(I_deficit_north) # list to be plotted
            current_deficit_south_values.append(I_deficit_south)
            I_total_current_north = (I_total_up_north + abs(I_total_down_north))/2
            I_total_current_south = (I_total_up_south + abs(I_total_down_south))/2
            I_norm_deficit_north = I_deficit_north/I_total_current_north
            I_norm_deficit_south = I_deficit_south/I_total_current_south
            norm_deficit_north_values.append(I_norm_deficit_north)
            norm_deficit_south_values.append(I_norm_deficit_south)
            year = int(current_linei[0:4])
            month = int(current_linei[5:7])
            day = int(current_linei[8:10])
            hour = int(current_linei[11:13])
            minute = int(current_linei[14:16])
            second = int(current_linei[17:19])
            timei_formatted = datetime.datetime(year,month,day,hour,minute,second)
            times.append(timei_formatted)

NvsS = plt.figure()
axa = NvsS.add_subplot(111)
axa.set_aspect('equal')
axa.tick_params(which='both',direction='inout')
axa.tick_params(which='major',length=8,right=True)
axa.tick_params(which='minor',length=4,right=True)
axa.xaxis.set_major_locator(MultipleLocator(0.5))
axa.yaxis.set_major_locator(MultipleLocator(0.5))
axa.scatter(current_deficit_south_values,current_deficit_north_values,s=2,c='k')
axa.set_xlabel('South Difference (MA)')
axa.set_ylabel('North Difference (MA)')
plt.tight_layout()
plt.savefig('northdiff_vs_southdiff_' + first_file[-12:-4] + '-' + last_file[-12:-4]+ '.png')

NvsS_norm = plt.figure()
axb = NvsS_norm.add_subplot(111)
axb.set_aspect('equal')
axb.tick_params(which='both',direction='inout')
axb.tick_params(which='major',length=8,right=True)
axb.tick_params(which='minor',length=4,right=True)
# axb.xaxis.set_major_locator(MultipleLocator(0.5))
# axb.yaxis.set_major_locator(MultipleLocator(0.5))
axb.scatter(norm_deficit_south_values,norm_deficit_north_values,s=2,c='k')
axb.set_xlabel('South Difference (MA)')
axb.set_ylabel('North Difference (MA)')
plt.tight_layout()
plt.savefig('norm_northdiff_vs_southdiff_' + first_file[-12:-4] + '-' + last_file[-12:-4]+ '.png')

fig1,axs = plt.subplots(2,1,tight_layout=True)
    
# ax1.xaxis.tick_top()
# ax1.xaxis.set_label_position('top')
axs[0].tick_params(which='both',direction='inout')
axs[0].tick_params(which='major',length=8,right=True)
axs[0].tick_params(which='minor',length=4,right=True)
axs[0].xaxis.set_major_locator(dates.HourLocator(interval=4))
axs[0].xaxis.set_minor_locator(AutoMinorLocator())
axs[0].yaxis.set_minor_locator(AutoMinorLocator())
axs[0].xaxis.set_major_formatter(dates.DateFormatter('%H:%M\n%m/%d'))

# ax1.text(-10,-20, 'B$_y$ vs B$_z$',fontsize=18,bbox={'facecolor':'white', 'alpha':0.5,'pad':10})
axs[0].plot(times, norm_deficit_north_values, c='k',linewidth=0.25)
axs[0].set_title('North Difference')
axs[0].autoscale(axis='x',tight=True)
axs[0].set_ylabel(R'Normalized Current Difference \textit{(MA)}',fontsize=10)

axs[1].tick_params(which='both',direction='inout')
axs[1].tick_params(which='major',length=8,right=True)
axs[1].tick_params(which='minor',length=4,right=True)
axs[1].xaxis.set_major_locator(dates.HourLocator(interval=4))
axs[1].xaxis.set_minor_locator(AutoMinorLocator())
axs[1].yaxis.set_minor_locator(AutoMinorLocator())
axs[1].xaxis.set_major_formatter(dates.DateFormatter('%H:%M\n%m/%d'))
axs[1].plot(times, norm_deficit_south_values, c='r',linewidth=0.25)
axs[1].set_title('South Difference')

axs[1].set_ylabel(R'Normalized Current Difference \textit{(MA)}',fontsize=10)
axs[1].autoscale(axis='x',tight=True)
plt.savefig(file_date + '_norm_difference.pdf')
# plt.show()
'''
# plotting the histograms

fig2, (ax21,ax22) = plt.subplots(1,2,sharey=True,tight_layout=True)
ax21.set_xlim(-2.0,2.0)
ax21.hist(current_deficit_north_values,16)
ax21.set_title(R'North Difference \textit{(MA)}')
ax22.set_xlim(-2.0,2.0)
ax22.hist(current_deficit_south_values,16)
ax22.set_title(R'South Difference \textit{(MA)}')
plt.tight_layout()
plt.savefig(file_date + '_histograms.pdf')
'''
