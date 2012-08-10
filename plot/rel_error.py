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

N_NOISES=25
N_SIGNALS=10
D_LENGTH=1000

def do_plot(data):
    plt.figure(1)
#    plt.gcf().set_size_inches(2*plt.gcf().get_figwidth(),
#                              2*plt.gcf().get_figheight())
    
    xs = [p[0] for p in data]
    ys = [p[1] for p in data]
    
    plt.scatter(xs,ys,c='r',s=30.0,edgecolor='none',label="relative error")
    
    plt.title("relative robustness to noise",color='b',fontsize=20.0)
    plt.xlabel("signal-to-noise ratio")
    plt.ylabel("relative mean squared error (fft / lpsvd)")
    
    plt.xlim(-0.05, 1.05)
    
    plt.gca().xaxis.tick_bottom()
    plt.gca().yaxis.tick_left()
    plt.legend(loc=2)
    
    plt.savefig("relative_error")

def main():
    specs = [u.make_specs(1) for i in range(N_SIGNALS)]
    makers = [s.Periodic(spec, noise=0.0) for spec in specs]
    
    # take data to be a list of tuples [... (nsr, error) ...]
    data = []
    
    noises = linspace(0.0, 1.0, N_NOISES)
    for nsr in noises:
        for maker in makers:
            maker.noise = nsr
            seed = maker.time_series(D_LENGTH)
            
            fft_d = fft.fft(seed)
            fft_r = [c.real for c in fft.ifft(fft_d)]
            
            lpsvd_d = l.LPSVD(seed, count=2.0).decomposition()
            lpsvd_r = lpsvd_d.time_series(D_LENGTH)
            
            maker.noise = 0.0
            clean = maker.time_series(D_LENGTH)
            
            fft_err = u.mean_sq_error(clean,fft_r)
            lpsvd_err = u.mean_sq_error(clean,lpsvd_r)
            
            rel_err = fft_err/lpsvd_err
            data.append((nsr,rel_err))
    
    for p in data:
        print str(p[0])+"\t"+str(p[1])
    
    do_plot(data)
    return None

if __name__ == "__main__":
    main()
