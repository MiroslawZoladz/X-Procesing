import go_parent_dir
go_parent_dir.do()

import pathlib
from lib.helper import load_thscan

ROOT = r'c:\Users\miro\Desktop\MEASUREMENTS\MPIX\Detect\1.50mm\vdet_scan'
FILE = 'thscan.npy'

ROOT = pathlib.Path(ROOT)

paths = list(ROOT.glob('**/*.npy'))
for p in paths:    
    vt,counts,chip = load_thscan(p)
    
    print(p)
    ## TO BINARY
    with open(p.parent / 'thscan.bin','wb') as f:
        f.write(counts.tobytes())

## TO CSV
#shape = counts.shape
#counts = np.reshape(counts,(shape[0],shape[1]*shape[2]))
#np.savetxt(file.parent / 'counts.csv', counts, delimiter=",",fmt='%04.0d')
#np.savetxt(file.parent / 'vt.csv', vt, delimiter=",",fmt='%04.0d')






