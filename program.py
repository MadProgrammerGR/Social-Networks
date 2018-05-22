import networkx as nx
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from datetime import datetime as date


def tmsp2str(seconds):
    return date.fromtimestamp(seconds).strftime('%Y/%m/%d %H:%M')

data = pd.read_csv('sx-stackoverflow.txt',nrows=1000,delimiter=' ',dtype=int,header=None,names=['src','dest','time']).values
Tmin = data[:,2].min()
Tmax = data[:,2].max()
N=2
dt=(Tmax-Tmin)//N
print('Oldest date:',tmsp2str(Tmin))
print('Newest date:',tmsp2str(Tmax))
print('Number of partitions:',N)
print('Time interval for each partition:',date.fromtimestamp(Tmin+dt)-date.fromtimestamp(Tmin))


# group edges between every dt interval
groups = {}
for row in data:
    index = (row[2]-Tmin)//dt
    if index==N: index=N-1
    groups[index] = groups.get(index,[]) + [row]

#print('Grouped:')
#for item in groups.items():
#    print(item)

G=[nx.DiGraph() for i in range(N)]
for group in groups:
    for row in groups[group]:
        G[group].add_edge(row[0],row[1],time=row[2])



for i in range(N):
    plt.figure('Graph %s:  %s  -  %s'%(str(i),tmsp2str(Tmin+i*dt),tmsp2str(Tmin+(i+1)*dt)))
    plt.title('Degree Centrality\nGraph size = '+str(G[i].number_of_nodes())+' nodes')

    n = G[i].number_of_nodes()
    inDegrees = [(n-1)*d for d in nx.in_degree_centrality(G[i]).values()]
    outDegrees = [(n-1)*d for d in nx.out_degree_centrality(G[i]).values()]
    degrees = [(n-1)*d for d in nx.degree_centrality(G[i]).values()]
    plt.hist([inDegrees,outDegrees,degrees], rwidth=1.0, color=['g','b','r'], alpha=0.7, label=['In-Degrees','Out-Degrees','Degrees'])

    plt.xlabel('Degrees')
    plt.ylabel('Frequencies')
    plt.legend()
    plt.grid(True)
    plt.show()

    # TODO gia twra: ypoloipa centralities, closeness, betweeness, eigenvector, katz



