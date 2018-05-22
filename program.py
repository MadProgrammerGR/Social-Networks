import networkx as nx
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

data = pd.read_csv('sx-stackoverflow.txt',nrows=1000,delimiter=' ',dtype=int,header=None,names=['src','dest','time']).values
Tmin = data[:,2].min()
Tmax = data[:,2].max()

N=2
dt=(Tmax-Tmin)//N


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

def draw(G,subplot,pos,measurement,measurement_title):
    plt.subplot(subplot)
    nx.draw(G,pos,node_size=50,node_color=list(measurement.values()),nodelist=list(measurement.keys()))
    plt.title(measurement_title)
    
plt.ion()
plt.show()
#xreiazete ligo beltiosi alla kanei doulia pros to paron
for i in range(N):
    plt.figure("Graph "+str(i))
    pos=nx.spring_layout(G[i])

    draw(G[i],331,pos,nx.degree_centrality(G[i]),"Degree centrality")
    draw(G[i],332,pos,nx.in_degree_centrality(G[i]),"In degree centrality")
    draw(G[i],333,pos,nx.in_degree_centrality(G[i]),"Out degree centrality")
    draw(G[i],334,pos,nx.in_degree_centrality(G[i]),"Closeness centrality")
    draw(G[i],335,pos,nx.in_degree_centrality(G[i]),"Betweeness centrality")
    draw(G[i],336,pos,nx.in_degree_centrality(G[i]),"Eigenvector centrality")
    draw(G[i],338,pos,nx.in_degree_centrality(G[i]),"Katz centrality")
    
