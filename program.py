import networkx as nx
import pandas as pd
import numpy as np

data = pd.read_csv('sx-stackoverflow.txt',delimiter=' ',dtype=int,header=None,names=['src','dest','time']).as_matrix()
Tmax=data[:,2].max()
Tmin=data[:,2].min()

N=10
dt=(Tmax-Tmin)//N
##ToDo
## save each graph in their on file,del data after that, load each graph seperated, save maybe some minor information like Tmin,Tmax
G=[nx.Graph() for i in range(N)]


        
        
        
