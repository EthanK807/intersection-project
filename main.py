import matplotlib.pyplot as plt
import numpy as np
import random
import time
from enum import Enum
import math

class Direction(Enum):
    LEFT = "LEFT"
    RIGHT = "RIGHT"
    STRAIGHT = "STRAIGHT"

class LightColor(Enum):
    RED = "RED"
    GREEN = "GREEN"
    YELLOW = "YELLOW"




def main():
    def simulate(network, steps=300):
        for t in range(steps):
            print(f"\n--- Time step {t} ---")

            # filles lanes with cars


            for road in network.road_segments:
                if len(road.spawn_nodes) > 0:
                    for spawn_node in road_segment.spawn_nodes:
                        if (random.random() < spawn_node.spawn_chance):
                            spawned_car = car(spawn_node, np.random.normal(3, 0.25))
                            # --- This is how you'd spawn a car ---
                            # 1. Pick a random spawn node from the road
                            # 2. Figure out a route (This is complex, placeholder for now)
                            # route = Route(spawn_node, ...)
                            arrival_node = None
                            while (True):
                                for spawn_node in network.road_segments.spawn_nodes:
                                    if (random.random() < spawn_node.arrival_chance):
                                        arrival_node = spawn_node
                                        break
                            assigned_route = route(spawned_car.spawn_node, arrival_node)
                            spawn_car.route = assigned_route


                    print(f"Car would spawn at {spawn_node.x}, {spawn_node.y}")


            # Update traffic lights (simple toggle)

            for road in intersection.road_segments: # FIX: Was intersection.roads, which doesn't exist
                for lane in road.lanes:
                    # FIX: Added 'if lane.traffic_light' to prevent crash
                    # Lanes not at an intersection won't have a light.
                    if lane.traffic_light and lane.traffic_light.color == LightColor.GREEN and r < 0.1/30:
                        lane.traffic_light.change_color(LightColor.RED) # FIX: Was .change()
                    elif lane.traffic_light and (r < 0.1/30): # FIX: Added 'if lane.traffic_light'
                        lane.traffic_light.change_color(LightColor.GREEN) # FIX: Was .change()

            # Move vehicles if light is green
            for road in intersection.road_segments: # FIX: Was intersection.roads
                for lane in road.lanes:
                    # FIX: 'len(lane.queue)' is correct syntax.
                    # FIX: Added 'if lane.traffic_light'
                    if lane.traffic_light and lane.traffic_light.color == LightColor.GREEN and len(lane.queue) != 0:
                        car = lane.vehicles.pop(0)  # car leaves the lane
                        print(f"{car} passed through {road.name} going {lane.direction}")

            # moves the cars through the intersection
            for road in intersection.road_segments: # FIX: Was intersection.roads
                for lane in road.lanes: # FIX: Was roads.lanes
                    for cars in lane.queue: # FIX: Was lanes.queue
                        pass # Added 'pass' to make the loop valid


            time.sleep(.0333)  # wait one second per step (for realism)


if __name__ == "__main__":
    main()

