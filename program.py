import networkx as nx
import numpy as np
from matplotlib import pyplot as plt
from datetime import datetime as date


def read_min_max_T():
    from sys import platform
    import subprocess
    if "linux" in platform:
        tmin = int(subprocess.check_output('head -1 '+filename).split()[2])
        tmax = int(subprocess.check_output('tail -1 '+filename).split()[2])
    elif "win" in platform:
        tmin = int(subprocess.check_output('powershell Get-Content '+filename+' -Head 1').split()[2])
        tmax = int(subprocess.check_output('powershell Get-Content '+filename+' -Tail 1').split()[2])
    else: #read full file with pandas..
        import pandas
        data = pandas.read_csv(filename, usecols=[2], delimiter=' ', dtype=int, header=None).values
        tmin = data[:,0].min()
        tmax = data[:,0].max()
    return (tmin,tmax)

def tmsp2str(seconds):
    return date.fromtimestamp(seconds).strftime('%Y/%m/%d %H:%M')


filename = 'sx-stackoverflow.txt'
(Tmin,Tmax) = read_min_max_T()
N=10000
dt=(Tmax-Tmin)//N
print('Oldest date:',tmsp2str(Tmin))
print('Newest date:',tmsp2str(Tmax))
print('Number of partitions:',N)
print('Time interval for each partition:',date.fromtimestamp(Tmin+dt)-date.fromtimestamp(Tmin))

file = open(filename,'rU')
now = Tmin
def readNextGraph():
    global now
    graph = nx.DiGraph()
    while True:
        edge = [int(x) for x in file.readline().split()]
        if not edge or (edge[2]>=now+dt and edge[2]!=Tmax):
            break
        graph.add_edge(edge[0],edge[1],time=edge[2])
    if not edge: file.close()
    now += dt
    if not graph.number_of_edges() and now<Tmax:
        graph = readNextGraph()
    return graph


for i in range(N):
    G = readNextGraph()
    plt.figure('Graph %s:  %s  -  %s'%(str(i),tmsp2str(Tmin+i*dt),tmsp2str(Tmin+(i+1)*dt)))
    plt.title('Degree Centrality\nGraph size = '+str(G.number_of_nodes())+' nodes')

    n = G.number_of_nodes()
    inDegrees = [(n-1)*d for d in nx.in_degree_centrality(G).values()]
    outDegrees = [(n-1)*d for d in nx.out_degree_centrality(G).values()]
    degrees = [(n-1)*d for d in nx.degree_centrality(G).values()]
    plt.hist([inDegrees,outDegrees,degrees], rwidth=1.0, color=['g','b','r'], alpha=0.7, label=['In-Degrees','Out-Degrees','Degrees'])

    plt.xlabel('Degrees')
    plt.ylabel('Frequencies')
    plt.legend()
    plt.grid(True)
    plt.show()

    # TODO gia twra: ypoloipa centralities, closeness, betweeness, eigenvector, katz



