#!/usr/bin/epython

import sys
import os.path

p = os.path.realpath(__file__)
q = os.path.split(os.path.dirname(p))
sys.path.append(os.path.join(q[0], "src"))
del p, q # keep globals clean

import matplotlib.pyplot as plt
from numpy import fft, linspace, average, sqrt
import py_lpsvd as l
import utility as u
import signallers as s
from scipy.stats import sem

N_NOISES=25
N_SIGNALS=25
D_LENGTH=750

def do_plot(fft_data, lpsvd_data):
    plt.figure(1)
#    plt.gcf().set_size_inches(2*plt.gcf().get_figwidth(),
#                              2*plt.gcf().get_figheight())
    plt.subplots_adjust(left=0.125,right=0.95,top=0.95)

    fxs = sorted(list(set([p[0] for p in fft_data])))
    fbs = map(lambda x: [p[1] for p in fft_data if p[0] == x],
              fxs)
    fys = [average(b) for b in fbs]
    fes = [2*sem(b) for b in fbs]
    
    lxs = sorted(list(set([p[0] for p in lpsvd_data])))
    lbs = map(lambda x: [p[1] for p in lpsvd_data if p[0] == x],
              lxs)
    lys = [average(b) for b in lbs]
    les = [2*sem(b) for b in lbs]
    
    plt.errorbar(lxs,lys,yerr=les,
                 c='g',label="lpsvd errors")
    plt.errorbar(fxs,fys,yerr=fes,
                 c='b',label="fft errors")
    
#    plt.title("comparative robustness to noise",color='b',fontsize=20.0)
    plt.xlabel("signal-to-noise ratio")
    plt.ylabel("norm. mean squared error")
    
    ymin,ymax = plt.ylim()
    plt.ylim(-0.05, ymax)
    plt.xlim(-0.05, 1.05)
    
    plt.gca().xaxis.tick_bottom()
    plt.gca().yaxis.tick_left()
    plt.legend(loc=2)
    
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
            maker.noise = 0.0
            amp = 2.0 * (
                average([m**2 for m in maker.time_series(D_LENGTH)])
                )
            
            maker.noise = nsr
            seed = maker.time_series(D_LENGTH)
            
            fft_d = fft.fft(seed)
            fft_r = [c.real for c in fft.ifft(fft_d)]
            
            lpsvd_d = l.LPSVD(seed, count=2.0).decomposition()
            lpsvd_r = lpsvd_d.time_series(D_LENGTH)
            
            maker.noise = 0.0
            clean = maker.time_series(D_LENGTH)
            
            fft_err = 1.0 * (u.mean_sq_error(clean,fft_r)) / amp
            lpsvd_err = 1.0 * (u.mean_sq_error(clean,lpsvd_r)) / amp
            
            fft_data.append((nsr, fft_err))
            lpsvd_data.append((nsr, lpsvd_err))
    
    for fd in fft_data:
        print str(fd[0])+"\t"+str(fd[1])
    for ld in lpsvd_data:
        print str(ld[0])+"\t"+str(ld[1])
    do_plot(fft_data, lpsvd_data)
    return None

if __name__ == "__main__":
    main()
