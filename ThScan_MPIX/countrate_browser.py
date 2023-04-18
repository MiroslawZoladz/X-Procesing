# PARAMS
ROOT = r'C:\Users\User\OneDrive\measurements\mpix\2023-03-30'

SETTINGS_VT = {'6b':0}# ,'6c':1,'6d':2}
LIN_RANGE = 50

COLUMN = 10
ROW    = 10

# CODE
import _go_parent_dir
_go_parent_dir.do()

from pathlib import Path
import os

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

from pathlib import Path
from lib_general import load_thscan

from sklearn.linear_model import LinearRegression    
    
def split_path(p):
    path = os.path.normpath(p)
    return path.split(os.sep) 

thscan_paths_l = list(Path(ROOT).glob('**/*.npy'))
chip_settings_l = {split_path(p)[-2] for p in thscan_paths_l} 

for settings in filter(lambda s: s.split('_')[0] in SETTINGS_VT,sorted(chip_settings_l)):

    ctc_vt=SETTINGS_VT[settings.split('_')[0]]
    
    paths_l = list(filter(lambda p:settings in str(p),thscan_paths_l))
    currents_l = sorted(set(map(lambda p: split_path(p)[-3],paths_l)))
    
    current_l_int = list()   
    cts_l = list()
    for current in currents_l:
        thscans_pl = list(filter(lambda p: current in str(p) and settings in str(p),thscan_paths_l))
        p = thscans_pl[0]
        vt,counts, chip = load_thscan(p)
        
        counts_sum = np.zeros(counts.shape,dtype=np.uint32)
        for p in thscans_pl:
            _,cts, _ = load_thscan(p)
            counts_sum += counts
        
        counts = counts_sum
        vt_ix=np.argmin(np.abs((np.array(vt)-ctc_vt)))
        cts = counts[vt_ix,10,10]
        
        current_l_int.append(int(current[:-2]))
        cts_l.append(cts)
    
    # RAW PLOT WITH FIT    
    plt.rcParams.update({'font.size': 16})
    plt.figure(figsize = (ROW,COLUMN));
    plt.plot(current_l_int,cts_l,'-p')
    
    X = np.array(current_l_int).reshape(-1,1)
    Y = np.array(cts_l).reshape(-1,1)
    linear_regressor = LinearRegression()  # create object for the class
    linear_regressor.fit(X[:int((LIN_RANGE/100)*len(X))],Y[:int((LIN_RANGE/100)*len(X))])  # perform linear regression
    ampl_pred = linear_regressor.predict(X).flatten()  # make predictions
    plt.plot(current_l_int,ampl_pred,'--')

    plt.title(settings.split('_')[0])
    plt.xlabel('current[mA]')
    plt.ylabel('counts')
    plt.grid()
    plt.show()
    
    # ERROR   
    plt.rcParams.update({'font.size': 16})
    plt.figure(figsize = (10,10));
    
    error = (np.abs(np.array(cts_l)-np.array(ampl_pred))/ampl_pred[-1])*100
    plt.plot(current_l_int,error,'-p')
    # plt.ylim(0,100)
    plt.xlabel('current[mA]')
    plt.ylabel('error[%]')
    plt.grid(which='major', color='#DDDDDD', linewidth=2)
    plt.grid(which='minor', color='#DDDDDD', linewidth=0.5)
    plt.minorticks_on()
    plt.show()