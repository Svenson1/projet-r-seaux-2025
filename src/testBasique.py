from src.Simulator import Simulator
from src.Router import Router
from src.Link import Link

simulator = Simulator()

prop_speed = 5e6  # m/s
trans_speed = 1e19  # bps
dist = 1e3  # m

#routeur :
A = Router(1)
B = Router(2)
C = Router(3)

#lien entre les routeurs
AB = Link(A, B, trans_speed, prop_speed, dist, 7)
AC = Link(A, C, trans_speed, prop_speed, dist, 4)

#Connecter les routeurs
A.add_neighbor(B, AB)
A.add_neighbor(C, AC)
B.add_neighbor(A, AB)
B.add_neighbor(C, AC)
C.add_neighbor(A, AC)
C.add_neighbor(B, AC)

# Envoi du vecteur de distance
A.send_vector_to_neighbors(simulator, 0)

simulator.run()