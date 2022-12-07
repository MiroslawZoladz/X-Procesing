import _go_parent_dir
_go_parent_dir.do()

import numpy as np
import numpy.ma as ma

import matplotlib.pyplot as plt
import pathlib
from lib.helper import load_thscan, pix_crds_sampler

#ROOT = r'C:\Users\miro\Desktop\DT_Measurements_\AGH\2020-01-09\paper_quality_thsacns\bgcsa=0\1'
#FILE = r'thscan.ths.npy'

ROOT = r'C:\Users\miro\Desktop\UFXC_Measurements\CdTe_New\corrections\gain\x-rays\scan'
FILE = r'15.npy'

VT=150

HIST_RANGE = 3000

x,thscan = load_thscan(pathlib.Path(ROOT)/FILE)

frame = thscan[VT]

mask = np.ones((256,128),dtype = np.bool)
mask[0:103,5:118]=False
mask[153:256,5:118]=False

frame = ma.masked_array(frame, mask=mask)

hy,hx = np.histogram(frame.compressed(),bins=HIST_RANGE//20,range=(0,HIST_RANGE))

plt.figure(figsize = (10,5))
plt.grid()
plt.ylim(0,2000)
plt.plot(hx[:-1],hy)


#frame[102,:]=0
#frame[153,:]=0
#frame[:,5]=0
#frame[:,117]=0

plt.figure(figsize=(16, 12), dpi=80)
plt.imshow(frame, clim=(500,2000)) #
plt.colorbar()
plt.show()




