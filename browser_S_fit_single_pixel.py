import sys; sys.path.append('../lib')

import numpy as np
import matplotlib.pyplot as plt
from  pathlib import Path
from lib_general import load_thscan, import_thscan_from_labview_binary_file_ufxc
from lib_s_curve_fitter import fit_pixel

ROOT = Path(r'C:\scan')
ROOT = Path(r'C:\Users\User\Desktop\measurements\lnpix\2022-11-08_porownanie_szumow_zasilacze_kontrolery\1_Ctl=Python_Supp=Lab')

FILE = r'thscan.npy'

COL=22
ROW=65

COL, ROW = [(25, 46), (99, 120), (56, 30), (127, 29), (70, 200)][0]

RISE_VT = 45
Q_IN =  19.599 #400mV: 12.993 el; 615mV: 19.976 el; Ag: 4.889 el, Molybden: 19.599

START_VT = 0 #190 #190 # if None use PLATOU_COUNTS & MARGIN for fit ROI (for callib S-curve)
MARGIN = 2.2
#=============================================

file_path = Path(ROOT)/FILE
vt,counts, chip = load_thscan(file_path)

# fn = r'c:\Users\User\Desktop\measurements\lnpix\2022-11-08_porownanie_szumow_zasilacze_kontrolery\4_PXI\data\\KRUM_0_gateTime_5s_onlyLow16bit.bin'
# vt,counts, chip = import_thscan_from_labview_binary_file_ufxc(fn)

counts_single_pix = counts[:,ROW,COL]

# ORIGINAL PLOT
rise_vt_ix=np.argmin(np.abs((np.array(vt)-RISE_VT)))
plt.rcParams.update({'font.size': 12})
plt.figure(figsize = (12,5));plt.grid();
plt.plot(vt[rise_vt_ix:],counts_single_pix[rise_vt_ix:],'-')

# FIT
fit_result, center,sigma,fit_vt,counts_fit = fit_pixel(vt,counts_single_pix,START_VT,MARGIN)

if fit_result != 'error':
    
    ylim = counts_single_pix[np.argwhere(vt==START_VT).item()]*1.2 if START_VT else PLATOU_COUNTS*1.2
    
    plt.ylim(0,ylim)
    amplitude = center-RISE_VT
    gain = amplitude/Q_IN
    plt.plot(fit_vt,counts_fit,color='red',label=f'gain:{gain:0.1f}\nampl.: {(amplitude):0.0f}\ncenter: {center:0.0f}')
plt.legend(loc='upper right') 
plt.show()

if fit_result != 'error':
    
    rise_vt_ix=np.argmin(np.abs((np.array(vt)-RISE_VT)))
    plt.rcParams.update({'font.size': 12})
    plt.figure(figsize = (12,5));plt.grid();
    _ = np.argwhere(vt==fit_vt[0]).item()
    plt.plot(fit_vt,counts_single_pix[_:_+len(fit_vt)],'-')
    
    noise = sigma/gain
    plt.plot(fit_vt,counts_fit,color='red',label=f'noise:{noise:0.3f}\nsigma: {sigma:0.2f}')
    plt.legend(loc='upper right') 
    plt.show()

