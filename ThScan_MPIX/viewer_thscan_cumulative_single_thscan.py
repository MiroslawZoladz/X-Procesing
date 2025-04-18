# =========== PARAMETERS =========================

ROOT_FOLDER = r'c:\Users\User\OneDrive\measurements\mpix\2025-04-09_Al_FastMode_LowNoiseMode_ChargeSharingCompensation\Msr\Al=7b_I=40mA'
# ROOT_FOLDER = r'C:\Users\User\OneDrive\measurements\mpix\2025-04-09_Al_FastMode_LowNoiseMode_ChargeSharingCompensation\Msr\Cu=1b_I=50mA'
SUB_FOLDER = '5a_ikrum=   ; igm=   ; vt0=  s; vt1=   ; DIS_DYN_SW= ; MPR_en= ; bgshc_W= ; bgshc_N= ; bgshc_NW= ;'

# SUB_FOLDER =   '5d_ikrum=   ; igm=   ; vt0=230; vt1=  s; DIS_DYN_SW= ; MPR_en=1; bgshc_W=1; bgshc_N=1; bgshc_NW=1;'
SUB_FOLDER = '7d_ikrum=  6; igm= 32; vt0=230; vt1=  s; DIS_DYN_SW= ; MPR_en=1; bgshc_W=1; bgshc_N=1; bgshc_NW=1;'

IMG_FOLDER = Path(ROOT_FOLDER).parent


SAMPLE_NR = 100

COL_RANGE = 0+5,50#0,96#LNPIXRG#100,120 #64-10,64+10
ROW_RANGE = 0+5,60#192-10#0,192#LNPIXRG128-10,128+10

VT_RANGE = None #220,1000 #210,400 #300,600#None #300,600 #220,350
COUNTS_RANGE = 0, 0.20 #0, 1600

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

CURRENT_FOLDER = Path(ROOT_FOLDER)/ SUB_FOLDER

with open(CURRENT_FOLDER/'thscan.json') as f:
    exposition = json.load(f)['exposition']
    t_exp = exposition['value']
    t_exp_unit = exposition['unit']

# list scans
thscan_paths_l = list(Path(CURRENT_FOLDER).glob('**/*.npy'))

# load scans
counts_roi_l = list()
for path in thscan_paths_l:
    vt, counts, chip = load_thscan(path)
    counts_roi_l.append(counts)

# sum scans
counts = np.zeros(counts_roi_l[0].shape,dtype=np.float32)
for cts in counts_roi_l:
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

# PLOT cumulative    
plt.rcParams.update({'font.size': 11})
plt.figure(figsize = (10,4));plt.grid();

if VT_RANGE:
    plt.xlim(*VT_RANGE)

if REMOVE_OUTLINERS:    
    rang = COUNTS_RANGE if COUNTS_RANGE else (0,cts_med[0]*1.1)  # vt_ix
    plt.ylim(*rang)

pix_crds = pix_crds_sampler(SAMPLE_NR,(0,counts_roi.shape[1]),(0,counts_roi.shape[2])) #random pixels

for r,c in pix_crds:
    y = counts_roi[:,r,c]    
    if not np.isnan(y[0]):
        plt.plot(vt,y,'-')        
plt.xlabel('vt[lsb]')
plt.ylabel('counts_roi[M/s]')

title = path.parent.stem + '\n' + '\n'.join(((path.parent.parent.stem).split('_')))
plt.title(title)

plt.plot(vt,cts_mean,color='black',linewidth=1)

plt.axvline(x = COUNTS_IMAGE_VT, color = 'black', linestyle='--', linewidth=1)
# name = (path.parent.parent.stem).split('_')[-1]
plt.savefig(Path(IMG_FOLDER)/('thscan.png'))  
plt.show()

# # PLOT diff  
# plt.rcParams.update({'font.size': 11})
# plt.figure(figsize = (10,4));plt.grid();

# if VT_RANGE:
#     plt.xlim(*VT_RANGE)

# # if REMOVE_OUTLINERS:    
# #     rang = COUNTS_RANGE if COUNTS_RANGE else (0,cts_med[vt_ix]*1.4)  
# #     plt.ylim(*rang)
    
# cts_mean_diff = np.diff(np.flip(cts_mean))
# # cts_mean_diff=np.convolve(cts_mean_diff, np.ones(2)/2, mode='valid')
# plt.plot(vt[1:],np.flip(cts_mean_diff))
# plt.savefig(CURRENT_FOLDER/'energyscan.png')  

# plt.legend()    
# plt.show()

# IMAGE
plt.figure(figsize=(12, 5)) 
cmap = mpl.cm.get_cmap("viridis").copy()
cmap.set_bad(color='red')

vt_cts = counts[vt_ix]
vt_cts_roi = vt_cts[ROW_RANGE[0]:ROW_RANGE[1],COL_RANGE[0]:COL_RANGE[1]]
min_=np.nanmin(vt_cts_roi)
max_=np.nanmax(vt_cts_roi)
clim = min_,max_

vt_cts[ROW_RANGE[0]:ROW_RANGE[1],COL_RANGE[0]:COL_RANGE[1]] *= 1.2
plt.imshow(vt_cts.T,interpolation='none',cmap=cmap,clim=clim)
plt.colorbar(location="right")
plt.savefig(IMG_FOLDER/'image.png')  
plt.xlabel('ROWS')
plt.ylabel('COLS')
plt.show()


