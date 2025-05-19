from Simulator import Simulator
from Router import Router
from Link import Link
from src.Simulator import SimulatorEvent
from topology_loader import load_topology

simulator = Simulator()

links_data, events_data = load_topology("topology1.json")

routers = {}
links = {}

#création des routeurs
for link in links_data:
   id1, id2 = link["endpoints"]
   for router_id in [id1, id2]:
       if router_id not in routers:
           routers[router_id] = Router(router_id)


#création des liens
for link in links_data:
    id1, id2 = link["endpoints"]
    router1 = routers[id1]
    router2 = routers[id2]

    temp_link = Link(router1, router2, link["trans_speed"], link["prop_speed"], link["dist"], link["bandwidth"])

    # Stocker les liens dans un dictionnaire avec les IDs triés pour éviter les doublons (1,2) == (2,1)
    links[tuple(sorted((id1, id2)))] = temp_link

    router1.add_neighbor(router2, temp_link)
    router2.add_neighbor(router1, temp_link)

def update_cost(_link, new_cost, current_time):
    _link.update_cost(new_cost)
    _link.router1.send_packet_to_neighbors(simulator, current_time)
    _link.router2.send_packet_to_neighbors(simulator, current_time)


#création des events
for event in events_data:
    id1, id2 = event["link"]
    link_key = tuple(sorted((id1, id2)))
    if link_key in links:
        link1 = links[link_key]
        simulator_event = SimulatorEvent(1, update_cost(link1, event["new_cost"], event["time"]))
        simulator.add_event(event["time"], lambda: simulator_event)
