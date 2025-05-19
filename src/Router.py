from src.Packet import Packet


class Router:
    def __init__(self, router_id):
        self.router_id = router_id
        self.neighbors = {} # Dictionaire des routeurs voisins (sous forme router: link)
        self.routing_table = {} # table de routage contenant la destination: le cout, le prochain saut
        self.routing_table[router_id] = (0, router_id) # la table de routage contient le cout 0 pour lui même et le prochain saut est lui même

    def add_neighbor(self, neighbor_router, link):
        self.neighbors[neighbor_router] = link
        self.routing_table[neighbor_router.router_id] = (link.cost, neighbor_router.router_id) #lorsque l'on ajoute un voisi,
        #on met à jour la table de routage avec le cout et le prochain saut (comme on vient de l'ajouet, le cout minimum est le lien)

    def send_packet_to_neighbors(self, simulator, current_time):

        vector = {}

        for dest, (cost, next_hop) in self.routing_table.items():
            vector[dest] = cost

        """Envoie le vecteur de distance à tous les voisins"""
        for neighbor_router, link in self.neighbors.items():
            # Envoie le vecteur de distance au voisin
            packet = Packet(self.router_id, neighbor_router.router_id, vector)
            packet_size = packet.size()
            # Calcule le temps d'arrivée du paquet
            arrival_time = current_time + link.delay(packet_size)
            simulator.add_event(arrival_time,lambda neighbor = neighbor_router : neighbor.receive_packet(self, packet,simulator,  arrival_time))

    def receive_packet(self, sender_router, packet, simulator, arrival_time):
        """Reçcoit le vecteur de distance d'un voisin et mets a jour sa table si necessaire"""
        updated = False
        link = self.neighbors[sender_router]
        cost_to_neighbor = link.cost

        for dest_id, costToDest in packet.vector.items():
            #si le cout est inferieur au cout actuel, on met à jour la table de routage
            new_cost = cost_to_neighbor + costToDest
            current_entry = self.routing_table.get(dest_id)
            if current_entry is None or new_cost < current_entry[0]:
                self.routing_table[dest_id] = (new_cost, sender_router.router_id)
                updated = True
        if updated:
            self.send_packet_to_neighbors(simulator, arrival_time)

    def print_routing_table(self):
        print(f"Routing table for router {self.router_id}:")
        for dest, (cost, next_hop) in self.routing_table.items():
            print(f"Destination: {dest}, Cost: {cost}, Next hop: {next_hop}")
