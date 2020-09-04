#!/usr/bin/env python

import math
import pandas as pd
# from astropy.io import ascii
# from astropy.table import Table, Column, MaskedColumn

# generating lists for dataframe

minutes = [0]*1440 # will be filled in by loop
density = [5.0]*1440 #/cc
vx = [-400.0]*1440 # km/s
vy = [0.0]*1440 # km/s
vz = [0.0]*1440 # km/s
cs = [30.0]*1440 # km/s
Bx = [0.0]*1440 # nT
Zangle = [0.0]*1440 # degrees
By = [0]*1440 # nT (will be filled in by loop)
Bz = [0]*1440 # nT (will be filled in by loop)
Btot = [0]*1440 # nT (will be filled in by loop)
sw_df_lines = [0]*1440 # for writelines later

# putting in the appropriate IMF component values

for i in range(0,1440):
    # if statements determining By and Bz
    if i < 119: # first hour of initialization phase
        By[i] = 0.0
        Bz[i] = -5.0
    elif i < 239 and i >= 119: # second hour of initialization phase
        By[i] = 0.0
        Bz[i] = 5.0
    elif i < 719 and i >= 239: # first set of run parameters
        By[i] = -10.0
        Bz[i] = 5.0
    else: # second set of run parameters
        By[i] = 10.0
        Bz[i] = -5.0  
    Btot[i] = math.sqrt(Bx[i]**2 + By[i]**2 + Bz[i]**2)
    minutes[i] = '  {}.0'.format(i+1)

# sw_data = Table([minute,density,vx,vy,vz,cs,Bx,By,Bz,Btot,Zangle])
# data_table = ascii.write(sw_data,'SW-SM-DAT')
sw_data = {'minute':minutes,'density':density,'vx':vx,'vy':vy,'vz':vz,'cs':cs,'Bx':Bx,'By':By,'Bz':Bz,'Btot':Btot,'Zangle':Zangle}
sw_df = pd.DataFrame(sw_data,columns=['minute','density','vx','vy','vz','cs','Bx','By','Bz','Btot','Zangle'],dtype=str)
with open('fake_solar_wind_Byswitch.txt','w') as out_file:
    out_file.writelines(['2040 358 0 1','\n  1440 11','\n DATA:\n     '])
    out_file.write(sw_df.to_string(header=False,index=False))
