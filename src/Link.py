class Link:
    def __init__(self, router1, router2, bandwidth, propagation_speed, distance):
        self.router1 = router1 #premier router
        self.router2 = router2 #second router
        self.bandwidth = bandwidth #debit de transmission
        self.propagation_speed = propagation_speed #vitesse de propagation
        self.distance = distance #distance entre les deux routeurs

    def delay(self, packet_size):
        """Calcul le temps de transmission d'un paquet sur le lien"""
        transmission_delay = packet_size / self.bandwidth
        propagation_delay = self.distance / self.propagation_speed
        return transmission_delay + propagation_delay

    def other_side(self, router):
        """Retourne l'autre routeur du lien"""
        if router == self.router1:
            return self.router2
        elif router == self.router2:
            return self.router1
        else:
            raise ValueError("Router not connected to this link")
