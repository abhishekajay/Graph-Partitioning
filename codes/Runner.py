# This code aims to combine the heuristic , k-algo and the spectral bisection 
# algorithm in a single file
# Running this program requires some arguments
# argument 1 : The name of the file stores as graph eg: python3 Runner.py edges.csv 20 0.1

"""
@author: Abhishek Ajayakumar
"""
import sys
import algo as m8
import kalgo as kl
import spectral as sp
import networkx as nx
import csv
import numpy as np
import os 
from joblib import Memory

try:
    os.mkdir('cache')
except FileExistsError:
    # directory already exists
    pass
location = './cache'
memory = Memory(location, verbose=0)
g1 = memory.cache(m8.load_graph)


G = m8.load_graph()
if nx.is_connected(G) and len(list(G.edges())) >= 4:
    alist1 = m8.main()
    klist = kl.run_kalgo()
    slist = sp.run_spectral()
    memory.clear(warn=False)

    print("heuristic algorithm output is ", alist1[0], alist1[1])
    print("KL output is ", klist[0], klist[1])
    print("spectral output is ", slist[0], slist[1])

else :
    print("graph is disconnected")

#ps.process() 
