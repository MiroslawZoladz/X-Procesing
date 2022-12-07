#import go_parent_dir
#go_parent_dir.do()

import pathlib

from lib.helper import load_thscan

vt,counts,chip = load_thscan( pathlib.Path(r'C:\scan\thscan.npy'))
with open(r'C:\scan\thscan.bin','wb') as f:
    f.write(counts.tobytes())






