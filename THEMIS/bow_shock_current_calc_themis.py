#!/usr/bin/env python

import sys
import os.path
from os import path
import numpy as np

with open(sys.argv[1], 'r') as data_in: # opening file, making it a Python object
    lines = data_in.readlines() # making the contents a list of strings
    loop_range = range(61, 83) # B while in magnetosheath
    Bx_sum = 0
    By_sum = 0
    Bz_sum = 0
    for i in loop_range: # looping over only magnetosheath B values
        current_linei = lines[i] # picking out one line at a time
        entry_x = current_linei[38:47]
        print('this is not working')
'''
        Bx_sum += float(current_linei[38:47]) # choosing Bx values and creating sum of all (for average later)
        By_sum += float(current_linei[62:70]) # choosing By values
        Bz_sum += float(current_linei[86:93]) # choosing Bz values
    Bx_avg = Bx_sum/len(loop_range)
    By_avg = By_sum/len(loop_range)
    Bz_avg = Bz_sum/len(loop_range)
    print(Bx_avg, By_avg, Bz_avg)
'''
