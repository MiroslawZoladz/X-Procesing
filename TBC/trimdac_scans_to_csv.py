import go_parent_dir
go_parent_dir.do()

import numpy as np
import matplotlib.pyplot as plt
import pathlib
from lib.helper import load_thscan, pix_crds_sampler

ROOT = r'C:\Users\miro\Desktop\MEASUREMENTS\MPIX\NoDetect\offset_scans\offset_scan\_igm_32_ikrum2\_discr_3'

COLUMN = 38
    
SAMPLE_NR = 10 
ROW_RANGE = (0,192)
COL_RANGE = (0,96)

paths = list(pathlib.Path(ROOT).glob('*.npy'))

        
for path in paths:
    print(path)

    vt,counts,chip = load_thscan(path)
    
    shape = counts.shape
    counts = np.reshape(counts,(shape[0],shape[1]*shape[2]))
    np.savetxt(path.parent / (path.stem +'.csv'), counts, delimiter=",",fmt='%04.0d')
    

