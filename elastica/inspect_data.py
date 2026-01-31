import pickle
import sys
import os
import numpy as np

filename = "simulation_data.pkl"
if len(sys.argv) > 1:
    filename = sys.argv[1]

if not os.path.exists(filename):
    print(f"File {filename} does not exist.")
    sys.exit(1)

print(f"Inspecting {filename}...")
with open(filename, "rb") as f:
    data = pickle.load(f)

print(f"Type of data: {type(data)}")

if isinstance(data, dict):
    print(f"Keys: {list(data.keys())}")
    
    if "rods" in data:
        rods = data["rods"]
        print(f"Number of rods: {len(rods)}")
        for i, rod in enumerate(rods):
            print(f"  Rod {i}:")
            if isinstance(rod, dict):
                print(f"    Keys: {list(rod.keys())}")
                if "time" in rod:
                    print(f"    Time steps: {len(rod['time'])}")
                if "position" in rod:
                    pos = np.array(rod['position'])
                    print(f"    Position shape: {pos.shape}")
            else:
                print(f"    Type: {type(rod)}")
                
    if "metadata" in data:
        print(f"Metadata: {data['metadata']}")

else:
    print("Data is not a dictionary.")
    print(data)
