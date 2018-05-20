function Graph = makeGraphMatrix(SrcL, DestL, Values)
[Labels,~,ranks] = unique([SrcL(:);DestL(:)]);
Src = ranks(1:end/2);
Dest = ranks(end/2+1:end);

Graph = zeros(length(Labels)); 
Graph(sub2ind(size(Graph),Src,Dest)) = Values;

