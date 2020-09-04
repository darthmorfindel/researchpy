#!/usr/bin/env python

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import sys
import matplotlib.axes
import datetime
from matplotlib import dates
from matplotlib import rc
import numpy as np

rc('font',**{'family':'serif','serif':['Times']})
rc('text', usetex=True)

with open(sys.argv[1], 'r') as data_in: # opening file, making it a Python object
    file_name = sys.argv[1] 
    lines = data_in.readlines() # making the contents a list of strings
    date = file_name[4:12]
    satellite = file_name[13:15]
    time_range1 = range(43801,45722) # time of interest -- CHANGE MANUALLY
    gdlat_vals = []
    glon_vals = []
    times = []
    time_labels = []
    label_lat_loc = []
    label_lon_loc = []
    for i in time_range1: # looping over only values for time of interest
        current_linei = lines[i] # picking out one line at a time
        year = int(current_linei[5:9])
        month = int(current_linei[17:19])
        day = int(current_linei[27:29])
        hour = int(current_linei[37:39])
        minute = int(current_linei[47:49])
        second = int(current_linei[57:59])
        gdlat = float(current_linei[62:70])
        gdlat_vals.append(gdlat)
        glon = float(current_linei[73:81])
        glon_vals.append(glon)
        timei_formatted = datetime.datetime(year,month,day,hour,minute,second)
        times.append(timei_formatted)
        labeli = '{}:{}'.format(timei_formatted.hour,timei_formatted.minute)
        if minute % 5 == 0 and second == 0:
            time_labels.append(labeli)
            label_lat_loc.append(gdlat)
            label_lon_loc.append(glon)
        else:
            None
            
# setting up basemap of continents (using gdlat, glon)

fig = plt.figure(figsize=(8,8))

map = Basemap(projection='stere', width=8E6, height=8E6, lat_0=90, lon_0=-135, resolution='l')
map.drawcoastlines()
map.fillcontinents(color='coral',lake_color='aqua')
map.drawmapboundary(fill_color='aqua')
map.drawmeridians(np.arange(0,360,30))
map.drawparallels(np.arange(-90,90,10))

# describe satellite track

map.plot(glon_vals, gdlat_vals, 'wo', latlon=True, markersize=0.75)
for lon, lat in zip(label_lon_loc, label_lat_loc):
    i = label_lon_loc.index(lon)
    label = "{}".format(time_labels[i])
    xpt, ypt = map(lon, lat)
    plt.annotate(label, xy=(xpt, ypt), xycoords='data', textcoords='offset points', xytext=(0,10),fontsize=12, fontweight='bold', bbox={'facecolor':'white', 'alpha':0.5,'pad':4})
plt.suptitle('DMSP, {}, F{}'.format(date,satellite))
plt.savefig(date + satellite + 'North_overflight_1222.png') # CHANGE TIME MANUALLY
plt.show()
