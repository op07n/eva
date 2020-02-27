import sys
import json

# redirect the output doing this:
# sudo asterix -i 225.45.211.2:10.45.211.50:4001 -j | python3 read.py

for line in sys.stdin:
    # print(line)
    json_line = json.loads(line[:-2])
    if 'I042' in line:
        print(json_line['CAT010']['I042'])
