
import numpy as np
from  pathlib import Path
from lib_general import load_thscan,mark_autsending_pixels, float_a_statistics, float_a_image,import_thscan_from_labview_binary_file_ufxc
from lib_s_curve_fitter import fit_matrix

#=========================

SCAN_FOLDER = r'C:\scan'
SCAN_FOLDER = r'C:\Users\User\Desktop\measurements\lnpix\2022-11-08_porownanie_szumow_zasilacze_kontrolery\2_Ctl=Python_Supp=Mod'
# SCAN_FOLDER = r'C:\Users\User\Desktop\measurements\mpix\2022-11-08_PythonSetupTest\bg=110'

RISE_VT = 45
Q_IN = 9000 #400mV: 12.993 el; 615mV: 19.976 el; Ag: 4.889 el

START_VT = 0 # if None use PLATOU_COUNTS & MARGIN for fit ROI (for callib S-curve)
MARGIN = 3

AUTSTENDING_RANGE = 10
#=============================================
ROOT = Path(SCAN_FOLDER)
file_path = Path(ROOT)/'thscan.npy'
vt,counts, chip = load_thscan(file_path)

# fn = r'c:\Users\User\Desktop\measurements\lnpix\2022-11-08_porownanie_szumow_zasilacze_kontrolery\4_PXI\data\\KRUM_0_gateTime_5s_onlyLow16bit.bin'
# vt,counts, chip = import_thscan_from_labview_binary_file_ufxc(fn)
# vt += 250

counts = counts[:,10:20,10:20]

center, sigma = fit_matrix(vt,counts,START_VT,MARGIN)
gain = (center-RISE_VT)/Q_IN
noise = sigma/gain  

print()
for arr, name in zip((gain, noise),('gain','noise')):
    arr = mark_autsending_pixels(arr,AUTSTENDING_RANGE)
    mean, std, min_dev, max_dev = float_a_statistics(arr)
    ignored_nr = np.sum(np.isnan(arr))

    params_s = f'{name.upper()}\n mean:{mean:0.4f}, stddev:{std:0.4f}, min dev:{min_dev:0.4f}, max dev:{max_dev:0.4f} \n ignored:{ignored_nr/(counts.shape[-1]*counts.shape[-2])*100:0.0f}[%]'        
    print(params_s.replace('\n',' '))

    float_a_image(arr.T,title='',folder = ROOT, file_name_stem = name)
    
# print(str(np.argwhere(np.isnan(center))))

