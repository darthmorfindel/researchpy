#!/usr/bin/env python

import sys
import matplotlib.pyplot as plt
# import matplotlib.gridspec 
import numpy as np
from matplotlib import rc
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter, AutoMinorLocator)

rc('font',**{'family':'serif','serif':['Times']})
rc('text', usetex=True)

with open(sys.argv[1], 'r') as data_in: # opening file, making it a Python object
    file_name = sys.argv[1] 
    lines = data_in.readlines() # making the contents a list of strings
    transition_range1 = range(401,520) # transition values, outside section
    Bz_values = [] # initializing lists for loop
    By_values = []
    for i in transition_range1: # looping over only outside transition values
        current_linei = lines[i] # picking out one line at a time
        Bz_values.append(float(current_linei[135:144])) # choosing Bz values and adding to list (for plotting later)
        By_values.append(float(current_linei[97:108])) # choosing By values
    transition_range2 = range(354,401) # transition values, inside section
    Bz_values_trans = [] # initializing lists for loop
    By_values_trans = []
    for j in transition_range2: # looping over only inside transition values
        current_linej = lines[j] # picking out one line at a time
        Bz_values_trans.append(float(current_linej[135:144])) # choosing Bz values and adding to list (for plotting later)
        By_values_trans.append(float(current_linej[97:108])) # choosing By values
    
    # date = file_name[11:-14]
    # print(date)
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    
    ax1.xaxis.tick_top()
    ax1.xaxis.set_label_position('top')
    ax1.tick_params(which='both',direction='inout')
    ax1.tick_params(which='major',length=8)
    ax1.tick_params(which='minor',length=4)
    ax1.xaxis.set_major_locator(MultipleLocator(5))
    ax1.xaxis.set_major_formatter(FormatStrFormatter('%d'))
    ax1.xaxis.set_minor_locator(MultipleLocator(1))
    ax1.yaxis.set_major_locator(MultipleLocator(5))
    ax1.yaxis.set_major_formatter(FormatStrFormatter('%d'))
    ax1.yaxis.set_minor_locator(MultipleLocator(1))
    
    ax1.text(-5,-35, 'B$_y$ vs B$_z$',fontsize=18,bbox={'facecolor':'white', 'alpha':0.5,'pad':10})
    ax1.scatter(Bz_values, By_values, s=2, c='g')
    ax1.scatter(Bz_values_trans, By_values_trans, s=2, c='b')
    labels = ['Exterior','Interior']
    ax1.set_xlabel(R'$B_z$ \textit{(nT)}',fontsize=12)
    ax1.set_ylabel(R'$B_y$ \textit{(nT)}',fontsize=12)
    ax1.legend(labels,frameon=True,loc='lower left')
    plt.tight_layout()
    plt.savefig(file_name[:-4] + '.png')
    plt.show()

''' 
    xlim1 = -35,5
    xlim2 = 0,80
    ylim1 = -65,-50
    ylim2 = -65,10
    gs = matplotlib.gridspec.GridSpec(2,1,height_ratios=[np.diff(ylim1)[0],np.diff(ylim2)[0]],width_ratios=[np.diff(xlim1)[0],np.diff(xlim2)[0]],figure=fig)
    ax1 = plt.subplot(gs[0,0])
    ax1.scatter(Bz_values, By_values, s=2*2, c='g', label='External')
    ax1.xaxis.tick_top()
    ax1.set_ylim(-65,-50)
    ax1.set_yticks([-65,-60,-55,-50])
    ax1.tick_params(direction='in')
    ax1.set_aspect(aspect=1)
    ax1.xaxis.set_label_position('top')
    ax2 = plt.subplot(gs[1,0])
    ax2.scatter(Bz_values_trans, By_values_trans, s=2*2, c='b', label='Internal')
    ax2.xaxis.tick_top()
    ax2.tick_params(direction='in')
    ax2.set_aspect(aspect=1)
    x_ticks=list(range(0,80,5))
    y_ticks=list(range(-65,10,5))
    ax2.set_xticks(x_ticks)
    ax2.set_yticks(y_ticks)
    ax2.xaxis.set_label_position('top')
    fig.suptitle('By vs Bz',fontsize=12)
    ax1.set_xlabel('Bz (nT)')
    ax1.set_ylabel('By (nT)')
    ax2.set_xlabel('Bz (nT)')
    ax2.set_ylabel('By (nT)')
    # plt.tight_layout()
    plt.savefig(file_name[:-4] + '.png')
    plt.show()


    sheath_range = range(62,124) # time period to average over for By in magnetosheath
    By_sheath_sum = 0 # initializing By variable in the sheath
    for i in sheath_range:
        cline_i = lines[i]
        By_sheath_sum += float(cline_i[60:70])
    inside_range = range(206,226) # time period to average over for Bz inside
    Bz_inside_sum = 0 # initializing Bz variable inside magnetopause
    for j in inside_range:
        cline_j = lines[j]
        Bz_inside_sum += float(cline_j[83:93])
    By_sheath_avg = By_sheath_sum / len(sheath_range) # for normalizing By later
    print(By_sheath_avg)
    Bz_inside_avg = Bz_inside_sum / len(inside_range) # for normalizing Bz later
    print(Bz_inside_avg)
    By_values_norm = [By/By_sheath_avg for By in By_values]
    Bz_values_norm = [Bz/Bz_inside_avg for Bz in Bz_values]
    By_values_trans_norm = [By/By_sheath_avg for By in By_values_trans]
    Bz_values_trans_norm = [Bz/Bz_inside_avg for Bz in Bz_values_trans]

    fig, ((ax1,ax2),(ax3,ax4)) = plt.subplots(2,2)
    fig.suptitle("By vs Bz")
    ax1.scatter(Bz_values, By_values, c='g')
    ax1.set_title('Outside')
    ax2.scatter(Bz_values_trans, By_values_trans)
    ax2.set_title('Inside')
    ax3.scatter(Bz_values_norm, By_values_norm, c='g')
    ax3.set_title('Outside, Normalized')
    ax4.scatter(Bz_values_trans_norm, By_values_trans_norm)
    ax4.set_title('Inside, Normalized')
    plt.tight_layout()
    plt.savefig(file_name[:-4] + '.png')
    plt.show()
'''    

