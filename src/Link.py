class Link:
    def __init__(self, router1, router2, bandwidth, propagation_speed, distance, cost):
        self.router1 = router1 #premier router
        self.router2 = router2 #second router
        self.bandwidth = bandwidth #debit de transmission
        self.propagation_speed = propagation_speed #vitesse de propagation
        self.distance = distance #distance entre les deux routeurs
        self.cost = cost #cout du lien

    def delay(self, packet_size):
        """Calcul le temps de transmission d'un paquet sur le lien"""
        transmission_delay = packet_size * 8 / self.bandwidth
        propagation_delay = self.distance / self.propagation_speed
        return transmission_delay + propagation_delay

    def update_cost(self, new_cost):
        """Met à jour le coût du lien"""
        self.cost = new_cost
