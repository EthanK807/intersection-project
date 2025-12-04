
            # filles lanes with cars


            for road in network.road_segments:
                if len(road.spawn_nodes) > 0:
                    for spawn_node in road.spawn_nodes:
                        if (random.random() < spawn_node.spawn_chance):
                            spawned_car = car(spawn_node, np.random.normal(3, 0.25))
                            arrival_node = None
                            while (True):
                                for spawn_node in network.road_segments.spawn_nodes:
                                    if (random.random() < spawn_node.arrival_chance):
                                        arrival_node = spawn_node
                                        break
                            assigned_route = route(spawned_car.spawn_node, arrival_node)
                            spawn_car.route = assigned_route


                    print(f"Car would spawn at {spawn_node.x}, {spawn_node.y}")
