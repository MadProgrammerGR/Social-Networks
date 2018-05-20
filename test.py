

# filename = 'sx-stackoverflow-sorted.txt'
# outfile = 'sx-stackoverflow-sorted.bin'
# with open(filename,'rU') as fin, open(outfile,'wb') as fout:
#     for line in fin:
#         data = line.split()
#         dataBytes = [int(s).to_bytes(4,byteorder='big') for s in data]
#         fout.write(dataBytes[0]+dataBytes[1]+dataBytes[2])

import timeit

start = timeit.default_timer()

filename = 'sx-stackoverflow-sorted.bin'
i = 0
with open(filename,'rb') as f:
    num1 = num2 = num3 = 1
    while num1 and num2 and num3:
        num1 = int.from_bytes(f.read(4),byteorder='big')
        num2 = int.from_bytes(f.read(4), byteorder='big')
        num3 = int.from_bytes(f.read(4), byteorder='big')
        i += 12   


stop = timeit.default_timer()
print(stop - start)
