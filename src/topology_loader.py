import json

from Link import Link
from Router import Router
from Simulator import Simulator

def update_cost_event(_link, _new_cost, _current_time, _simulator):
    _link.update_cost(_new_cost)
    _link.router1.update_link_cost(_link.router2, _new_cost, _simulator, _current_time)
    _link.router2.update_link_cost(_link.router1, _new_cost, _simulator, _current_time)


def load_topology(topology_file):
    with open(topology_file, 'r') as f:
        data = json.load(f)

    links_data = data['links']
    events_data = data['events']

    simulator = Simulator()
    routers = {}
    links = {}

    # création des routeurs
    for link in links_data:
        id1, id2 = link["endpoints"]
        for router_id in [id1, id2]:
            if router_id not in routers:
                routers[router_id] = Router(router_id)

    # création des liens
    for link in links_data:
        id1, id2 = link["endpoints"]
        router1 = routers[id1]
        router2 = routers[id2]

        temp_link = Link(router1, router2, link["transmission_speed"], link["propagation_speed"], link["distance"],
                         link["cost"])

        # Stocker les liens dans un dictionnaire avec les IDs triés pour éviter les doublons (1,2) == (2,1)
        links[tuple(sorted((id1, id2)))] = temp_link

        router1.add_neighbor(router2, temp_link)
        router2.add_neighbor(router1, temp_link)

        # création des events
        for event in events_data:
            id1, id2 = event["link"]
            link_key = tuple(sorted((id1, id2)))
            if link_key in links:
                link1 = links[link_key]
                simulator.add_event(
                    event["time"],
                    lambda l=link1, c=event["new_cost"], t=event["time"]: update_cost_event(l, c, t, simulator)
                )


    return simulator, routers, links
