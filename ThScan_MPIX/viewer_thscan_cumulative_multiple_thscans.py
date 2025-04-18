# =========== PARAMETERS =========================

HEAD_FOLDER = r'c:\Users\User\OneDrive\measurements\mpix\2025-04-09_Al_FastMode_LowNoiseMode_ChargeSharingCompensation\Msr'
PARAM_FOLDER = 'Al=5b_I=XmA'
TEIL_FOLDER = '5a_ikrum=   ; igm=   ; vt0=  s; vt1=   ; DIS_DYN_SW= ; MPR_en= ; bgshc_W= ; bgshc_N= ; bgshc_NW= ;'

# TEIL_FOLDER =   '5d_ikrum=   ; igm=   ; vt0=230; vt1=  s; DIS_DYN_SW= ; MPR_en=1; bgshc_W=1; bgshc_N=1; bgshc_NW=1;'
#TEIL_FOLDER = '7d_ikrum=  6; igm= 32; vt0=230; vt1=  s; DIS_DYN_SW= ; MPR_en=1; bgshc_W=1; bgshc_N=1; bgshc_NW=1;'

PARAMS = ['10','20','30','40','50','55']
PARAMS.reverse()

SAMPLE_NR = 100

COL_RANGE = 0+5,50#0,96#LNPIXRG#100,120 #64-10,64+10
ROW_RANGE = 0+5,60#192-10#0,192#LNPIXRG128-10,128+10

VT_RANGE = 200, 600 #220,1000 #210,400 #300,600#None #300,600 #220,350
COUNTS_RANGE = 0, 0.50 #0, 1600

COUNTS_IMAGE_VT=300

REMOVE_OUTLINERS=True
OUTLINING_MARGIN = 10

#=========== CODE =================
import _go_parent_dir
_go_parent_dir.do()

import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

from pathlib import Path
from lib_general import load_thscan, pix_crds_sampler, mark_autliners, import_thscan_from_labview_binary_file_ufxc

# PLOT cumulative    
plt.rcParams.update({'font.size': 11})
plt.figure(figsize = (10,4));plt.grid();

for param in PARAMS:
    param_folder = PARAM_FOLDER.replace("X",param)
    current_folder = Path(HEAD_FOLDER)/Path(param_folder)/TEIL_FOLDER

    with open(current_folder/'thscan.json') as f:
        exposition = json.load(f)['exposition']
        t_exp = exposition['value']
        t_exp_unit = exposition['unit']
    
    # list scans
    thscan_paths_l = list(Path(current_folder).glob('**/*.npy'))
    
    # load and cumulate scans
    vt, cts, chip = load_thscan(thscan_paths_l[0])
    counts = np.zeros(cts.shape,dtype=np.float32)
    for path in thscan_paths_l:
        vt, cts, chip = load_thscan(path)
        counts += cts
    
    t_exp_unit = 1/1000 if t_exp_unit=='ms' else 1/1000_000
    counts = ((counts*(1/(t_exp*t_exp_unit)))/1000_000)/len(thscan_paths_l)    
    
    counts = np.copy(counts)
        
    if VT_RANGE:
        s,t = VT_RANGE[0],VT_RANGE[-1]
        s_ix=np.argmin(np.abs((np.array(vt)-s)))
        t_ix=np.argmin(np.abs((np.array(vt)-t)))
        vt = vt[s_ix:t_ix]
        counts = counts[s_ix:t_ix]
        
    COUNTS_IMAGE_VT = min(max(vt[1],COUNTS_IMAGE_VT),vt[-2])
    vt_ix=np.argmin(np.abs((np.array(vt)-COUNTS_IMAGE_VT)))
    
    if REMOVE_OUTLINERS:
        cts_med = np.median(counts,axis=[2,1])
        counts = np.array(counts,dtype=np.float32)
        sum_abs_diff =  np.sum(np.abs(counts - cts_med[:,None,None]),axis=0)
        inv = np.isnan(mark_autliners(sum_abs_diff,margin=OUTLINING_MARGIN,unit='sigma'))
        counts = np.where(~inv,counts,np.nan)
        cts_mean = np.nanmean(counts,(2,1))
        
    counts_roi = counts[:,ROW_RANGE[0]:ROW_RANGE[1],COL_RANGE[0]:COL_RANGE[1]]    
        
    if VT_RANGE:
        plt.xlim(*VT_RANGE)
    
    if REMOVE_OUTLINERS:    
        rang = COUNTS_RANGE if COUNTS_RANGE else (0,cts_med[0]*1.1)  # vt_ix
        plt.ylim(*rang)
    
    pix_crds = pix_crds_sampler(SAMPLE_NR,(0,counts_roi.shape[1]),(0,counts_roi.shape[2])) #random pixels
 
    plt.plot(vt,cts_mean,label=f'X={param}',linewidth=1)

plt.title(PARAM_FOLDER)
plt.xlabel('vt [lsb]')
plt.ylabel('counts [M/s]')    
plt.legend(loc="upper right") #"upper center"
plt.axvline(x = COUNTS_IMAGE_VT, color = 'black', linestyle='--', linewidth=1)
plt.savefig(Path(HEAD_FOLDER)/(PARAM_FOLDER+'__'+TEIL_FOLDER+'.png'))  
plt.show()



