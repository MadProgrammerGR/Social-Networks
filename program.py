import networkx as nx
import pandas as pd
import numpy as np

data = pd.read_csv('data/sx-stackoverflow-sorted.txt',nrows=100,delimiter=' ',dtype=int,header=None,names=['src','dest','time']).values
Tmin = data[:,2].min()
Tmax = data[:,2].max()

N=10
dt=(Tmax-Tmin)//N

def dict_append(dict, key, value):
    if key not in dict:
        dict[key] = [value]
    else:
        dict[key] += [value]

groups = {}
for row in data:
    index = (row[2]-Tmin)//dt
    dict_append(groups,index,row)

dict_append(groups,N-1,groups[N])
del groups[N]
print('Grouped:')
for item in groups.items():
    print(item)

##ToDo
## load each graph seperated
#G=[nx.Graph() for i in range(N)]

