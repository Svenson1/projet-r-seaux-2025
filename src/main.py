from topology_loader import load_topology


def start_simulation(_routers, _simulator):
    # Envoi du vecteur de distance initial
    for r in _routers.values():
        r.send_packet_to_neighbors(_simulator, 0)


if __name__ == '__main__':
    print("===== Topology Selection =====")
    print("1. Validation de votre implémentation")
    print("2. Impact des délais")
    print("3. Comptage à l’infini")
    print("4. Solution du problème de comptage à l’infini")
    choice = input("choose your topology: \n")
    file = {"1":"simple_case.json", "2":"impact_of_delay.json", "3": "count_to_infinity.json", "4": "topology4.json"}

    simulator, routers, links = load_topology(file[choice])
    start_simulation(routers, simulator)
    simulator.run()

    print("\n===== Final Routing Tables =====")
    for router in sorted(routers.values(), key=lambda r: r.router_id):
        router.print_routing_table()
        print()







