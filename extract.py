# fritz
# 2012

import sys
import os

def main():

    if len(sys.argv) != 2:
        print "Usage: %s filename.pcap" % sys.argv[0]
        sys.exit()

    dump = sys.argv[1] + ".dump"
    result = dump + ".result"

    cmd = "tshark -R bittorrent.piece.data -T fields " + \
            "-e bittorrent.piece.index -e bittorrent.piece.begin " + \
            "-e bittorrent.piece.data -E separator=, -r %s > %s" \
            % (sys.argv[1], dump)

    print "[-] Executing: %s" % cmd
    try:
        pipe = os.popen(cmd)
    except OSError, err:
        sys.exit("Cannot execute: %s" % err)

    error = pipe.close()

    if error != None:
        sys.exit("Error code returned: %s" % error)

    print "[-] Sorting bittorrent pieces"

    store = {}

    with open(dump, 'r') as f:
        for line in f.readlines():
            parts = line.split(',')

            idx = int(parts[0], 16)
            begin = int(parts[1], 16)
            data = parts[2]

            store["%08x" % idx + "-" + "%08x" % begin] = data

        with open(result, 'wb') as output:
            for s in sorted(store.keys()):
                bytes = store[s].split(':')
                for byte in bytes:
                    output.write(chr(int(byte, 16)))

    print "[-] Finished! File is extract to %s" % result

if __name__ == '__main__':
    main()
