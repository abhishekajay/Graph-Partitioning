import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import sys
import algo as m8 
import time
#%matplotlib inline
"""
@author: Abhishek Ajayakumar
"""
plt.rcParams['figure.figsize'] = (5,4)
def plott(g0, g1,):
    plt.subplot(1,2,1)
    plt.title(nx.algebraic_connectivity(g0, weight = 'weight'))
    nx.draw_networkx(g0)
    plt.axis('off')
    
    plt.subplot(1,2,2)
    plt.title(nx.algebraic_connectivity(g1 , weight = 'weight'))
    nx.draw_networkx(g1, node_color='y')
    plt.axis('off')
    plt.savefig("kalgo.pdf")
    plt.clf()

def run_kalgo():
  start_time = time.time()
  loadfile = sys.argv[1]
  G = m8.load_graph()
  g0_kl, g1_kl = nx.algorithms.community.kernighan_lin_bisection(G,weight = 'weight')
  g0 = G.subgraph(list(g0_kl)); g1 = G.subgraph(list(g1_kl))
  e0 =  m8.getFiedler(g0); e1 = m8.getFiedler(g1); #val = he.get_normalized_cut(G, g0_kl, g1_kl) ; val1 = he.average_cut(G , g0_kl, g1_kl)
  klist = [e0,e1]
  return  klist
  #plott(g0_kl,g1_kl)  
 
    
if __name__ == "__main__":
     run_kalgo()
