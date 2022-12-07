import go_parent_dir
go_parent_dir.do()

import numpy as np
from pathlib import Path

ROOT = Path(r'c:\scan')

for p in ROOT.glob('**/*.npy'):    
    a = np.load(p)
    print(p)
    with open(p.parent/'thscan.bin','wb') as f:
        f.write(a.tobytes())
    
