class Link:
    def __init__(self, router1, router2, bandwidth, propagation_speed, distance):
        self.router1 = router1 #premier router
        self.router2 = router2 #second router
        self.bandwidth = bandwidth #debit de transmission
        self.propagation_speed = propagation_speed #vitesse de propagation
        self.distance = distance #distance entre les deux routeurs

