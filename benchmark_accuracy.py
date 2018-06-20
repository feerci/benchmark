import time

import numpy as np
from feerci import feer, feerci, bootstrap_draw_sorted
import pandas as pd
np.random.seed(0)
m = 10000
r = 1000


def bootstrap_sorted_feer(impostors, genuines, m=1):
    eers = [0] * m
    for c_iter in range(m):
        imps = bootstrap_draw_sorted(impostors)
        gens = bootstrap_draw_sorted(genuines)
        eers[c_iter] = feer(imps, gens, is_sorted=True)
    return eers

n = 10000
eers = [(.02,2.054*2),(.05,1.645*2),(.1,1.2815*2),(.2,0.8415*2)]

for eer,gen_mean in eers:
    for i in range(r):
        impostors = np.array(sorted(np.random.normal(0,1,int(n))))
        genuines = np.array(sorted(np.random.normal(gen_mean,1,int(n))))

        eers_feer = bootstrap_sorted_feer(impostors,genuines,m=m)
        eer1, estimated_eers, lower, upper = feerci(impostors, genuines, m=m, is_sorted=True)
        print('accuracy,%s,,,%s,%s,%s,%s,%s' % ("feer",i,eer,eer1,eers_feer[int(m * 0.025)],eers_feer[int(m*0.975)]),flush=True)
        print('accuracy,%s,,,%s,%s,%s,%s,%s' % ("feerci",i,eer,eer1,lower,upper),flush=True)