import json

def load_topology(topology_file):
    with open(topology_file, 'r') as f:
        data = json.load(f)

    links_data = data['links']
    events_data = data['events']


    return links_data, events_data
