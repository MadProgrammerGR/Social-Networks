import networkx as nx
import pandas as pd
import numpy as np

data = pd.read_csv('data/sx-stackoverflow-sorted.txt',nrows=100,delimiter=' ',dtype=int,header=None,names=['src','dest','time']).values
Tmin = data[:,2].min()
Tmax = data[:,2].max()

N=10
dt=(Tmax-Tmin)//N


groups = {}
for row in data:
    index = (row[2]-Tmin)//dt
    if index==N: index=N-1
    groups[index] = groups.get(index,[]) + [row]

print('Grouped:')
for item in groups.items():
    print(item)

G=[nx.Graph() for i in range(N)]

for group in groups:
    for row in groups[group]:
        G[group].add_edge(row[0],row[1],time=row[2])
