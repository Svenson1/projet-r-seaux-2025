from Packet import Packet


class Router:
    def __init__(self, router_id):
        self.router_id = router_id # Identifiant du routeur
        self.neighbors = {}  # {neighbor_router: link}
        self.routing_table = {router_id: (0, router_id)}  # Dx: {dest: (cost, next_hop)}
        self.neighbor_vectors = {}  # Dv: {neighbor_id: {dest: cost}}

    def add_neighbor(self, neighbor_router, link):
        self.neighbors[neighbor_router] = link # Ajout du voisin et du lien
        self.routing_table[neighbor_router.router_id] = (link.cost, neighbor_router.router_id) # Coût du lien vers le voisin
        self.neighbor_vectors[neighbor_router.router_id] = {} # Initialisation du vecteur de distance du voisin

    def send_distance_vector(self, simulator, current_time):
        vector = {} # Création du vecteur de distance

        for dest, (cost, next_hop) in self.routing_table.items(): # Remplissage du vecteur de distance avec la table de routage
            vector[dest] = cost

        for neighbor, link in self.neighbors.items(): # Envoi du vecteur de distance à chaque voisin
            print(f"[{current_time:.2f}] Router {self.router_id} envoie à {neighbor.router_id} : {vector}")
            packet = Packet(self.router_id, neighbor.router_id, vector) #creation du paquet
            arrival_time = current_time + link.delay(packet.size()) #calcul du temps d'arrivée
            simulator.add_event(arrival_time, lambda n=neighbor, p=packet, t=arrival_time: n.receive_packet(self, p, simulator, t)) # Ajout de l'événement dans le simulateur

    #methode permettant de recevoir un vecteur de distance d'un voisin et de verifier si la table de routage doit être mise à jour
    def receive_packet(self, sender_router, packet, simulator, arrival_time):
        sender_id = sender_router.router_id
        print(f"[{arrival_time:.2f}] Router {self.router_id} reçoit de {sender_id} : {packet.vector}")
        self.neighbor_vectors[sender_id] = packet.vector
        updated = self.bellman_ford()
        if updated:
            print(f"[{arrival_time:.2f}] Router {self.router_id} met à jour sa table de routage.")
            self.send_distance_vector(simulator, arrival_time)

    #methode permettant le calcul de la nouvelle table de routage si il y a des changements se basant sur l'algo de Bellman-Ford
    def bellman_ford(self):
        updated = False
        new_table = {self.router_id: (0, self.router_id)}

        for dest in self.all_known_destinations(): #all_known_destinations() retourne tous les voisins connus du routeur et des voisins
            if dest == self.router_id:
                continue  # On saute soi-même

            min_cost = float('inf') #cout minimum init a infini afin de trouver le cout minimum parmi tous les voisins
            next_hop = None

            # On parcourt les voisins et on calcule le coût total pour chaque destination
            for neighbor, link in self.neighbors.items(): #on parcour tous les voisins
                neighbor_vector = self.neighbor_vectors.get(neighbor.router_id, {}) #on recupere le vecteur de distance du voisin et on renvoie un dictionnaire vide si il n'en a pas
                if dest in neighbor_vector: #si le voisin posséde deja un chemin vers la destination, on calcule le cout total et on verifie si il est inferieur au cout minimum
                    total_cost = neighbor_vector[dest] + link.cost
                    if total_cost < min_cost:
                        min_cost = total_cost
                        next_hop = neighbor.router_id

            if next_hop is not None:
                new_table[dest] = (min_cost, next_hop) #on ajoute la destination et le cout minimum a la nouvelle table de routage

        # Comparaison de la table avec celle que l'on a afin de determiner si il y a eu des changements
        if new_table != self.routing_table:
            self.routing_table = new_table
            updated = True

        return updated

    #methode permettant de recuperer toute les destinations connues par le routeur et ses voisins sans doublons
    def all_known_destinations(self):
        destinations = set()
        for vector in self.neighbor_vectors.values():
            destinations.update(vector.keys())
        destinations.update(self.routing_table.keys())
        return destinations

    #methode permettant de mettre a jour le cout d'un lien avec un voisin et de recalculer la table de routage si il y a des changements
    def update_link_cost(self, neighbor_router, new_cost, simulator, current_time):
        if neighbor_router not in self.neighbors:
            return
        print(
            f"[{current_time:.2f}] Router {self.router_id} change coût du lien avec {neighbor_router.router_id} -> {new_cost}")
        self.neighbors[neighbor_router].cost = new_cost
        updated = self.bellman_ford()
        if updated:
            print(f"[{current_time:.2f}] Router {self.router_id} met à jour sa table après changement de coût.")
            self.print_routing_table()
            self.send_distance_vector(simulator, current_time)


    #methode permettant d'afficher la table de routage du routeur
    def print_routing_table(self):
        print(f"Routing table for router {self.router_id}:")
        for dest, (cost, next_hop) in self.routing_table.items():
            print(f"  {dest} → cost: {cost}, via: {next_hop}")