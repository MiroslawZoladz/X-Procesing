import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from scipy import stats
import itertools, random, json

# ------ pixels browsing --------
def pix_crds_sampler(sample_nr, row_range, col_range):  
    pix_crds = list(itertools.product(range(*row_range),range(*col_range)))    
    return random.sample(pix_crds,k=sample_nr)
	
def load_thscan(file_path):
    thscan = np.load(file_path)
    with open(file_path.parent/'thscan.json') as f:
        params = json.load(f)
    vt = range(*params['steps'].values())
    
    with open(file_path.parent/'chip.json') as f:
        chip = json.load(f)
    
    return np.array(vt), thscan, chip

# ---------- statistics ---------------
def mark_autsending_pixels(a,margin_in_sigma):        
    a = np.asarray(a,dtype =np.float32)    
    
    median = np.nanmedian(a)
    mad = stats.median_abs_deviation(a,nan_policy='omit',scale='normal',axis=None)
    
    low_range  = median-(margin_in_sigma*mad)        
    high_range = median+(margin_in_sigma*mad)     

    bad = ( (a < low_range) | (a > high_range))
    a[bad]=np.nan
    
    return a

def float_a_statistics(a): #treshold in %     
    return np.nanmean(a), np.nanstd(a), np.nanmin(a)-np.nanmean(a), np.nanmax(a)-np.nanmean(a)

def float_a_image(a,title, folder = None, file_name_stem=None):
    
    min_= np.nanmin(a)
    max_= np.nanmax(a)
    
    cmap = mpl.cm.get_cmap("viridis").copy()
    cmap.set_bad(color='red')
    
    plt.rcParams['font.size'] = '12'
    plt.figure(figsize=(12, 5))
    plt.title(title)
    plt.imshow(a,clim=(min_,max_),cmap=cmap,interpolation='none') #
    cbar=plt.colorbar(location="right")
    
    if file_name_stem:
        plt.savefig(folder/(file_name_stem+'.png'))
        
    plt.show()
    plt.close()  
    
# import from labview binary file

def import_thscan_from_labview_binary_file_ufxc(file_path):
    a = np.fromfile(file_path, dtype=np.uint16)
    a = np.reshape(a,(152,256,128))
    a = a[:-1]
    return np.arange(a.shape[0]), a, None 