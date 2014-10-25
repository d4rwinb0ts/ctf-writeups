import struct

data = open('weissman.csawlz')

def read_header(data):
    assert data.read(8) == 'CSAWlz\0\0'
    print struct.unpack('<I', data.read(4))[0] == 1
    return struct.unpack('<I', data.read(4))[0]
    
def asdf(text):
    chunks = text.split('\x13')
    for i,c in enumerate(chunks[:100]): 
        if len(c) > 9:
            c, d = c[:9], c[9:]
            print "{0:5} {2}\t".format(i, 0, c)
            for i in range(0, len(d), 3):
                print '\x1b[32m', 
                print map(ord,d[i:i+3]),
                print '\x1b[m'
        else:
            print "{0:5} {2}\t".format(i, 0, c),
    print text[:200]

def read_entry(n):
    assert data.read(4) == 'AAee'
    compressed_size = struct.unpack('<I', data.read(4))[0]
    uncompressed_size = struct.unpack('<I', data.read(4))[0]
    filename = data.read(32)
    print '-' * 50
    print filename, compressed_size, uncompressed_size
    text = data.read(compressed_size)
    asdf(text)
    raise 0

entries = read_header(data)
entries = map(read_entry, range(entries))
