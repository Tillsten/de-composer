#!/usr/bin/epython

import sys
import os.path

p = os.path.realpath(__file__)
q = os.path.split(os.path.dirname(p))
sys.path.append(os.path.join(q[0], "src"))
del p, q # keep globals clean

import matplotlib.pyplot as plt
from numpy import fft, linspace
import lpsvd as l
import utility as u
import signallers as s

N_NOISES=20
N_SIGNALS=25
D_LENGTH=1000

def do_plot(fft_data, lpsvd_data):
    plt.figure(1)
#    plt.gcf().set_size_inches(2*plt.gcf().get_figwidth(),
#                              2*plt.gcf().get_figheight())
    
    fxs = [p[0] for p in fft_data]
    fys = [p[1] for p in fft_data]
    
    lxs = [p[0] for p in lpsvd_data]
    lys = [p[1] for p in lpsvd_data]
    
    plt.scatter(fxs,fys,c='b',s=30.0,edgecolor='none',label="fft errors")
    plt.scatter(lxs,lys,c='g',s=30.0,edgecolor='none',label="lpsvd errors")
    
    plt.title("comparative robustness to noise",color='b',fontsize=20.0)
    plt.xlabel("signal-to-noise ratio")
    plt.ylabel("norm. mean squared error")
    
    plt.xlim(-0.05, 1.05)
    
    plt.gca().xaxis.tick_bottom()
    plt.gca().yaxis.tick_left()
    plt.legend(loc=1)
    
    plt.savefig("comp_error")

def main():
    specs = [u.make_specs(1) for i in range(N_SIGNALS)]
    makers = [s.Periodic(spec, noise=0.0) for spec in specs]
    
    # take data to be a list of tuples [... (nsr, error) ...]
    fft_data = []
    lpsvd_data = []
    
    noises = linspace(0.0, 1.0, N_NOISES)
    for nsr in noises:
        for spec,maker in zip(specs,makers):
            amp = spec[0][0] # use this to normalize errors.
            
            maker.noise = nsr
            seed = maker.time_series(D_LENGTH)
            
            fft_d = fft.fft(seed)
            fft_r = [c.real for c in fft.ifft(fft_d)]
            
            lpsvd_d = l.LPSVD(seed, count=2.0).decomposition()
            lpsvd_r = lpsvd_d.time_series(D_LENGTH)
            
            maker.noise = 0.0
            clean = maker.time_series(D_LENGTH)
            
            fft_err = u.mean_sq_error(clean,fft_r) / (amp**2)
            lpsvd_err = u.mean_sq_error(clean,lpsvd_r) / (amp**2)
            
            fft_data.append((nsr, fft_err))
            lpsvd_data.append((nsr, lpsvd_err))
    
#    for fd in fft_data:
#        print fd
#    for ld in lpsvd_data:
#        print ld
    do_plot(fft_data, lpsvd_data)
    return None

if __name__ == "__main__":
    main()
