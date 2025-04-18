# =========== PARAMETERS =========================
# SCAN_FOLDER = r'C:\Users\User\Desktop\measurements\lnpix\2022-11-08_porownanie_szumow_zasilacze_kontrolery\1_Ctl=Python_Supp=Lab'
SCAN_FOLDER = r'C:\scan'
# SCAN_FOLDER = r'C:\scan\trimdac_scans\discr=3'
# SCAN_FOLDER = r'D:\MZ_pomiary\MPIX\2022-11-16'

# FILE = r'32.npy'
FILE = r'thscan.npy'

HIST_RANGE = 0,500
OUTLINING_RANGE = 5

#=========== CODE =================
import _go_parent_dir
_go_parent_dir.do()

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

offset = np.argmax(counts,axis=0)+vt[0]
offset = mark_autliners(offset, margin = OUTLINING_RANGE, unit='lsb')
mean_,std_, auts_nr = np.nanmean(offset), np.nanstd(offset), np.sum(np.isnan(offset))
param_string = f'mean={mean_:0.0f}; std={std_:0.3f}, autstending nr={auts_nr:0.0f}'

# IMAGE
plt.figure(figsize=(12, 5)) 
cmap = mpl.cm.get_cmap("viridis").copy()
cmap.set_bad(color='red')
plt.imshow(offset.T,interpolation='none',cmap=cmap)
plt.colorbar(location="right")
plt.title(param_string)
plt.savefig(ROOT/'offset.png')  
plt.show()

# Histogram

plt.rcParams.update({'font.size': 15})
plt.figure(figsize = (10,5))
plt.hist(offset.flatten(), bins=HIST_RANGE[-1]-HIST_RANGE[0],range=(HIST_RANGE),color='red')
plt.xlabel('vt[lsb]')
plt.ylabel('count')
plt.title(param_string)
plt.grid()
plt.savefig(ROOT/'histograms.png') 
plt.show()
plt.close()

