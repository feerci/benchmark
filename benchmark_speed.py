import time

import numpy as np
from feerci import feer, feerci, bootstrap_draw_sorted
from bob.measure import eer_rocch

m = 10000
r = 10


def bootstrap_sorted_feer(impostors, genuines, m=1):
    eers = [0] * m
    impostors = np.array(sorted(impostors))
    genuines = np.array(sorted(genuines))
    for c_iter in range(m):
        imps = bootstrap_draw_sorted(impostors)
        gens = bootstrap_draw_sorted(genuines)
        eers[c_iter] = feer(imps, gens, is_sorted=True)
    return eers


def bootstrap_sorted_bob(impostors, genuines, m=1):
    eers = [0] * m
    impostors = np.array(sorted(impostors))
    genuines = np.array(sorted(genuines))
    for c_iter in range(m):
        imps = bootstrap_draw_sorted(impostors)
        gens = bootstrap_draw_sorted(genuines)
        eers[c_iter] = eer_rocch(imps, gens)
    return eers


def bootstrap_naive_bob(impostors, genuines, m=1):
    eers = [0] * m
    max_rounds = 20
    i = 0

    # It is more time efficient to generate more sample draws in one call to the numpy api. However,
    # this comes at considerable cost in memory (10,000 * 100,000 32-bit scores is 4 GB for example).
    # Therefore, we try to strike a balance between memory and computation.
    for i in range(int(m / max_rounds)):
        imps = np.random.choice(impostors, (max_rounds, len(impostors)))
        gens = np.random.choice(genuines, (max_rounds, len(genuines)))
        for c_iter in range(max_rounds):
            eers[c_iter + i * max_rounds] = eer_rocch(imps[c_iter, :], gens[c_iter, :])
    imps = np.random.choice(impostors, (m % max_rounds, len(impostors)))
    gens = np.random.choice(genuines, (m % max_rounds, len(genuines)))
    for c_iter in range(m % max_rounds):
        eers[c_iter + (i + 1) * max_rounds] = eer_rocch(imps[c_iter, :], gens[c_iter, :])

    return eers

def bootstrap_naive_bob_once(imps, gens):
    return eer_rocch(imps, gens)

sizes = [1e3, 2e3, 5e3, 1e4, 2e4, 5e4, 1e5, 2e5, 5e5, 1e6, 2e6, 5e6, 1e7, 2e7, 5e7]

for n in sizes:
    for i in range(r):

        impostors = np.random.normal(0, 1, int(n))
        genuines = np.random.normal(2, 1, int(n))


        # This sorts while making a copy
        impostors_presorted = np.array(sorted(impostors))
        genuines_presorted = np.array(sorted(genuines))

        if n < 2e5:
            start = time.time()
            bootstrap_naive_bob(impostors, genuines, m=m)
            stop = time.time() - start
            print("speed,%s,%s,%s,%s,,,," % ("naive_bob", stop, n, i), flush=True)
            start = time.time()
            bootstrap_sorted_bob(impostors, genuines, m=m)
            stop = time.time() - start
            print("speed,%s,%s,%s,%s,,,," % ("sorted_bob", stop, n, i), flush=True)

        if n < 2e6:
            start = time.time()
            bootstrap_sorted_feer(impostors, genuines, m=m)
            stop = time.time() - start
            print("speed,%s,%s,%s,%s,,,," % ("sorted_feer", stop, n, i), flush=True)

        start = time.time()
        bootstrap_naive_bob_once(impostors, genuines)
        stop = time.time() - start
        print("speed,%s,%s,%s,%s,,,," % ("bob_once", stop, n, i), flush=True)

        start = time.time()
        # Sorting inside the function is _much_ more efficient than outside of it. This is due to the need to cross
        # the cpython "frontier" in the pre-sorted case.
        feerci(impostors, genuines, is_sorted=False, m=m)
        stop = time.time() - start
        print("speed,%s,%s,%s,%s,,,," % ("feerci_on_unsorted", stop, n, i), flush=True)

        start = time.time()
        feerci(impostors_presorted, genuines_presorted, is_sorted=True, m=m)
        stop = time.time() - start
        print("speed,%s,%s,%s,%s,,,," % ("feerci_on_presorted", stop, n, i), flush=True)
