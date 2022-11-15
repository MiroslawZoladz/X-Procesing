import numpy as np
from scipy.special import erf
from scipy.optimize import curve_fit
import warnings
from scipy.optimize import OptimizeWarning
from tqdm import tqdm
import matplotlib.pyplot as plt

warnings.simplefilter("error", OptimizeWarning)

def find_fit_init_params(counts, margin):
    smooth = np.convolve(counts, np.ones(20)/20, mode='valid')
    # plt.plot(smooth)
    counts = np.asarray(counts,dtype=np.int32)
    diff = np.diff(smooth)
    # plt.plot(diff)
    center = np.argmin(diff)+1
    # print(center)
    _ = counts[center]-(counts[center]*(0.67))
    sigma = np.abs(center-np.argmin(np.abs(counts - _)))
    intercept = counts[center-sigma]
    x_range = center+int(sigma*margin)
    # plt.plot(counts[:x_range])
    return x_range, center, sigma, intercept

def __fit(y,center,sigma,slope,intercept, fit_approx_plot): 
    
    def err_func(x, ampl, cener, sigma,slope,intercept, slope_,intercept_, offset): 
        return ((-1*ampl)*erf((x-cener)/(sigma*np.sqrt(2)))+ampl)*((slope*x)+intercept) + ((slope_*x)+intercept_)  + offset  
    x = np.arange(len(y), dtype=np.uint16)    
    try:
        fit_result, _ = curve_fit(err_func, x, y,p0=[10_000,center,sigma,slope,intercept, slope,intercept, 200])
        return True, fit_result[1],fit_result[2], err_func(x, *fit_result) if fit_approx_plot else None
    except:
        return False, 0,0, None  

def _fit(y,margin,fit_approx_plot = True):  
    init = find_fit_init_params(y,margin)
    slope_init = -20
    y = y[:init[0]]    
    return __fit(y,init[1],init[2],slope_init,init[3],fit_approx_plot)

def fit_pixel(vt,counts,start_vt,margin):
    
    if start_vt:
        start_vt_ix = np.argwhere(vt==start_vt).item()
        counts = counts[start_vt_ix:] 
        vt = vt[start_vt_ix:]            
    try:    
        result, center,sigma,fit_counts = _fit(counts,margin)
        fit_vt = vt[:len(fit_counts)]
        center += vt[0]
        return result, center,sigma,fit_vt,fit_counts
    except:
        return 'error', None, None, None, None    

def fit_matrix(vt, counts, start_vt, margin):
    
    center_a = np.empty(counts.shape[1:])
    center_a.fill(np.nan)
    sigma_a = np.copy(center_a)
    for row in tqdm(range(counts.shape[-2])):
        for col in range(counts.shape[-1]):
            # pixel selection
            cts = counts[:,row,col]
            fit_result, center,sigma,_,_ = fit_pixel(vt,cts,start_vt, margin)            
            if fit_result != 'error':
                center_a[row,col]  = center
                sigma_a[row,col]   = sigma    
    return center_a, sigma_a


