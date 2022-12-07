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
def mark_autliners(a,margin, unit):        
    a = np.asarray(a,dtype =np.float32)    
    
    median = np.nanmedian(a)
   
    
    if unit == 'sigma':
        mad = stats.median_abs_deviation(a,nan_policy='omit',scale='normal',axis=None)
        range_ = margin*mad
    elif unit =='lsb':
        range_ = margin
    else:
        print('!!! mark_autliners argument')
    
    low_range  = median-range_       
    high_range = median+range_    

    bad = ( (a < low_range) | (a > high_range))
    a[bad]=np.nan
    
    return a

def float_a_statistics(a): #treshold in %     
    return np.nanmedian(a), np.nanstd(a), np.nanmin(a), np.nanmax(a)

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

def import_thscan_from_labview_binary_file_ufxc(file_path,vt_start):
    a = np.fromfile(file_path, dtype=np.uint16)
    a = np.reshape(a,(len(a)//256//128,256,128))
    a = a[:-1]
    return np.arange(vt_start,vt_start+a.shape[0]), a, None 
    

# currently not used

def fit_rise_centers_from_treshols_endpoints(counts,treshold):

    treshold_above = counts > treshold
    treshold_left = np.argmax(treshold_above,axis=0)
    treshold_right = len(counts)-1-np.argmax(np.flip(treshold_above,axis=0),axis=0)    
    centers_tresholds_mean = (treshold_left+treshold_right)//2
    
    centers_counts_max = np.argmax(counts,axis=0)
    
    return np.where(treshold_above[0] | treshold_above[-1] |(np.logical_not(np.any(treshold_above,axis=0))),centers_counts_max,centers_tresholds_mean )    