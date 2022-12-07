import numpy as np
import matplotlib.pyplot as plt
from lib_general import import_thscan_from_labview_binary_file_ufxc

fn = r'c:\Users\User\Desktop\measurements\lnpix\2022-11-08_porownanie_szumow_zasilacze_kontrolery\4_PXI\data\\KRUM_0_gateTime_5s_onlyLow16bit.bin'

vt, counts, _ =import_thscan_from_labview_binary_file_ufxc(fn)

plt.plot(vt, counts[:,0])
plt.show()

plt.imshow(counts[20])
plt.show()

