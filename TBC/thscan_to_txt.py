import sys; sys.path.append('../lib')

import numpy as np
from helper import load_thscan
from  pathlib import Path
from tabulate import tabulate 

import pandas as pd

ROOT = Path(r'D:\scan')
FILE = r'thscan.npy'

COL=22
ROW=(16,17,21)

#=============================================

file_path = Path(ROOT)/FILE
vt,counts, chip = load_thscan(file_path)

df = pd.DataFrame()
df['vt'] = vt
for row in ROW:
    
    pix_counts = counts[:,row,COL]    
    df[f'row={row}'] = pix_counts
    
s = tabulate(df,headers=df.columns,showindex=False,tablefmt="plain")
print(s)
    
    



