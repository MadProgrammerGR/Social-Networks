import networkx as nx
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from datetime import datetime as date
import heapq
import itertools
import argparse

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

# https://stackoverflow.com/a/12117065
def restricted_float(x):
    x = float(x)
    if x < 0.0 or x > 1.0:
        raise argparse.ArgumentTypeError("%r not in range [0.0, 1.0]"%(x,))
    return x
parser = argparse.ArgumentParser(description='This program predicts edges on a temporal network and displays centrality measurements.')
parser.add_argument("filename", help="filename of the temporal network dataset")
parser.add_argument("N", type=int, help="number of equally spaced time intervals")
parser.add_argument('--PDF', metavar='filename', help='save distributions on pdf file instead')
group = parser.add_argument_group('Percentages','Percentages of best edges to keep for specific prediction methods')
group.add_argument('Pgd', type=restricted_float, nargs='?', default=0.05, help='Graph Distance')
group.add_argument('Pcn', type=restricted_float, nargs='?', default=0.05, help='Common Neighbors')
group.add_argument('Pjc', type=restricted_float, nargs='?', default=0.05, help="Jaccard's Coefficient")
group.add_argument('Paa', type=restricted_float, nargs='?', default=0.05, help='Adamic/Adar')
group.add_argument('Ppa', type=restricted_float, nargs='?', default=0.05, help='Preferential Attachment')
args = parser.parse_args()
filename = args.filename
N = args.N
(Tmin,Tmax) = read_min_max_T()
dt=(Tmax-Tmin)//N
print('Oldest date:',tmsp2str(Tmin))
print('Newest date:',tmsp2str(Tmax))
print('Number of partitions:',N)
print('Time interval for each partition:',date.fromtimestamp(Tmin+dt)-date.fromtimestamp(Tmin))

file = open(filename,'rU')
now = Tmin
if args.PDF:
    pp = PdfPages(args.PDF)
def read_next_graph():
    global now
    graph = nx.DiGraph()
    while True:
        edge = [int(x) for x in file.readline().split()]
        if not edge or (edge[2]>=now+dt and edge[2]!=Tmax):
            break
        if edge[0]!=edge[1]:
            graph.add_edge(edge[0],edge[1])
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

    in_degrees = [(n-1)*d for d in nx.in_degree_centrality(G).values()]
    out_degrees = [(n-1)*d for d in nx.out_degree_centrality(G).values()]
    degrees = [(n-1)*d for d in nx.degree_centrality(G).values()]
    hist_plot('Degrees',[in_degrees,out_degrees,degrees], (3,1,1), ['r','g','b'])
    plt.legend(['Degree','In-Degree','Out-Degree'])

    G = nx.Graph(G) #directed -> undirected
    hist_plot('Closeness', nx.closeness_centrality(G).values(), (3,2,3), 'xkcd:orangered')
    hist_plot('Betweenness', nx.betweenness_centrality(G).values(), (3,2,4), 'xkcd:crimson')
    hist_plot('Eigenvector', nx.eigenvector_centrality_numpy(G).values(), (3,2,5), 'xkcd:teal')
    hist_plot('Katz', nx.katz_centrality_numpy(G).values(), (3,2,6), 'xkcd:brown')
    plt.tight_layout(rect=(0,0,1,0.95))
    if args.PDF:
        pp.savefig()
        plt.close()
    else: plt.show()

def predict_edges(name, percent, scored_edges, correct_edges):
    scored_edges = list(scored_edges)
    predicted_edges = heapq.nlargest(int(percent * len(scored_edges)), scored_edges, key=lambda e: e[2])
    # success_ratio = sum(1 for (u,v,s) in predicted_edges if (u,v) in correct_edges)/len(predicted_edges)
    # print('%s, successful predictions: %.2f%% from %d predicted edges'%(name,100*success_ratio,len(predicted_edges)))
    num_succesful = sum(1 for (u, v, s) in predicted_edges if (u, v) in correct_edges)
    print('%30s%30d%30d%7.2f%%'%(name,num_succesful,len(predicted_edges),100*num_succesful/len(predicted_edges)))


curr_directed_graph = read_next_graph() #initial
try:
    for i in range(N-1):
        print('\nGraph',i)
        next_directed_graph = read_next_graph()

        V_star = set(curr_directed_graph).intersection(set(next_directed_graph))
        G_star = nx.Graph(curr_directed_graph).subgraph(V_star)  # undirected subgraph with only nodes-edges in V_star
        all_pairs = list(itertools.combinations(G_star.nodes,2))

        graph_d = dict(nx.all_pairs_shortest_path_length(G_star))
        graph_d = [(u,v,-graph_d[u][v]) if v in graph_d[u] else (u,v,float('-inf')) for (u,v) in all_pairs]
        comm_neighbors = [(u,v,sum(1 for n in nx.common_neighbors(G_star,u,v))) for (u,v) in all_pairs]
        jaccard_coeff = nx.jaccard_coefficient(G_star,all_pairs)
        adamic_adar = nx.adamic_adar_index(G_star,all_pairs)
        pref_attach = nx.preferential_attachment(G_star,all_pairs)

        correct_edges = nx.Graph(next_directed_graph).subgraph(V_star).edges

        print('%30s%30s%30s%7s' %('Method','Successfully predicted edges','Total predicted edges','Ratio'))
        print('%30s%30d%30d%7.2f%%'%('Random Selection',len(correct_edges),len(all_pairs),100*len(correct_edges)/len(all_pairs)))
        predict_edges('Graph Distance', args.Pgd, graph_d, correct_edges)
        predict_edges('Common Neighbors', args.Pcn, comm_neighbors, correct_edges)
        predict_edges('Jaccard\'s Coefficient', args.Pjc, jaccard_coeff, correct_edges)
        predict_edges('Adamic Adar', args.Paa, adamic_adar, correct_edges)
        predict_edges('Preferential Attachment', args.Ppa, pref_attach, correct_edges)

        plot_centralities(curr_directed_graph)
        curr_directed_graph = next_directed_graph
except KeyboardInterrupt:
    file.close()
    if args.PDF:
        pp.close()
