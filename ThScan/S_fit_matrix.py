
import numpy as np
from  pathlib import Path
from lib_general import load_thscan,mark_autliners, float_a_statistics, float_a_image,import_thscan_from_labview_binary_file_ufxc
from lib_s_curve_fitter import fit_matrix


#=========================

SCAN_FOLDER = r'C:\scan'
SCAN_FOLDER = r'D:\MZ_pomiary\MPIX\2022-11-16'


FIT_COL_RANGE = 48-10,48+10#64-10,64+10#100,120 #64-10,64+10
FIT_ROW_RANGE = 96-10,96+10

FIT_START_VT = 260 # if None use PLATOU_COUNTS & FIT_S_RANGE for fit ROI (for callib S-curve)
FIT_S_RANGE = 2.3

AUTSTENDING_RANGE = 6

RISE_VT = 200
Q_IN = 9000 

#=============================================
ROOT = Path(SCAN_FOLDER)
file_path = Path(ROOT)/'thscan.npy'
vt,counts, chip = load_thscan(file_path)

# fn = r'D:\Pomiary\LNPIXRG\2022-11-16\PXI\1\thrScan.bin'
# vt,counts, chip = import_thscan_from_labview_binary_file_ufxc(fn,100)

counts = counts[:,FIT_ROW_RANGE[0]:FIT_ROW_RANGE[1],FIT_COL_RANGE[0]:FIT_COL_RANGE[1]]

# center, sigma = fit_matrix(vt,counts,FIT_START_VT,FIT_S_RANGE)
gain = (center-RISE_VT)/Q_IN
noise = sigma/gain  

print()
for arr, name in zip((center, sigma),('center','sigma')):
    arr = mark_autliners(arr,AUTSTENDING_RANGE)
    median, std, min_, max_ = float_a_statistics(arr)
    ignored_nr = np.sum(np.isnan(arr))

    params_s = f'\n{name.upper()}, median:{median:0.4f}, stddev:{std:0.4f}, min:{min_:0.4f}, max:{max_:0.4f}, ignored:{ignored_nr/(counts.shape[-1]*counts.shape[-2])*100:0.0f}[%]'        
    print(params_s) #.replace('\n',' '))

    float_a_image(arr.T,title='',folder = ROOT, file_name_stem = name)
    _ = np.argwhere(np.isnan(arr))
    _[:,0] += FIT_COL_RANGE[0]
    _[:,1] += FIT_ROW_RANGE[0]
    curr_crds = _
    # print(curr_crds)


