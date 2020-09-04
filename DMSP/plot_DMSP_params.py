#!/usr/bin/env python

import sys
import matplotlib.pyplot as plt
import matplotlib.axes
import datetime
from matplotlib import dates
import numpy as np
from matplotlib import rc
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter, AutoMinorLocator)

rc('font',**{'family':'serif','serif':['Times']})
rc('text', usetex=True)

with open(sys.argv[1], 'r') as data_in: # opening file, making it a Python object
    file_name = sys.argv[1] 
    lines = data_in.readlines() # making the contents a list of strings
    time_range1 = range(56161,57242) # time of interest; CHANGE MANUALLY
    diff_B_perp = [] # initializing lists for loop
    hor_ion_v = []
    glat_vals = []
    glon_vals = []
    times = []
    time_labels = []
    for i in time_range1: # looping over only values for time of interest
        current_linei = lines[i] # picking out one line at a time
        diff_B_perp.append(float(current_linei[96:108])) # choosing diff_B_perp values and adding to list (for plotting later)
        hor_ion_v.append(float(current_linei[112:120])) # choosing horizontal ion velocity values
        year = int(current_linei[5:9])
        month = int(current_linei[17:19])
        day = int(current_linei[27:29])
        hour = int(current_linei[37:39])
        minute = int(current_linei[47:49])
        second = int(current_linei[57:59])
        gdlat = (current_linei[63:70])
        glon = (current_linei[73:81])
        timei_formatted = datetime.datetime(year,month,day,hour,minute,second)
        times.append(timei_formatted)
        labeli = '{}:{}\n{}\n{}'.format(timei_formatted.hour,timei_formatted.minute,gdlat,glon)
        if second==0:
            time_labels.append(labeli)
        else:
            None

    fig, axs = plt.subplots(2,1,sharex=True,figsize=(10,6.5))
    fig.subplots_adjust(hspace=0)
    
    axs[0].plot(times,diff_B_perp,linewidth=0.75,color='k')
    axs[0].tick_params(which='both',direction='inout')
    axs[0].tick_params(which='major',length=8)
    axs[0].tick_params(which='minor',length=4)
    axs[0].tick_params(which='major',labelsize=8)
    axs[1].yaxis.set_minor_locator(AutoMinorLocator())

    axs[1].plot(times,hor_ion_v,linewidth=0.75,color='k')    
    axs[1].tick_params(which='both',direction='inout')
    axs[1].tick_params(which='major',length=8)
    axs[1].tick_params(which='minor',length=4)
    axs[1].tick_params(which='major',labelsize=8)

    axs[1].xaxis.set_major_locator(dates.MinuteLocator())
    axs[1].set_xticklabels(time_labels)
    # axs[1].xaxis.set_major_formatter(FormatStrFormatter('%d'))
    axs[1].xaxis.set_minor_locator(AutoMinorLocator())
    axs[1].yaxis.set_minor_locator(AutoMinorLocator())
    # ax1.yaxis.set_major_locator(MultipleLocator(20))
    # ax1.yaxis.set_major_formatter(FormatStrFormatter('%d'))
    # ax1.yaxis.set_minor_locator(MultipleLocator(5))
    
    axs[1].text(-0.15,-0.225, 'UT\nGDLAT\nGLON',transform=axs[1].transAxes,fontsize=8,bbox={'facecolor':'white', 'edgecolor':'none', 'alpha':0.5,'pad':10})
    date = file_name[4:12]
    satellite = file_name[13:15]
    plt.suptitle('DMSP, {}, F{}'.format(date,satellite))
    plt.autoscale(axis='x',tight=True)
    axs[0].set_ylabel(R'Difference of $B_{perp}$ (\textit{T})',fontsize=10)
    axs[1].set_ylabel(R'Horizontal ion velocity (\textit{m/s})',fontsize=10)
    plt.savefig(file_name[:-15] + '_2027-2045.png') # must manually change time range for name of png
    # plt.tight_layout()
    plt.show()
