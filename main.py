import matplotlib.pyplot as plt
import numpy as np
import random
import time
from enum import Enum
import math
from inspector import view_raw_data

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

            # Update traffic lights (simple toggle)

            for road in network.road_segments: # FIX: Was intersection.roads, which doesn't exist
                for lane in road.lanes:
                    r = random.random()
                    # FIX: Added 'if lane.traffic_light' to prevent crash
                    # Lanes not at an intersection won't have a light.
                    if lane.traffic_light and lane.traffic_light.color == LightColor.GREEN and r < 0.1/30:
                        lane.traffic_light.change_color(LightColor.RED) # FIX: Was .change()
                    elif lane.traffic_light and (r < 0.1/30): # FIX: Added 'if lane.traffic_light'
                        lane.traffic_light.change_color(LightColor.GREEN) # FIX: Was .change()

            time.sleep(1/30)  # wait one second per step (for realism)


if __name__ == "__main__":
    main()

