import _go_parent_dir
_go_parent_dir.do()

import numpy as np
import matplotlib.pyplot as plt
import pathlib
from lib.helper import load_thscan, pix_crds_sampler
import pprint

NAME = ''


ROOT = r'C:\scan'
# ROOT = r'c:\Users\User\Desktop\MEASUREMENTS\LNPIX\2021-03-24_DrugieTestySetupuNaEthernecie_RCas\ZasilaczeLab'

FILE = r'thscan.npy'

SAMPLE_NR = 10

VT=300
CROSS_TRESHOLD = 1500

COL_RANGE_s = np.s_[15:30]
ROW_RANGE_s = np.s_[50:180]

#---------------------------------------
vt,counts, chip = load_thscan(pathlib.Path(ROOT)/FILE)

# for image
counts_oryg = np.copy(counts)

counts = np.asarray(counts,dtype=np.int32)
counts = counts[:,ROW_RANGE_s,COL_RANGE_s]

mean = np.mean(counts[0])
print(mean)

# counts = (counts/mean)

# IMAGE
_=np.argmin(np.abs((np.array(vt)-VT)))

image = counts_oryg[0]
image[ROW_RANGE_s,COL_RANGE_s] = image[ROW_RANGE_s,COL_RANGE_s]*1.2

plt.figure(figsize=(8, 6), dpi=80)
plt.imshow(image, clim=(2000,5000)) #
plt.colorbar()
plt.show()
#
#
# PLOT
plt.rcParams.update({'font.size': 15})
plt.figure(figsize = (14,8));plt.grid();
#plt.xlim(20,80)
#plt.ylim(0,50000)
pix_crds = pix_crds_sampler(SAMPLE_NR,(0,counts.shape[1]),(0,counts.shape[2]))
# plt.legend(loc='upper right') 
for r,c in pix_crds:
    y = counts[:,r,c] #& 0xFFF# if scurve from callib "& 0xFFF"
    plt.plot(vt,y,'-')

# WIRTUAL ADUJSTMENT
cross_points = np.argmin(np.abs(counts-CROSS_TRESHOLD),axis=0)   
cross_min = np.min(cross_points)
cross_max = np.max(cross_points)

lef_max_range = cross_max
right_max_range = len(counts)- cross_min

lef_min_range = cross_min
right_min_range = len(counts)- cross_max

sum_ =  np.zeros(lef_max_range+right_max_range,dtype=np.int32)
tmp = np.copy(sum_)
#
plt.rcParams.update({'font.size': 15})
plt.figure(figsize = (14,8));plt.grid();
plt.axhline(y=CROSS_TRESHOLD,color='red')
for r in range(counts.shape[1]):
    for c in range(counts.shape[2]):
        shift = lef_max_range - cross_points[r,c]        
        tmp[shift:shift+len(counts)] = counts[:,r,c]
        sum_ += tmp
        plt.plot(tmp,'-')
plt.show()

sum_ = sum_[lef_max_range-lef_min_range:lef_max_range+right_min_range]
diff_ = np.flip(np.diff(np.flip(sum_))) 

plt.rcParams.update({'font.size': 15})
plt.figure(figsize = (14,8));plt.grid();  
plt.plot(sum_,'-') 
plt.show()
 
plt.rcParams.update({'font.size': 15})
plt.figure(figsize = (14,8));plt.grid();  
plt.plot(diff_,'-') 
plt.show()

# SAVE
assert not (pathlib.Path(ROOT)/('sum_'+NAME+'.npy')).exists(), "!!! File exists"

np.save(pathlib.Path(ROOT)/('sum_'+NAME),sum_)
np.save(pathlib.Path(ROOT)/('diff_'+NAME),diff_)

with open(pathlib.Path(ROOT)/('chip_'+NAME+'.txt'),'w') as f:
    pprint.pprint(chip, f)
