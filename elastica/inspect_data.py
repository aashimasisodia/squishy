import pickle
import sys
import os

filename = "axial_stretching_data.dat"
if not os.path.exists(filename):
    print(f"File {filename} does not exist.")
    sys.exit(1)

with open(filename, "rb") as f:
    data = pickle.load(f)

print(f"Type of data: {type(data)}")
try:
    print(f"Dir of data: {dir(data)}")
    if hasattr(data, 'position_collection'):
        print(f"Position collection shape: {data.position_collection.shape}")
except Exception as e:
    print(f"Error inspecting data: {e}")
