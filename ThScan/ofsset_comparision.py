import sys; sys.path.append('../lib')

import numpy as np
# from scipy import stats
import matplotlib.pyplot as plt
import matplotlib as mpl

from pathlib import Path
# # import helper, re

from lib_general import load_thscan, mark_autliners

import pandas as pd

from tabulate import tabulate


NOT_CORECTED_THSCAN = r'C:\scan\trimdac_scans\discr=0\32.npy'
CORECTED_THSCAN = r'C:\scan\thscan.npy'


HIST_RANGE = 0,400
NOT_COR_OUTLINING_RANGE = 3
COR_OUTLINING_RANGE = 9

HIST_RANGE = (0,1024)


#=========== MAIN ====================================

NOT_CORECTED_THSCAN = Path(NOT_CORECTED_THSCAN)
CORECTED_THSCAN = Path(CORECTED_THSCAN)

# ----------- NOT COR ----------------

# statystyka
vt,counts, chip = load_thscan(NOT_CORECTED_THSCAN)
not_cor_offsets = np.argmax(counts,axis=0)+vt[0]
not_cor_offsets = mark_autliners(not_cor_offsets,NOT_COR_OUTLINING_RANGE)        
not_cor_mean , not_cor_stdev, not_cor_outliners_nr =  np.nanmean(not_cor_offsets), np.nanstd(not_cor_offsets), np.sum(np.isnan(not_cor_offsets))

# ------------ COR -----------------        

# wyznaczenie srodków risów
vt,counts, chip = load_thscan(CORECTED_THSCAN)
cor_offsets = np.argmax(counts, axis=0)
cor_offsets = mark_autliners(cor_offsets,COR_OUTLINING_RANGE)+vt[0]
cor_mean , cor_stdev, cor_outliners_nr =  np.nanmean(cor_offsets), np.nanstd(cor_offsets), np.sum(np.isnan(cor_offsets))        

# --------------- figures -----------------
# ----histograms

plt.rcParams.update({'font.size': 15})
plt.figure(figsize = (10,5))
plt.xlabel('vt[lsb]')
plt.ylabel('count')

label = f'Not corr.:   mean={not_cor_mean:0.0f},  stdev={not_cor_stdev:0.1f}, outliners={not_cor_outliners_nr}'
plt.hist(not_cor_offsets.flatten(), bins=HIST_RANGE[-1]-HIST_RANGE[0],range=(HIST_RANGE),label=label, color='blue')

label = f'Corrected: mean={cor_mean:0.0f},  stdev={cor_stdev:0.2f}, outliners={cor_outliners_nr}'    
plt.hist(cor_offsets.flatten(), bins=HIST_RANGE[-1]-HIST_RANGE[0],range=(HIST_RANGE),label=label, color='red')

legend = plt.legend(loc='upper right')   
plt.savefig(Path(CORECTED_THSCAN).parent / 'offset_hist_comp') 
plt.grid()
plt.show()


plt.figure(figsize=(12, 5)) 
cmap = mpl.cm.get_cmap("viridis").copy()
cmap.set_bad(color='red')
plt.imshow(not_cor_offsets.T,interpolation='none',cmap=cmap)
plt.colorbar(location="right")
plt.title('Not corrected')
plt.savefig(CORECTED_THSCAN.parent/'offset_image_not_cor.png')  
plt.show()

plt.figure(figsize=(12, 5)) 
cmap = mpl.cm.get_cmap("viridis").copy()
cmap.set_bad(color='red')
plt.imshow(cor_offsets.T,interpolation='none',cmap=cmap)
plt.colorbar(location="right")
plt.title('Corrected')
plt.savefig(CORECTED_THSCAN.parent/'offset_image_cor.png')  
plt.show()


