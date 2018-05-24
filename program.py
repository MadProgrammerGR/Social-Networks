import networkx as nx
from matplotlib import pyplot as plt
from datetime import datetime as date


def read_min_max_T():
    from sys import platform
    import subprocess
    ok = True
    try:
        if "linux" in platform:
            tmin = int(subprocess.check_output('head -1 '+filename).split()[2])
            tmax = int(subprocess.check_output('tail -1 '+filename).split()[2])
        elif "win" in platform:
            tmin = int(subprocess.check_output('powershell Get-Content '+filename+' -Head 1').split()[2])
            tmax = int(subprocess.check_output('powershell Get-Content '+filename+' -Tail 1').split()[2])
        else: ok = False
    except: ok = False
    if not ok: #read full file with pandas..
        import pandas
        data = pandas.read_csv(filename, usecols=[2], delimiter=' ', dtype=int, header=None).values
        tmin = data[:,0].min()
        tmax = data[:,0].max()
    return (tmin,tmax)

def tmsp2str(seconds):
    return date.fromtimestamp(seconds).strftime('%Y/%m/%d %H:%M')


filename = 'sx-stackoverflow.txt'
(Tmin,Tmax) = read_min_max_T()
N=700
dt=(Tmax-Tmin)//N
print('Oldest date:',tmsp2str(Tmin))
print('Newest date:',tmsp2str(Tmax))
print('Number of partitions:',N)
print('Time interval for each partition:',date.fromtimestamp(Tmin+dt)-date.fromtimestamp(Tmin))

file = open(filename,'rU')
now = Tmin
def read_next_graph():
    global now
    graph = nx.DiGraph()
    while True:
        edge = [int(x) for x in file.readline().split()]
        if not edge or (edge[2]>=now+dt and edge[2]!=Tmax):
            break
        if edge[0]!=edge[1]:
            graph.add_edge(edge[0],edge[1],time=edge[2])
    if not edge: file.close()
    now += dt
    if not graph.number_of_edges() and now<Tmax:
        graph = read_next_graph()
    return graph

def hist_plot(title, measurements, subpos, color):
    plt.subplot(*subpos)
    plt.hist(measurements, 30, rwidth=0.9, color=color)
    plt.ylabel('Frequencies')
    plt.title(title)
    plt.grid(True)

def plot_centralities(G):
    n = G.number_of_nodes()
    plt.figure('Graph %s:  %s  -  %s'%(str(i),tmsp2str(Tmin+i*dt),tmsp2str(Tmin+(i+1)*dt)))
    plt.suptitle('Centrality Measurements (Graph size = '+str(n)+')')

    inDegrees = [(n-1)*d for d in nx.in_degree_centrality(G).values()]
    outDegrees = [(n-1)*d for d in nx.out_degree_centrality(G).values()]
    degrees = [(n-1)*d for d in nx.degree_centrality(G).values()]
    hist_plot('Degrees',[inDegrees,outDegrees,degrees], (3,1,1), ['r','g','b'])
    plt.legend(['Degree','In-Degree','Out-Degree'])

    G = nx.Graph(G) #directed -> undirected
    hist_plot('Closeness', nx.closeness_centrality(G).values(), (3,2,3), 'xkcd:orangered')
    hist_plot('Betweenness', nx.betweenness_centrality(G).values(), (3,2,4), 'xkcd:crimson')
    hist_plot('Eigenvector', nx.eigenvector_centrality_numpy(G).values(), (3,2,5), 'xkcd:teal')
    hist_plot('Katz', nx.katz_centrality_numpy(G).values(), (3,2,6), 'xkcd:brown')
    plt.tight_layout(rect=(0,0,1,0.95))
    plt.show()


G2 = read_next_graph() #initial
for i in range(N-1):
    G1 = G2 #move one graph ahead
    plot_centralities(G1)

    G2 = read_next_graph()
    V_star = set(G1.nodes).intersection(set(G2.nodes))
    G1_star = G1.subgraph(V_star) #subgraph with only nodes-edges in V_star

    #TODO continue...
