function displayCentralities(G)
degreeCentrality(G);
closenessCentrality(G);



endfunction


function degreeCentrality(G)
InDegrees = sum(G!=0,1)'; %a8roisma mh mhdenikwn stoixeiwn ana sthlh
OutDegrees = sum(G!=0,2); % ..... ana grammh
Degrees = InDegrees + OutDegrees; %ana sthlh kai grammh
d = [InDegrees OutDegrees Degrees];
figure;
hist(d,50);
title('Degree Centrality Distributions');
legend('In-Degrees','Out-Degrees','Degrees');
xlabel('Degrees');
ylabel('Counts');
endfunction

function closenessCentrality(G)
D = FloydWarshall2(G);
N = size(G,1);
InCloseness = (N-1)./sum(D,1)';
OutCloseness = (N-1)./sum(D,2);
c = [InCloseness OutCloseness];
figure;
hist(c,50);
title('Closeness Centrality Distributions');
legend('In-Closeness','Out-Closeness');
xlabel('Closeness');
ylabel('Counts');
endfunction

