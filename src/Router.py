class Router:
    def __init__(self, router_id):
        self.router_id = router_id
        self.neighbors = {} # Dictionaire des routeurs voisins (sous forme router: link)
        self.routing_table = {} # table de routage contenant la destination: le cout, le prochain saut

    def add_neighbor(self, neighbor_router, link):
        self.neighbors[neighbor_router] = link
        self.routing_table[neighbor_router.router_id] = (link.cost, neighbor_router.router_id) #lorsque l'on ajoute un voisi,
        #on met à jour la table de routage avec le cout et le prochain saut (comme on vient de l'ajouet, le cout minimum est le lien)
