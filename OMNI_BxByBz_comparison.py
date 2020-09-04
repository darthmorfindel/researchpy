#!/usr/bin/env python

import sys 
import numpy as np
import datetime
import matplotlib.pyplot as plt
from matplotlib import dates
from matplotlib import rc
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter, AutoMinorLocator)

rc('font',**{'family':'serif','serif':['Times']})
rc('text', usetex=True)

with open(sys.argv[1], 'r') as data_in: # opening file, making it a Python object
    file_name = sys.argv[1] 
    lines = data_in.readlines() # making the contents a list of strings
    end_of_data = len(lines)-3
    data_range = range(67,end_of_data) # actual data in file
    Bz_values = [] # initializing lists for loop
    By_values = []
    Bx_values = []
    times = []
    time_labels = []
    for i in data_range: # looping over only data
        current_linei = lines[i] # picking out one line at a time
        if float(current_linei[27:38])==9999.99: # checking for bad data in Bx
            Bx_values.append(np.nan)
        else:
            Bx_values.append(float(current_linei[27:38])) # choosing Bz values and adding to list (for plotting later)
        if float(current_linei[57:66])==9999.99: # checking for bad data in Bz
            Bz_values.append(np.nan)
        else:
            Bz_values.append(float(current_linei[57:66])) # choosing Bz values
        if float(current_linei[41:52])==9999.99: # checking for bad data in By
            By_values.append(np.nan)
        else:
            By_values.append(float(current_linei[41:52])) # choosing By values
        year = int(current_linei[6:11])
        day = int(current_linei[0:2])
        month = int(current_linei[3:5])
        hour = int(current_linei[11:13])
        minute = int(current_linei[14:16])
        second = int(current_linei[17:19])
        timei_formatted = datetime.datetime(year,month,day,hour,minute,second)
        times.append(timei_formatted)
        labeli = '{}:{}0\n{}/{}'.format(timei_formatted.hour,timei_formatted.minute,timei_formatted.month,timei_formatted.day)
        if minute==0:
            time_labels.append(labeli)
        else:
            None
    
    # date = file_name[11:-14]
    # print(date)
    fig = plt.figure(figsize=(10,4))
    ax1 = fig.add_subplot(111)
    
    # ax1.xaxis.tick_top()
    # ax1.xaxis.set_label_position('top')
    ax1.tick_params(which='both',direction='inout')
    ax1.tick_params(which='major',length=8,right=True)
    ax1.tick_params(which='minor',length=4,right=True)
    ax1.xaxis.set_major_locator(dates.HourLocator())
    ax1.xaxis.set_minor_locator(AutoMinorLocator())
    ax1.yaxis.set_minor_locator(AutoMinorLocator())
    ax1.set_xticklabels(time_labels)
    # ax1.xaxis.set_major_locator(MultipleLocator(20))
    # ax1.xaxis.set_major_formatter(FormatStrFormatter('%d'))
    # ax1.xaxis.set_minor_locator(MultipleLocator(5))
    # ax1.yaxis.set_major_locator(MultipleLocator(1))
    # ax1.yaxis.set_major_formatter(FormatStrFormatter('%d'))
    # ax1.yaxis.set_minor_locator(MultipleLocator(5))
    
    fig.suptitle('OMNI IMF Components',fontsize=18)
    # ax1.text(-10,-20, 'B$_y$ vs B$_z$',fontsize=18,bbox={'facecolor':'white', 'alpha':0.5,'pad':10})
    ax1.plot(times, Bx_values, c='k',linewidth=0.75)
    ax1.plot(times, By_values, c='b',linewidth=0.75)
    ax1.plot(times, Bz_values, c='r',linewidth=0.75)
    labels = ['B$_x$, GSE','B$_y$, GSM','B$_z$, GSM']
    # ax1.set_xlabel(R'$B_z$ \textit{(nT)}',fontsize=12)
    ax1.set_ylabel(R'IMF \textit{(nT)}',fontsize=12)
    ax1.legend(labels,frameon=True)
    plt.autoscale(axis='x',tight=True)
    plt.savefig(file_name[:-4] + '_vector.pdf')
    plt.show()
