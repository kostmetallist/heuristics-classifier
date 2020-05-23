#!/usr/bin/python3

# argv[1] is the file location for the JSON event data
# argv[2] (optional) is the name of heuristic procedure to use
if __name__ == '__main__':
    import json
    import sys
    from pprint import pprint 
    with open(sys.argv[1]) as jsonDataStream:
        events = json.loads(jsonDataStream.readline())
        pprint(events, indent=2)
