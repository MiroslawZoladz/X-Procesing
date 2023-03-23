import numpy as np
from pathlib import Path
from tqdm import tqdm

# ---- PARAMS -----
ROOT = Path(r'C:\scan\trimdac_scans')
DRISCRS = 1,2,3
# ------ MAIN ------------

for discr in DRISCRS:

    folder = ROOT / f'discr={discr}'
    print(folder)
    
    _ = np.load(folder/'0.npy')
    centers = np.zeros((64,)+_.shape[1:], dtype = np.uint16) 

    for offset in tqdm(range(64)):
        counts = np.load(folder/(str(offset)+'.npy'))
        centers[offset] = np.argmax(counts, axis=0)

    np.save(folder/'centers',centers)


