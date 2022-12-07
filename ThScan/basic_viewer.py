# =========== PARAMETERS =========================
# SCAN_FOLDER = r'C:\Users\User\Desktop\measurements\lnpix\2022-11-08_porownanie_szumow_zasilacze_kontrolery\1_Ctl=Python_Supp=Lab'
SCAN_FOLDER = r'C:\scan'
# SCAN_FOLDER = r'C:\scan\trimdac_scans\discr=0'
# SCAN_FOLDER = r'D:\MZ_pomiary\MPIX\2022-11-16'

# SCAN_FOLDER = r'C:\scan\5a_ikrum=   ; igm=   ; vt0=  s; vt1=   ; DIS_DYN_SW= ; MPR_en= ; bgshc_W= ; bgshc_N= ; bgshc_NW= ;'
# SCAN_FOLDER = r'C:\scan\5b_ikrum=   ; igm=   ; vt0=225; vt1=  s; DIS_DYN_SW= ; MPR_en= ; bgshc_W= ; bgshc_N= ; bgshc_NW= ;'
# SCAN_FOLDER = r'C:\scan\5c_ikrum=   ; igm=   ; vt0=  s; vt1=   ; DIS_DYN_SW= ; MPR_en=1; bgshc_W=1; bgshc_N=1; bgshc_NW=1;'
# SCAN_FOLDER = r'C:\scan\5d_ikrum=   ; igm=   ; vt0=225; vt1=  s; DIS_DYN_SW= ; MPR_en=1; bgshc_W=1; bgshc_N=1; bgshc_NW=1;'

# SCAN_FOLDER = r'C:\scan\6a_ikrum=   ; igm=   ; vt0=  s; vt1=   ; DIS_DYN_SW=0; MPR_en= ; bgshc_W= ; bgshc_N= ; bgshc_NW= ;'
# SCAN_FOLDER = r'C:\scan\6b_ikrum=   ; igm=   ; vt0=225; vt1=  s; DIS_DYN_SW=0; MPR_en= ; bgshc_W= ; bgshc_N= ; bgshc_NW= ;'
# SCAN_FOLDER = r'C:\scan\6c_ikrum=   ; igm=   ; vt0=  s; vt1=   ; DIS_DYN_SW=0; MPR_en=1; bgshc_W=1; bgshc_N=1; bgshc_NW=1;'
# SCAN_FOLDER = r'C:\scan\6d_ikrum=   ; igm=   ; vt0=225; vt1=  s; DIS_DYN_SW=0; MPR_en=1; bgshc_W=1; bgshc_N=1; bgshc_NW=1;'

SCAN_FOLDER = r'C:\scan\7a_ikrum=  2; igm= 32; vt0=  s; vt1=   ; DIS_DYN_SW= ; MPR_en= ; bgshc_W= ; bgshc_N= ; bgshc_NW= ;'
SCAN_FOLDER = r'C:\scan\7c_ikrum=  2; igm= 32; vt0=  s; vt1=   ; DIS_DYN_SW= ; MPR_en=1; bgshc_W=1; bgshc_N=1; bgshc_NW=1;'
SCAN_FOLDER = r'C:\scan\8a_ikrum=  2; igm= 32; vt0=  s; vt1=   ; DIS_DYN_SW=0; MPR_en= ; bgshc_W= ; bgshc_N= ; bgshc_NW= ;'
SCAN_FOLDER = r'C:\scan\8c_ikrum=  2; igm= 32; vt0=  s; vt1=   ; DIS_DYN_SW=0; MPR_en=1; bgshc_W=1; bgshc_N=1; bgshc_NW=1;'


# FILE = r'0.npy'
FILE = r'thscan.npy'


SAMPLE_NR = 50
ROI_COL = 0+24-10,96-24-10,#LNPIXRG#100,120 #64-10,64+10
ROI_ROW = 0+48,196-48#LNPIXRG128-10,128+10

VT_RANGE = None #300,600#None #300,600 #220,350
COUNTS_RANGE = 0, 4096 #0,2000

CURRENT_VT=225

REMOVE_OUTLINERS_AT_CURRENT_VT=True
OUTLINING_RANGE = 31

#=========== CODE =================
import go_parent_dir
go_parent_dir.do()

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

from pathlib import Path
from lib_general import load_thscan, pix_crds_sampler, mark_autliners, import_thscan_from_labview_binary_file_ufxc

ROOT = Path(SCAN_FOLDER)

vt,counts, chip = load_thscan(ROOT/FILE)

# ## From LabView
# fn = r'D:\Pomiary\LNPIXRG\2022-11-16\PXI\1\thrScan.bin'
# vt,counts, chip = import_thscan_from_labview_binary_file_ufxc(fn,100)


if VT_RANGE:
    s,t = VT_RANGE[0],VT_RANGE[-1]
    s_ix=np.argmin(np.abs((np.array(vt)-s)))
    t_ix=np.argmin(np.abs((np.array(vt)-t)))
    vt = vt[s_ix:t_ix]
    counts = counts[s_ix:t_ix]
    
CURRENT_VT = min(max(vt[1],CURRENT_VT),vt[-2])
vt_ix=np.argmin(np.abs((np.array(vt)-CURRENT_VT)))

if REMOVE_OUTLINERS_AT_CURRENT_VT:
    cts_med = np.median(counts,axis=[2,1])
    counts = np.array(counts,dtype=np.float32)
    sum_abs_diff =  np.sum(np.abs(counts - cts_med[:,None,None]),axis=0)
    inv = np.isnan(mark_autliners(sum_abs_diff,margin=OUTLINING_RANGE,unit='sigma'))
    counts = np.where(~inv,counts,np.nan)

# PLOTS    
plt.rcParams.update({'font.size': 15})
plt.figure(figsize = (10,4));plt.grid();

if VT_RANGE:
    plt.xlim(*VT_RANGE)

if REMOVE_OUTLINERS_AT_CURRENT_VT:    
    rang = COUNTS_RANGE if COUNTS_RANGE else (0,cts_med[vt_ix]*1.4)  
    plt.ylim(*rang)

pix_crds = pix_crds_sampler(SAMPLE_NR,ROI_ROW,ROI_COL) #random pixels

for r,c in pix_crds:
    y = counts[:,r,c]    
    if not np.isnan(y[0]):
        plt.plot(vt,y,'-')        
plt.xlabel('vt[lsb]')
plt.ylabel('count')

plt.plot(vt,cts_med, color='black',linewidth=3)

plt.axvline(x = CURRENT_VT, color = 'black', linestyle='--')
plt.savefig(ROOT/'plot.png')  
plt.show()

# IMAGE
plt.figure(figsize=(12, 5)) 
cmap = mpl.cm.get_cmap("viridis").copy()
cmap.set_bad(color='red')

cts = counts[vt_ix]
cts = np.asarray(cts,dtype=np.float32) 
row_roi_ix = np.s_[ROI_ROW[0]:ROI_ROW[1]]
col_roi_ix = np.s_[ROI_COL[0]:ROI_COL[1]]
cts_roi = cts[row_roi_ix,col_roi_ix]
min_=np.nanmin(cts_roi)
max_=np.nanmax(cts_roi)
clim = min_,max_
cts *= 0.95
cts[row_roi_ix,col_roi_ix] *= 1.05
plt.imshow(cts.T,interpolation='none',cmap=cmap,clim=clim)
plt.colorbar(location="right")
plt.savefig(ROOT/'image.png')  
plt.show()


