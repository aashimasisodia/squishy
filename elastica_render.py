import pickle
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
import sys
import os
import elastica as ea

# Define the Simulator class (must inherit from BaseSystemCollection and CallBacks)
class ButterflySimulator(ea.BaseSystemCollection, ea.CallBacks):
    pass

class SnakeSimulator(
    ea.BaseSystemCollection,
    ea.Constraints,
    ea.Forcing,
    ea.Damping,
    ea.CallBacks,
    ea.Contact,
):
    pass

class RenderingCallBack(ea.CallBackBaseClass):
    """
    Call back function for recording simulation history
    """
    def __init__(self, step_skip: int, callback_params: dict) -> None:
        ea.CallBackBaseClass.__init__(self)
        self.every = step_skip
        self.callback_params = callback_params

    def make_callback(
        self, system: ea.typing.RodType, time: np.float64, current_step: int
    ) -> None:

        if current_step % self.every == 0:
            self.callback_params["time"].append(time)
            self.callback_params["position"].append(system.position_collection.copy())
            return

def main():
    filename = "butterfly_data.dat"

    if not os.path.exists(filename):
        print(f"File {filename} not found.")
        print("Please run elastica_tutorial.py first to generate the data.")
        return

    print(f"Loading system configuration from {filename}...")
    with open(filename, "rb") as f:
        data = pickle.load(f)

    if "rod" not in data:
        print("Error: 'rod' object not found in data.")
        return
    
    rod = data["rod"]
    final_time = data.get("final_time", 10.0)
    dl = data.get("dl", 1.0) # Default if not found
    
    # Try to find time step
    if "time_step" in data:
        dt = data["time_step"]
    elif "dt" in data:
        dt = data["dt"]
    else:
        dt = 0.01 * dl
    
    # Reconstruct the simulation environment
    print("Setting up simulation...")
    
    if "features" in data:
        print("Reconstructing system from features list...")
        butterfly_sim = SnakeSimulator() # Use SnakeSimulator as it has all mixins
        
        # Add main rod
        butterfly_sim.append(rod)
        
        # Add auxiliary systems (like planes)
        if "auxiliary_systems" in data:
            for aux_sys in data["auxiliary_systems"]:
                butterfly_sim.append(aux_sys)
                
        # Apply features
        for feature in data["features"]:
            f_type = feature["type"]
            cls = feature["class"]
            kwargs = feature["kwargs"]
            
            if f_type == "forcing":
                target = feature["target"]
                butterfly_sim.add_forcing_to(target).using(cls, **kwargs)
            elif f_type == "contact":
                sys1 = feature["system_one"]
                sys2 = feature["system_two"]
                butterfly_sim.detect_contact_between(sys1, sys2).using(cls, **kwargs)
            elif f_type == "damping":
                target = feature["target"]
                butterfly_sim.dampen(target).using(cls, **kwargs)
            elif f_type == "constraint":
                target = feature["target"]
                butterfly_sim.constrain(target).using(cls, **kwargs)
            else:
                print(f"Unknown feature type: {f_type}")

    elif "system" in data:
        print("Using pre-configured system from data file (legacy mode).")
        butterfly_sim = data["system"]
    else:
        print("Constructing new default simulation system.")
        butterfly_sim = ButterflySimulator()
        butterfly_sim.append(rod)
    
    # Setup recording
    recorded_history = ea.defaultdict(list)
    # Record initial state
    recorded_history["time"].append(0.0)
    recorded_history["position"].append(rod.position_collection.copy())
    
    # Add callback
    # Adjust step_skip as needed. 
    # If dt is small, we might want to skip more steps to keep animation manageable.
    step_skip = 100 
    butterfly_sim.collect_diagnostics(rod).using(
        RenderingCallBack, step_skip=step_skip, callback_params=recorded_history
    )
    
    butterfly_sim.finalize()
    
    # Setup time stepper
    timestepper = ea.PositionVerlet()
    # dt is already set above
    # total_steps = int(final_time / dt)
    # The saved final_time is usually large for Snake (22.0), and dt is small (1e-4)
    # total_steps would be ~220,000. This might take a while.
    total_steps = int(final_time / dt)

    print(f"Starting simulation: Final time={final_time}, dt={dt}, Steps={total_steps}")
    
    # Run simulation
    ea.integrate(timestepper, butterfly_sim, final_time, total_steps)
    
    print("Simulation complete.")
    
    # Now render the results
    history = recorded_history["position"]
    times = recorded_history["time"]
    n_steps = len(history)
    print(f"Recorded {n_steps} frames.")

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
    
    ax.set_xlim(mid_vals[0] - max_range/2, mid_vals[0] + max_range/2)
    ax.set_ylim(mid_vals[1] - max_range/2, mid_vals[1] + max_range/2)
    ax.set_zlim(mid_vals[2] - max_range/2, mid_vals[2] + max_range/2)
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Butterfly Rod Animation')
    
    line, = ax.plot([], [], [], 'o-', lw=2, markersize=4)
    time_text = ax.text2D(0.05, 0.95, '', transform=ax.transAxes)
    
    def init():
        line.set_data([], [])
        line.set_3d_properties([])
        time_text.set_text('')
        return line, time_text
    
    def update(frame):
        current_pos = history[frame]
        line.set_data(current_pos[0], current_pos[1])
        line.set_3d_properties(current_pos[2])
        time_text.set_text(f'Time: {times[frame]:.2f} s')
        return line, time_text
    
    print("Creating animation...")
    # Adjust interval for playback speed
    ani = animation.FuncAnimation(
        fig, update, frames=n_steps, init_func=init, blit=False, interval=30)
    
    save_filename = "butterfly_simulation.gif"
    print(f"Saving animation to {save_filename}...")
    try:
        ani.save(save_filename, writer='pillow', fps=30)
        print("Animation saved.")
    except Exception as e:
        print(f"Failed to save animation: {e}")
        
    # plt.show()

if __name__ == "__main__":
    main()
