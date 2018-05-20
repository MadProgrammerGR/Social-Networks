% == vectorized ==
function [D,P] = FloydWarshall2(W)
% This function computes shortest paths' distances for each pair of nodes
% within the graph whose initial weight (adjacency) matrix is stored in
% matrix W.
% Element D[i,j] of matrix D stores the shortest path distance from node i 
% to node j.
% Matrix P is the corresponding predecessor matrix so that element P[i,j]
% stores the last vertex traversed within the shortest path connecting
% nodes i and j.

% Get the number of nodes pertaining to the graph.
nodes_num = size(W,1);

% Initialize internal matrix D.
D = double(W);

% prepare dist matrix
D(D==0) = Inf;
D(1:nodes_num+1:end) = 0;
prevD = D;

% Initialize internal matrix P.
P = zeros(nodes_num,nodes_num);
% Main Algorithm.
for k = 1:1:nodes_num
  D = min(D,D(:,k) + D(k,:));
  P(D!=prevD) = k;
  prevD = D;
end;

