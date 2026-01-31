import pickle
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
import sys
import os

def main():
    # Default filename, can be overridden by command line argument
    filename = "simulation_data.pkl"
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    
    # Fallback for the tutorial
    if not os.path.exists(filename) and os.path.exists("simulation_data.dat"):
        filename = "simulation_data.dat"

    if not os.path.exists(filename):
        print(f"File {filename} not found.")
        print("Please run the simulation script first to generate the data.")
        return

    print(f"Loading simulation data from {filename}...")
    with open(filename, "rb") as f:
        data = pickle.load(f)

    # Check for expected data structure
    if "rods" not in data:
        print("Error: 'rods' key not found in data.")
        print("Expected format: {'rods': [{'time': [], 'position': []}, ...], 'metadata': {...}}")
        return
    
    rods_history = data["rods"]
    metadata = data.get("metadata", {})
    fps = metadata.get("fps", 30)
    
    if not rods_history:
        print("No rod history found.")
        return

    # Assuming all rods have the same time steps
    times = rods_history[0]["time"]
    n_steps = len(times)
    print(f"Loaded {len(rods_history)} rods with {n_steps} frames.")

    # Determine bounds for plotting (consider all rods)
    all_pos_list = []
    for history in rods_history:
        # history["position"] is a list of (3, n_nodes) arrays
        # Convert to a single array for this rod: (n_steps, 3, n_nodes)
        rod_pos = np.array(history["position"])
        all_pos_list.append(rod_pos)
    
    # Concatenate all positions to find global min/max
    # Shape: (n_rods * n_steps * n_nodes, 3) - flattened for easier min/max
    # Or just iterate
    min_vals = np.array([np.inf, np.inf, np.inf])
    max_vals = np.array([-np.inf, -np.inf, -np.inf])

    for rod_pos in all_pos_list:
        # rod_pos shape: (n_steps, 3, n_nodes)
        current_min = np.min(rod_pos, axis=(0, 2))
        current_max = np.max(rod_pos, axis=(0, 2))
        min_vals = np.minimum(min_vals, current_min)
        max_vals = np.maximum(max_vals, current_max)
    
    # Add some margin
    ranges = max_vals - min_vals
    max_range = np.max(ranges)
    if max_range == 0:
        max_range = 1.0
        
    mid_vals = (max_vals + min_vals) / 2
    
    # Create figure
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    ax.set_xlim(mid_vals[0] - max_range/2, mid_vals[0] + max_range/2)
    ax.set_ylim(mid_vals[1] - max_range/2, mid_vals[1] + max_range/2)
    ax.set_zlim(mid_vals[2] - max_range/2, mid_vals[2] + max_range/2)
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Elastica Simulation Animation')
    
    # Create lines for each rod
    lines = []
    for _ in rods_history:
        line, = ax.plot([], [], [], 'o-', lw=2, markersize=2)
        lines.append(line)
        
    time_text = ax.text2D(0.05, 0.95, '', transform=ax.transAxes)
    
    def init():
        for line in lines:
            line.set_data([], [])
            line.set_3d_properties([])
        time_text.set_text('')
        return lines + [time_text]
    
    def update(frame):
        for i, line in enumerate(lines):
            current_pos = all_pos_list[i][frame] # (3, n_nodes)
            line.set_data(current_pos[0], current_pos[1])
            line.set_3d_properties(current_pos[2])
        
        time_text.set_text(f'Time: {times[frame]:.2f} s')
        return lines + [time_text]
    
    print("Creating animation...")
    # Adjust interval based on fps
    interval = 1000 / fps
    ani = animation.FuncAnimation(
        fig, update, frames=n_steps, init_func=init, blit=False, interval=interval)
    
    save_filename = "simulation.gif"
    if filename != "simulation_data.pkl":
        base_name = os.path.splitext(filename)[0]
        save_filename = f"{base_name}.gif"
        
    print(f"Saving animation to {save_filename}...")
    try:
        ani.save(save_filename, writer='pillow', fps=fps)
        print("Animation saved.")
    except Exception as e:
        print(f"Failed to save animation: {e}")
        
    # plt.show()

if __name__ == "__main__":
    main()
