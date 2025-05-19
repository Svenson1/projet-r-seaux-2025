from src.Packet import Packet


class Router:
    def __init__(self, router_id):
        self.router_id = router_id
        self.neighbors = {}  # {neighbor_router: link}
        self.routing_table = {router_id: (0, router_id)}  # Dx: {dest: (cost, next_hop)}
        self.neighbor_vectors = {}  # Dv: {neighbor_id: {dest: cost}}

    def add_neighbor(self, neighbor_router, link):
        self.neighbors[neighbor_router] = link
        self.routing_table[neighbor_router.router_id] = (link.cost, neighbor_router.router_id)
        self.neighbor_vectors[neighbor_router.router_id] = {}

    def send_distance_vector(self, simulator, current_time):
        vector = {dest: cost for dest, (cost, _) in self.routing_table.items()}
        for neighbor, link in self.neighbors.items():
            print(f"[{current_time:.2f}] Router {self.router_id} envoie à {neighbor.router_id} : {vector}")
            packet = Packet(self.router_id, neighbor.router_id, vector)
            arrival_time = current_time + link.delay(packet.size())
            simulator.add_event(arrival_time, lambda n=neighbor, p=packet, t=arrival_time: n.receive_packet(self, p, simulator, t))

    def receive_packet(self, sender_router, packet, simulator, arrival_time):
        sender_id = sender_router.router_id
        print(f"[{arrival_time:.2f}] Router {self.router_id} reçoit de {sender_id} : {packet.vector}")
        self.neighbor_vectors[sender_id] = packet.vector
        updated = self.bellman_ford()
        if updated:
            print(f"[{arrival_time:.2f}] Router {self.router_id} met à jour sa table de routage.")
            self.send_distance_vector(simulator, arrival_time)

    def bellman_ford(self):
        """Algorithme de Bellman-Ford pour mettre à jour la table de routage"""
        updated = False
        new_table = {self.router_id: (0, self.router_id)}

        for dest in self.all_known_destinations():
            if dest == self.router_id:
                continue  # On saute soi-même, déjà géré

            min_cost = float('inf')
            next_hop = None

            for neighbor, link in self.neighbors.items():
                neighbor_vector = self.neighbor_vectors.get(neighbor.router_id, {})
                if dest in neighbor_vector:
                    total_cost = neighbor_vector[dest] + link.cost
                    if total_cost < min_cost:
                        min_cost = total_cost
                        next_hop = neighbor.router_id

            if next_hop is not None:
                new_table[dest] = (min_cost, next_hop)

        # Comparaison de la table
        if new_table != self.routing_table:
            self.routing_table = new_table
            updated = True

        return updated

    def all_known_destinations(self):
        destinations = set()
        for vector in self.neighbor_vectors.values():
            destinations.update(vector.keys())
        destinations.update(self.routing_table.keys())
        return destinations

    def update_link_cost(self, neighbor_router, new_cost, simulator, current_time):
        if neighbor_router not in self.neighbors:
            return
        print(
            f"[{current_time:.2f}] Router {self.router_id} change coût du lien avec {neighbor_router.router_id} → {new_cost}")
        self.neighbors[neighbor_router].cost = new_cost
        updated = self.bellman_ford()
        if updated:
            print(f"[{current_time:.2f}] Router {self.router_id} met à jour sa table après changement de coût.")
            self.print_routing_table()
            self.send_distance_vector(simulator, current_time)

    def print_routing_table(self):
        print(f"Routing table for router {self.router_id}:")
        for dest, (cost, next_hop) in self.routing_table.items():
            print(f"  {dest} → cost: {cost}, via: {next_hop}")