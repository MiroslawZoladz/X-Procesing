import sys; sys.path.append('../')

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from lib_general import load_thscan, pix_crds_sampler

#------- PARAMS -----------------
CENTERS_FILE_PATH =r'C:\scan\trimdac_scans'
DISCR_LIST = 0,1 #0,1,2,3
TRIM_VT = 200 

SAMPLE_PIXEL_NR = 250
COL_RAGE = (0,96) 
ROW_RAGE = (0,192) 
HIST_RANGE = 10

#----------- CODE ------------------
for discr in DISCR_LIST:
    
    FOLDER =(( Path(CENTERS_FILE_PATH) / f'discr={discr}'))
    print(FOLDER)

    #- calc corrections
    centers = np.asarray(np.load(FOLDER/'centers.npy'),dtype = np.int16)
    corrections = np.argmin(np.abs(centers - TRIM_VT),axis=0)
    np.save(FOLDER/f'correction.npy',corrections)
    
    # INSPECTION
    
    image_crds = f'discr={discr}'
    
    # ------ draw trimdac - vs offset
    plt.figure(figsize = (8,8)); plt.grid()
    plt.rcParams.update({'font.size': 15})
    plt.xlabel('trimDAC [lsb]')
    plt.ylabel('offset [lsb]')
    crds = pix_crds_sampler(SAMPLE_PIXEL_NR,ROW_RAGE,COL_RAGE)
    for r,c in crds:
        _ = centers[:,r,c]
        plt.plot(_) 
    plt.axhline(y = TRIM_VT, color = 'black', linestyle='--',linewidth=3)
    plt.title(f'TRIM_VT = {TRIM_VT}')
    plt.savefig(FOLDER/f'trim_chars.png') 
    plt.show()
        
    # ------ draw error histogram
    err = np.min(np.abs(centers - TRIM_VT),axis=0)
    plt.figure(figsize = (8,4))
    plt.rcParams.update({'font.size': 15})
    plt.grid()
    plt.hist(err.flat, bins=HIST_RANGE,range=(0,HIST_RANGE)) 
    plt.xlabel('absolute error')
    plt.ylabel('pixel count')
    plt.savefig(FOLDER/f'trim_error.png') 
    plt.show()
    
    
    
