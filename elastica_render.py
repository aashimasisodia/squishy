import pickle
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
import sys
import os


def main():
    filename = "axial_stretching_data.dat"

    if not os.path.exists(filename):
        print(f"File {filename} not found.")
        print("Please run elastica_tutorial.py first to generate the data.")
        return

    print(f"Loading data from {filename}...")
    with open(filename, "rb") as f:
        data = pickle.load(f)

    if "rod_history" not in data:
        print("Error: 'rod_history' key not found in data.")
        print("Please ensure you have run the modified elastica_tutorial.py that saves the full rod history.")
        return

    history = data["rod_history"]
    times = data["time"]

    n_steps = len(history)
    print(f"Loaded {n_steps} time steps.")

    # Determine bounds for plotting
    all_pos = np.array(history)  # Shape: (n_steps, 3, n_nodes)

    min_vals = np.min(all_pos, axis=(0, 2))
    max_vals = np.max(all_pos, axis=(0, 2))

    # Add some margin
    ranges = max_vals - min_vals
    max_range = np.max(ranges)
    if max_range == 0:
        max_range = 1.0

    mid_vals = (max_vals + min_vals) / 2

    # Create figure
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Set equal aspect ratio manually by setting limits
    # This ensures the rod doesn't look distorted
    ax.set_xlim(mid_vals[0] - max_range/2, mid_vals[0] + max_range/2)
    ax.set_ylim(mid_vals[1] - max_range/2, mid_vals[1] + max_range/2)
    ax.set_zlim(mid_vals[2] - max_range/2, mid_vals[2] + max_range/2)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Axial Stretching Animation')

    line, = ax.plot([], [], [], 'o-', lw=2, markersize=4)

    time_text = ax.text2D(0.05, 0.95, '', transform=ax.transAxes)

    def init():
        line.set_data([], [])
        line.set_3d_properties([])
        time_text.set_text('')
        return line, time_text

    def update(frame):
        current_pos = history[frame]
        # current_pos is (3, n_nodes)
        line.set_data(current_pos[0], current_pos[1])
        line.set_3d_properties(current_pos[2])
        time_text.set_text(f'Time: {times[frame]:.2f} s')
        return line, time_text

    print("Creating animation...")
    # Use interval=30ms for smooth playback
    ani = animation.FuncAnimation(
        fig, update, frames=n_steps, init_func=init, blit=False, interval=30)

    print("Displaying animation. Close the window to exit.")
    plt.show()


if __name__ == "__main__":
    main()
