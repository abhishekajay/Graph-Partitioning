
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Abhishek Ajayakumar
"""
from collections import  Counter

""" Will Contains the code snippets or function that will be used
    by other algorithms"""
import numpy as np
import networkx as nx
import sys
from heapq import nsmallest
from joblib import Parallel, delayed
import time
import random
from operator import add
import os
from joblib import Memory
from networkx.utils import not_implemented_for, py_random_state

@py_random_state(0)
def random_partition(seed= None):

    #=======================================
    # The way the initial parition is taken
    # is taken from the networkx kalgorithm 
    #=======================================
    nodes = list(G)
    seed.shuffle(nodes)
    h = len(nodes) // 2
    partition = (nodes[:h], nodes[h:])
    #=======================================     

    return partition[0],partition[1]

def get_icost_no_hidden_edges(s0, hidden_node_set=set({})):
    ledges = G.edges(nbunch = s0)
    t1 = list(filter (lambda x : (x[0] in s0 and x[1] in s0), ledges))
    dct = dict(zip(s0, [0]*len(s0)))
    for (u,v) in t1:
        w = list(G.get_edge_data(u, v).values())[0]
        dct[u] += w
        dct[v] += w
    icost = [(u,v) for u,v in dct.items() if v != 0]
    return icost

def get_sumoftwo_icost(icost):
    isum = [abs(v) for (u,v) in icost]
    sum1 = sum(nsmallest(2, isum))
    return sum1

def get_allcost_hidden_edges(s0, s1, hidden_node_set= set({})):
    ledges = getedges()
    d1 = dict(zip(s0, [0]*len(s0)))
    d2 = dict(zip(s1, [0]*len(s1)))
    s = s0 | s1
    de = dict(zip(s, [0]*len(s)))
    dct2a = dict(zip(s0, [0]*len(s0)))
    dct2b = dict(zip(s1, [0]*len(s1)))
    #===========================================================================================
    for (u,v) in ledges:
        if (u not in hidden_node_set and v not in hidden_node_set):
            if (u in s0 and v in s0):
                w = list(G.get_edge_data(u, v).values())[0]
                d1[u] += w
                d1[v] += w
            elif (u in s1 and v in s1):
                w = list(G.get_edge_data(u, v).values())[0]
                d2[u] += w
                d2[v] += w
            else :
                w = list(G.get_edge_data(u, v).values())[0]
                de[u] += w
                de[v] += w
        else :
            if (u in s0 and v in s0):
                w = list(G.get_edge_data(u, v).values())[0]
                dct2a[u] += w
                dct2a[v] += w
            elif (u in s1 and v in s1):
                w = list(G.get_edge_data(u, v).values())[0]
                dct2b[u] += w
                dct2b[v] += w
    #========================================================================================            
    dct2a = Counter(d1) + Counter(dct2a)
    dct2b = Counter(d2) + Counter(dct2b)               
    # ========================================================================================   
    icosta = [(u,v) for u,v in d1.items() if v != 0]
    sum1 = get_sumoftwo_icost([(u,v) for u,v in dct2a.items() if v != 0])
    icostb = [(u,v) for u,v in d2.items() if v != 0]
    sum2 = get_sumoftwo_icost([(u,v) for u,v in dct2b.items() if v != 0])
    ecost = [(u,v) for u,v in de.items() if v!= 0]
    return icosta, sum1, icostb, sum2, ecost
    
def get_ecost_edges(s0, s1, hidden_node_set=set({})):
    """ ecost is computed using hiding node and hiding edges"""
    #================================================================================
    s =  (set(s0) | set(s1)) - hidden_node_set
    dct = dict(zip(s, [0]*len(s)))
    l = getedges()
    for (u,v) in l:
        if (u in s0 and v not in s0) :
            w = list(G.get_edge_data(u, v).values())[0]            
            dct[u] += w
            dct[v] += w
        if (u not in s0 and v in s0) :
            w = list(G.get_edge_data(u, v).values())[0]
            dct[u] += w
            dct[v] += w
    ecost = [(u,v) for u,v in dct.items() if v != 0]
    
    return ecost

def get_max_diff_node(ecost, icost, s):
    """ difference of ecost and icost (No absolute) and its max value"""
    ecost = dict(ecost)
    icost = dict(icost) 
    diff = s - icost.keys()
    dct = dict(zip(diff, [0]*len(diff)))
    z = {**icost, **dct}
    c = ecost.keys() & z.keys()
    d3 = {key: ecost[key] - z.get(key, 0) for key in c}
    maxval = max(d3.values())
    max_key = [k for k, v in d3.items() if v == maxval ]
    diffs = (max_key[0],maxval)
    # Fixme: if second graph doesn't contain any node corresponding to g1,
    # i.e. all are internal edges then ecost must be zero.
    # return the maximum difference node and corresponding weight difference
    return diffs

def swapNodes(s0, s1, ecost, icost_a, icost_b, hidden_node_set=set({})):
    """ swapping node based on the max difference """
    g1_active_nodes = list(set(s0) - hidden_node_set)
    g0_active_nodes = list(set(s1) - hidden_node_set)
    flag = True
    n0 = n1 = None
    if len(g0_active_nodes) > 2 and len(g1_active_nodes) > 2:

        n0, _ = get_max_diff_node(ecost, icost_a, s0)
        n1, _ = get_max_diff_node(ecost, icost_b, s1) 
        g0_nodes = set(s0)
        g0_nodes.remove(n0)
        g0_nodes.add(n1)

        g1_nodes = set(s1)
        g1_nodes.remove(n1)
        g1_nodes.add(n0)
        
        hidden_node_set.add(n0)
        hidden_node_set.add(n1)
    else:
        flag = False  # Cannot partition more  
    result = {
        's0': g0_nodes,
        's1': g1_nodes ,
        'hidden_set': hidden_node_set,
        'n0': n0,
        'n1': n1
    }

    return result, flag

def get_icost(s0 = {}):

    return get_icost_no_hidden_edges(s0, hidden_node_set=set({}))

def find_optimalpart(C0, C1):
    sumlist = list(map(add,C0,C1))
    index = None
    if not sumlist:
        return index
    else :
        index = sumlist.index(max(sumlist))           
    return index

# This function checks if the sum of the two minimum internal costs is greater than tau    
def check_valid(l, tau):
    f = [v for (u,v) in l]
    isum = sum(nsmallest(2,f))
    if isum > tau:
        boolv = True
    else:
        boolv = False    
    return boolv

def run(tau): 
    S0 = []
    S1 = []
    C0 = []
    C1 = []
    res = []
    hidden_set = set({})
    flag = True
    s0, s1 = random_partition()
    l0 = get_icost(s0) ; l1 = get_icost(s1)
    b1 = check_valid(l0, tau) ; b2 = check_valid(l1, tau)
    if b1 == True and b2 == True:
        count = 1
        while flag:    
            try:
                count = count + 1
                if hidden_set : 
                    icost_a , a_cost_sum, icost_b , b_cost_sum, ecost  = get_allcost_hidden_edges(s0,s1,hidden_set)    
                else :
                    icost_a = l0; a_cost_sum = get_sumoftwo_icost(l0)
                    icost_b = l1; b_cost_sum = get_sumoftwo_icost(l1)
                    ecost =   get_ecost_edges(s0,s1,hidden_set)
                # checking  whether new parttion is valid or not              
                S0.append(s0) ; S1.append(s1)
                C0.append(a_cost_sum); C1.append(b_cost_sum)
                result, flag = swapNodes(s0, s1, ecost, icost_a, icost_b, hidden_set)
                #==========================================================================
                s0, s1 = result['s0'], result['s1']
                #==========================================================================
                hidden_set = result['hidden_set']
            except Exception as e:
                flag = False
                continue    
    else :
        a_cost_sum = get_sumoftwo_icost(l0)
        b_cost_sum = get_sumoftwo_icost(l1)
        S0.append(s0) ; S1.append(s1)
        C0.append(a_cost_sum); C1.append(b_cost_sum)
        
    index = find_optimalpart (C0, C1)
    e0 = getFiedler(G.subgraph(list(S0[index])))
    e1 = getFiedler(G.subgraph(list(S1[index])))
    ev = min(e0, e1)
    if index is not None:   
        S0 = [S0[index]] ; S1 = [S1[index]]
        res = [S0, S1, [ev]]
    return res 


def getFiedler(G):
    f = nx.algebraic_connectivity(G , weight = 'weight', method = 'lanczos' )    
    return f

def two_smallest(listv):
    c = np.partition(np.matrix(listv)[:,2].flatten(),2)    
    w = c[0,0] + c[0,1]
    return w
def getedges():
    return G.edges()

def main():
    l = G.edges.data('weight')
    tau =  two_smallest(list(l)) # Here tau is set to the sum of two lowest weights
    start_time = time.time()
    try:
        os.mkdir('algo8cache')
    except FileExistsError:
        # directory already exists
        pass
    location = './algo8cache'
    memory = Memory(location, verbose=0)
    E = memory.cache(getedges)
    backend = 'multiprocessing'
    result = []
    result = Parallel(n_jobs=nproc, backend = backend )(delayed(run)(tau) for j in range(iterval))
    reslist = result
    result = list(zip(reslist))
    memory.clear(warn=False) 
    if reslist:      
        suml = [ (i,result[i][0][2][0])  for i in range(iterval) if (result[i][0] != ([]) and result[i][0][2][0] != 0 )]
        try :
            rind = [max(suml,key = lambda x:x[1])][0][0]
        except Exception as e:
            alist = 0 
        tph = (time.time() - start_time)
        try :
            v1 = nx.algebraic_connectivity(G.subgraph((result[rind][0][0])[0]) , weight = 'weight', method = 'lanczos' )
            v2 = nx.algebraic_connectivity(G.subgraph((result[rind][0][1])[0]) , weight = 'weight', method = 'lanczos' )
            alist = [v1, v2]
        except:
            v1, v2 = 0, 0
            alist = [v1, v2]
        return alist
def load_graph():
    G = nx.read_edgelist('./data/'+loadfile, delimiter=',',nodetype=int,
                                  data=(('weight', float),))
    return G 
#=======================================================================================
iterval = 100 # This denotes the number of trials
nproc =  10 # This denotes the number of processes
loadfile = sys.argv[1] 
#G = load_graph() #global
G = load_graph()
#=======================================================================================
if __name__ == "__main__":
    main()