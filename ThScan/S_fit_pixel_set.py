import numpy as np
import matplotlib.pyplot as plt
from  pathlib import Path
from lib_general import load_thscan, pix_crds_sampler
from lib_s_curve_fitter import fit_pixel

SCAN_FOLDER = r'C:\scan'
SCAN_FOLDER = r'D:\MZ_pomiary\MPIX\2022-11-16'

SAMPLE_NR = 5
SAMPLING_COL_RANGE = 0,96#100,120 #64-10,64+10
SAMPLING_ROW_RANGE = 0,192

FIT_START_VT = 260 #190 #190 # if None use PLATOU_COUNTS & MARGIN for fit ROI (for callib S-curve)
FIT_S_RANGE = 2.3

RISE_VT = 200
Q_IN =  12.993 #400mV: 12.993 el; 615mV: 19.976 el; Ag: 4.889 el

#=============================================
ROOT = Path(SCAN_FOLDER)
file_path = Path(ROOT)/ r'thscan.npy'
vt,counts, chip = load_thscan(file_path)

# fn = r'D:\Pomiary\LNPIXRG\2022-11-16\PXI\1\thrScan.bin'
# vt,counts, chip = import_thscan_from_labview_binary_file_ufxc(fn,100)

pix_crds = pix_crds_sampler(SAMPLE_NR,SAMPLING_ROW_RANGE,SAMPLING_COL_RANGE)
# pix_crds = curr_crds

for row,col  in pix_crds:
    counts_single_pix = counts[:,row,col]
    
    # FIT
    fit_result, center,sigma,fit_vt,counts_fit = fit_pixel(vt,counts_single_pix,FIT_START_VT,FIT_S_RANGE)
    
    params_s = ''
    if fit_result != 'error':
        amplitude = center-RISE_VT
        gain = amplitude/Q_IN
        noise = sigma/gain
        params_s = f'row={row}, col={col},,center={center:0.0f}, ampl={amplitude:0.0f}, gain={gain:0.1f},, sigma={sigma:0.2f}, noise={noise:0.3f}'
      
    plt.rcParams.update({'font.size': 12})
    plt.figure(figsize = (12,5));plt.grid();
    plt.plot(vt,counts_single_pix,'-')
    if fit_result != 'error':        
        plt.plot(fit_vt,counts_fit,color='red',label=params_s.replace(',','\n'))
        
    # plt.savefig(ROOT/'fit.png')    
    plt.legend()
    plt.show()
    
    print(params_s)
    
    print()        

