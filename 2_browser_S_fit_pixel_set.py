import numpy as np
import matplotlib.pyplot as plt
from  pathlib import Path
from lib_general import load_thscan 
from lib_s_curve_fitter import fit_pixel
from tabulate import tabulate

# SCAN_FOLDER = r'C:\scan'
SCAN_FOLDER = r'C:\Users\User\Desktop\measurements\lnpix\2022-11-08_porownanie_szumow_zasilacze_kontrolery\1_Ctl=Python_Supp=Lab'
# SCAN_FOLDER = r'C:\Users\User\Desktop\measurements\mpix\2022-11-08_PythonSetupTest\bg=110'

FILE = r'thscan.npy'

COL=22
ROW=65

COORDINATES  = [[ 0,  0],
       [ 0,  6],
       [ 0,  7],
       [ 0,  8],
       [ 0, 16],
       [ 1,  4],
       [ 1,  5],
       [ 1, 14],
] #

RISE_VT = 45
Q_IN =  12.993 #400mV: 12.993 el; 615mV: 19.976 el; Ag: 4.889 el

START_VT = 225 #190 #190 # if None use PLATOU_COUNTS & MARGIN for fit ROI (for callib S-curve)
S_RANGE = 3

SKIP_WHOLE_VIEW = False
#=============================================
ROOT = Path(SCAN_FOLDER)
file_path = Path(ROOT)/FILE
vt,counts, chip = load_thscan(file_path)

for row,col  in COORDINATES:
    row+=10
    col+=10
    counts_single_pix = counts[:,row,col]
    
    print(f' row={row}; column={col}')

    # FIT
    fit_result, center,sigma,fit_vt,counts_fit = fit_pixel(vt,counts_single_pix,START_VT,S_RANGE)
    
    if fit_result != 'error':
        amplitude = center-RISE_VT
        gain = amplitude/Q_IN
        noise = sigma/gain
        params_s = f'rise={RISE_VT}, q_in={Q_IN:0.3f} | center={center:0.0f}, ampl={amplitude:0.0f}, gain={gain:0.1f} | sigma={sigma:0.2f} noise={noise:0.3f}'        
    else:        
        params_s = ''  
      
    if not SKIP_WHOLE_VIEW: 
        rise_vt_ix=np.argmin(np.abs((np.array(vt)-RISE_VT)))
        plt.rcParams.update({'font.size': 11})
        plt.figure(figsize = (12,5));plt.grid();
        
        if fit_result != 'error':
            
            ylim = counts_single_pix[np.argwhere(vt==START_VT).item()]*1.2     
            plt.ylim(0,ylim)
            
            plt.plot(vt[rise_vt_ix:],counts_single_pix[rise_vt_ix:],'-')
            plt.plot(fit_vt,counts_fit,color='red')
        else:
            plt.plot(vt[rise_vt_ix:],counts_single_pix[rise_vt_ix:],'-')    
            
        plt.savefig(ROOT/'fit.png')     
        plt.show()
    
    print(params_s)
    
    if fit_result != 'error':
        
        rise_vt_ix=np.argmin(np.abs((np.array(vt)-RISE_VT)))
        
        plt.rcParams.update({'font.size': 12})
        plt.figure(figsize = (12,5));plt.grid();
        _ = np.argwhere(vt==fit_vt[0]).item()
        fit_counts = counts_single_pix[_:_+len(fit_vt)]
        plt.plot(fit_vt,fit_counts,'-')
        plt.plot(fit_vt,counts_fit,color='red')
        plt.savefig(ROOT/'fit_roi.png')  
        plt.show()
    
        ts = tabulate(zip(fit_vt,fit_counts,counts_fit),headers=['vt','counts','counts_fit'],tablefmt ='plain')
        with open(ROOT/f'fit_c={col}_r={row}.txt','w') as f:
            f.write(ts)
    
    print()        

