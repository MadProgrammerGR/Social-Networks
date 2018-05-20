filename = "sx-stackoverflow-sorted.txt";
%filename = "test.txt";
batchSize = 100; %poses grammes na diavasei ka8e fora/akmes gia ka8e grafhma

fid = fopen(filename);
curr_data = textscan(fid,"%d %d %d",batchSize);
while !feof(fid)
  
      
  gMatrix = makeGraphMatrix(curr_data{1}, curr_data{2}, curr_data{3});
  displayCentralities(gMatrix!=0);
  
  break;
  next_data = textscan(fid,"%d %d %d",batchSize);
%  curr_nodes = union(curr_data{1},curr_data{2});
%  next_nodes = union(next_data{1},next_data{2});
%  graph_nodes = intersect(curr_nodes, next_nodes);

  curr_data = next_data;
endwhile
fclose(fid);

