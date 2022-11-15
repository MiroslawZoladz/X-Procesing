# =========== PARAMETERS =========================
SCAN_FOLDER = r'C:\Users\User\Desktop\measurements\lnpix\2022-11-08_porownanie_szumow_zasilacze_kontrolery\1_Ctl=Python_Supp=Lab'
# SCAN_FOLDER = r'C:\Users\User\Desktop\measurements\mpix\2022-11-08_PythonSetupTest\bg=110'
# SCAN_FOLDER = r'C:\scan\offset_scan_discr=bl'

FILE = r'thscan.npy'
# FILE = r'63.npy'

SAMPLE_NR = 50

COL_RANGE = 0,96
ROW_RANGE = 0,192

X_RANGE = None#300,600#None #300,600 #220,350
Y_RANGE = None

OUTLINE_RANGE = 3

VT=225

#=========== CODE =================

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

from pathlib import Path
from lib_general import load_thscan, pix_crds_sampler, mark_autsending_pixels, import_thscan_from_labview_binary_file_ufxc

ROOT = Path(SCAN_FOLDER)

vt,counts, chip = load_thscan(ROOT/FILE)

# fn = r'c:\Users\User\Desktop\measurements\lnpix\2022-11-08_porownanie_szumow_zasilacze_kontrolery\4_PXI\data\\KRUM_0_gateTime_5s_onlyLow16bit.bin'
# vt,counts, chip = import_thscan_from_labview_binary_file_ufxc(fn)

if X_RANGE:
    s,t = X_RANGE[0],X_RANGE[-1]
    s_ix=np.argmin(np.abs((np.array(vt)-s)))
    t_ix=np.argmin(np.abs((np.array(vt)-t)))
    vt = vt[s_ix:t_ix]
    counts = counts[s_ix:t_ix]
    
VT = min(max(vt[1],VT),vt[-2])
vt_ix=np.argmin(np.abs((np.array(vt)-VT)))

# REMOVING OUTLINERS
cts_med = np.median(counts,axis=[2,1])
counts = np.array(counts,dtype=np.float32)
sum_abs_diff =  np.sum(np.abs(counts - cts_med[:,None,None]),axis=0)
inv = np.isnan(mark_autsending_pixels(sum_abs_diff,OUTLINE_RANGE))
counts = np.where(~inv,counts,np.nan)

# PLOTS    
plt.rcParams.update({'font.size': 15})
plt.figure(figsize = (10,4));plt.grid();

# plt.xlim(*X_RANGE)
rang = Y_RANGE if Y_RANGE else (0,cts_med[vt_ix]*1.2)  
plt.ylim(*rang)

pix_crds = pix_crds_sampler(SAMPLE_NR,ROW_RANGE,COL_RANGE) #random pixels

for r,c in pix_crds:
    y = counts[:,r,c]    
    if not np.isnan(y[0]):
        plt.plot(vt,y,'-')        
        plt.xlabel('vt[lsb]')
        plt.ylabel('count')

cts_mean = np.nanmean(counts,axis=(2,1))
plt.plot(vt,cts_mean,color='black',linewidth=3)
plt.axvline(x = VT, color = 'black', linestyle='--')
plt.savefig(ROOT/'plot.png')  
plt.show()

# IMAGE
plt.figure(figsize=(12, 5)) 
cmap = mpl.cm.get_cmap("viridis").copy()
cmap.set_bad(color='red')
cts = counts[vt_ix]
plt.imshow(cts.T,interpolation='none',cmap=cmap)
plt.colorbar(location="right")
plt.savefig(ROOT/'image.png')  
plt.show()


