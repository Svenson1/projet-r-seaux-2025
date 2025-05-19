from Packet import Packet


class Router:
    def __init__(self, router_id):
        self.router_id = router_id
        self.neighbors = {} # Dictionaire des routeurs voisins (sous forme router: link)
        self.routing_table = {
            router_id: (0, router_id)}  # table de routage contenant la destination: le cout, le prochain saut

    def add_neighbor(self, neighbor_router, link):
        self.neighbors[neighbor_router] = link
        self.routing_table[neighbor_router.router_id] = (link.cost, neighbor_router.router_id) #lorsque l'on ajoute un voisi,
        #on met à jour la table de routage avec le cout et le prochain saut (comme on vient de l'ajouet, le cout minimum est le lien)

    def send_packet_to_neighbors(self, simulator, current_time):

        vector = {} # Dictionnaire contenant le vecteur de distance sous la forme destination: cout

        for dest, (cost, next_hop) in self.routing_table.items():
            vector[dest] = cost

        """Envoie le vecteur de distance à tous les voisins"""
        for neighbor_router, link in self.neighbors.items():
            # Envoie le vecteur de distance au voisin
            packet = Packet(self.router_id, neighbor_router.router_id, vector)
            packet_size = packet.size()
            # Calcule le temps d'arrivée du paquet
            arrival_time = current_time + link.delay(packet_size)
            print("On va envoyer a packet à :" + str(neighbor_router.router_id) + " avec un cout de : " + str(link.cost) + " et un temps d'arrivée de : " + str(arrival_time) + "depuis le routeur : " + str(self.router_id))
            simulator.add_event(arrival_time,lambda neighbor = neighbor_router, pkt = packet, at =arrival_time : neighbor.receive_packet(self, pkt,simulator, at))



    def receive_packet(self, sender_router, packet, simulator, arrival_time):
        """Reçcoit le vecteur de distance d'un voisin et mets a jour sa table si necessaire"""
        print(f"Router {self.router_id} received packet from {sender_router.router_id} at time {arrival_time}")
        updated = False
        link = self.neighbors[sender_router]
        cost_to_neighbor = link.cost

        for dest_id, costToDestFromSender in packet.vector.items():
            #si le cout est inferieur au cout actuel, on met à jour la table de routage
            new_cost = cost_to_neighbor + costToDestFromSender
            current_entry = self.routing_table.get(dest_id)
            print(f"Router {self.router_id} checking destination {dest_id}: current cost {current_entry}, new cost {new_cost}")
            #if current_entry[1] == sender_router.router_id and new_cost > current_entry[0]:
                #signifie que l'on a eu un changement de cout sur le lien


            if current_entry is None or new_cost < current_entry[0]:
                # Met à jour la table de routage
                print(f"Router {self.router_id} updating routing table for destination {dest_id}: new cost {new_cost}, next hop {sender_router.router_id}")
                self.routing_table[dest_id] = (new_cost, sender_router.router_id)
                updated = True
        if updated:
            # Si la table de routage a été mise à jour, envoie le vecteur de distance à tous les voisins
            print(f"Router {self.router_id} updated routing table")
            self.send_packet_to_neighbors(simulator, arrival_time)

    def print_routing_table(self):
        print(f"Routing table for router {self.router_id}:")
        for dest, (cost, next_hop) in self.routing_table.items():
            print(f"Destination: {dest}, Cost: {cost}, Next hop: {next_hop}")


