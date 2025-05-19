class Packet:
    def __init__(self, source_router_id, dest_router_id, vector):
        self.source_router_id = source_router_id
        self.dest_router_id = dest_router_id
        self.vector = vector

    def size(self):
        return len(self.vector) * 8 # 4 octets pour la clé + 4 octets pour la valeur