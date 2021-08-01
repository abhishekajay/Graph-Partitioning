import numpy as np
import networkx as nx
import sys
import time
from networkx.algorithms import bipartite
from collections import Counter, defaultdict
import itertools 
import algo as m8
import random

"""
@author: Abhishek Ajayakumar
"""
#========================================================================================
# Spectral Bisection Algo
def run_spectral():
    A = []; B = [];
    X = []; Y = [];
    start_time = time.time()
    G = m8.load_graph()
    cc = nx.fiedler_vector(G, weight='weight', normalized=False, tol=1e-08, method='lanczos') 
    mid = np.median(cc)
    count = 0
    E = []
    for i in cc:
        if i <= mid:
            A += [count]
        else:
            B += [count]
        count = count + 1
    if abs(len(A) - len(B)) > 1 and abs(len(A) - len(B)) < 3:
        for i in A:
            if cc[i] == mid:
                A.remove(i)
                B += [i]
                break                      
    if abs(len(A) - len(B)) > 3:
        if len(A) > len(B):
            swap = random.sample(A, len(A)-len(B))
            A = list(set(A) - set(swap))
            B = list(set(B).union(set(swap)))
        else :
            swap = random.sample(B, len(B)-len(A))
            B = list(set(B) - set(swap))
            A = list(set(A).union(set(swap)))

    g0 , g1 = G.subgraph(A), G.subgraph(B)
    slist = [m8.getFiedler(g0) , m8.getFiedler(g1)]
    return slist 

