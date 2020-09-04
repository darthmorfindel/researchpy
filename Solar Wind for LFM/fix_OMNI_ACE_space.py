#!/usr/bin/env python

# This script does some last processing of a made-up OMNI file to fix 
# a few formatting problems.

import pandas as pd
import sys

with open(sys.argv[1],'r') as data_in:
    lines = data_in.readlines() # making the contents a list of strings
    new_lines = []
    header = lines[:72]
    footer = lines[-3:]
    end_of_data = len(lines)-4
    data_range = range(72,end_of_data) # actual data in file
    for i in data_range: # looping over only data
        current_linei = lines[i] # picking out one line at a time
        new_lines.append(current_linei[1:])
        
final_OMNI = open('OMNI_ACE_final.txt','w')
final_OMNI.writelines(header)
final_OMNI.writelines(new_lines)
final_OMNI.writelines(footer)
final_OMNI.close()
