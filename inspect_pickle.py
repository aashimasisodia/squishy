import pickle
import sys

# Define a dummy class to catch the unpickling
class SnakeSimulator:
    pass

def inspect():
    try:
        with open("butterfly_data.dat", "rb") as f:
            data = pickle.load(f)
            print("Successfully loaded!")
            print(data.keys())
            if "system" in data:
                print("System type:", type(data["system"]))
                print("System module:", data["system"].__class__.__module__)
                print("System class:", data["system"].__class__.__name__)
    except Exception as e:
        print(f"Error loading pickle: {e}")

if __name__ == "__main__":
    inspect()
