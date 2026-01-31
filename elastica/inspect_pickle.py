import pickle
import sys
import os

def inspect():
    filename = "simulation_data.dat"
    if len(sys.argv) > 1:
        filename = sys.argv[1]

    if not os.path.exists(filename):
        print(f"File {filename} not found.")
        return

    try:
        with open(filename, "rb") as f:
            data = pickle.load(f)
            print(f"Successfully loaded {filename}!")
            
            if isinstance(data, dict):
                print("Keys:", list(data.keys()))
                if "rods" in data:
                    print(f"Contains {len(data['rods'])} rod histories.")
                if "metadata" in data:
                    print("Metadata:", data["metadata"])
            else:
                print("Data is not a dictionary:", type(data))

    except Exception as e:
        print(f"Error loading pickle: {e}")

if __name__ == "__main__":
    inspect()
