import _go_parent_dir
_go_parent_dir.do()

import numpy as np
import matplotlib.pyplot as plt
import pathlib

ROOT = r'C:\scan'
ROOT = pathlib.Path(ROOT)

plt.rcParams.update({'font.size': 15})
plt.figure(figsize = (14,8));plt.grid();
for p in list(ROOT.glob('sum_*')):
        a = np.load(p)
        if 'my' in str(p):
            a=a*1.2
        plt.plot(a,'-',label=p.name.replace('sum_','').replace('.npy',''))
plt.legend(loc='upper right') 
plt.title('SUM')
plt.show()

plt.rcParams.update({'font.size': 15})
plt.figure(figsize = (14,8));plt.grid();
#plt.ylim(0,1000_000)

for p in list(ROOT.glob('diff_*')):        
    a = np.load(p)
    x = np.arange(len(a),dtype=np.float)
    if 'moj' in str(p):
        a=a*1.1
        # x += 10.5
        pass

    plt.plot(x,a,'-',label=p.name.replace('diff_','').replace('.npy',''))
plt.legend(loc='upper right') 
plt.title('DIF')
plt.show()

