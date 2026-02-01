import numpy as np
import elastica as ea
from collections import defaultdict
import pickle

# --- INLINED TEMPLATES ---
from collections import defaultdict


class BaseSimulator(
    ea.BaseSystemCollection,
    ea.Constraints,
    ea.Connections,  # Added Connections for joints
    ea.Forcing,
    ea.Damping,
    ea.CallBacks,
):
    """
    Base simulator class combining all necessary PyElastica modules.
    """
    pass


def create_simulator():
    """Creates a new simulator instance."""
    return BaseSimulator()


def make_rod(
    sim,
    *,
    n_elem: int,
    length: float,
    radius: float,
    density: float,
    youngs_modulus: float,
    start=(0.0, 0.0, 0.0),
    direction=(0.0, 0.0, 1.0),
    normal=(0.0, 1.0, 0.0),
    poisson_ratio=0.5,
):
    """
    Creates a straight Cosserat rod and adds it to the simulator.
    """
    shear_modulus = youngs_modulus / (poisson_ratio + 1.0)

    rod = ea.CosseratRod.straight_rod(
        n_elem,
        np.array(start),
        np.array(direction),
        np.array(normal),
        length,
        radius,
        density,
        youngs_modulus=youngs_modulus,
        shear_modulus=shear_modulus,
    )

    sim.append(rod)
    return rod


# --- Boundary Conditions ---

def clamp_start(sim, rod):
    """Fixes the starting end of the rod (position and rotation)."""
    sim.constrain(rod).using(
        ea.OneEndFixedBC,
        constrained_position_idx=(0,),
        constrained_director_idx=(0,),
    )


def clamp_end(sim, rod):
    """Fixes the final end of the rod (position and rotation)."""
    sim.constrain(rod).using(
        ea.OneEndFixedBC,
        constrained_position_idx=(-1,),
        constrained_director_idx=(-1,),
    )


def fix_node(sim, rod, index):
    """Fixes a specific node index of the rod."""
    sim.constrain(rod).using(
        ea.OneEndFixedBC,
        constrained_position_idx=(index,),
        constrained_director_idx=(index,),
    )


# --- Forcing ---

def add_gravity(sim, rod, g=9.81, direction=(0.0, 0.0, -1.0)):
    """Adds gravity force to the rod."""
    acc_gravity = np.array(direction) * g
    sim.add_forcing_to(rod).using(
        ea.GravityForces,
        acc_gravity=acc_gravity,
    )


def add_endpoint_force(sim, rod, force, ramp_up_time=0.0):
    """
    Adds a force to the endpoint of the rod.

    Args:
        force: (3,) array specifying force vector
        ramp_up_time: Time to ramp up the force
    """
    sim.add_forcing_to(rod).using(
        ea.EndpointForces,
        0.0 * np.array(force),
        np.array(force),
        ramp_up_time=ramp_up_time,
    )


# --- Connections ---

def connect_rods(sim, rod_one, rod_two, index_one=-1, index_two=0, k=1e5, nu=0.0):
    """
    Connects two rods using a FixedJoint (spherical joint behavior if rotation not constrained, 
    but FixedJoint usually implies rigid connection).

    Args:
        index_one: Element index on first rod (default: last)
        index_two: Element index on second rod (default: first)
        k: Spring constant for joint
        nu: Damping for joint
    """
    sim.connect(rod_one, rod_two).using(
        ea.FixedJoint,
        k=k,
        nu=nu,
        kt=k,  # Rotational stiffness
        nut=nu,  # Rotational damping
        pinned_element_index=index_one,
        v_index=index_two,
    )


# --- Damping ---

def add_damping(sim, rod, damping_constant, time_step):
    """Adds analytical linear damping to the rod."""
    sim.dampen(rod).using(
        ea.AnalyticalLinearDamper,
        damping_constant=damping_constant,
        time_step=time_step,
    )


# --- Callbacks / Data Collection ---

class GenericRodCallBack(ea.CallBackBaseClass):
    """
    Callback to record time, position, velocity, and directors.
    """

    def __init__(self, step_skip: int, callback_params: dict):
        ea.CallBackBaseClass.__init__(self)
        self.every = step_skip
        self.callback_params = callback_params

    def make_callback(self, system, time, current_step):
        if current_step % self.every == 0:
            self.callback_params["time"].append(time)
            self.callback_params["position"].append(
                system.position_collection.copy())
            # self.callback_params["velocity"].append(system.velocity_collection.copy())
            # self.callback_params["directors"].append(system.director_collection.copy())


def record_history(sim, rod, step_skip=100):
    """
    Attaches a callback to record the rod's history.
    Returns a dictionary list that will be populated during simulation.
    """
    history = defaultdict(list)
    sim.collect_diagnostics(rod).using(
        GenericRodCallBack, step_skip=step_skip, callback_params=history
    )
    return history


# --- Simulation Loop ---

def finalize_and_integrate(
    sim,
    *,
    final_time: float,
    total_steps: int,
):
    """Finalizes the simulator and runs the integration loop."""
    sim.finalize()
    timestepper = ea.PositionVerlet()
    ea.integrate(timestepper, sim, final_time, total_steps)


# --- GENERATED SIMULATION CODE ---
def main():
    # 1. Setup Simulator
    sim = create_simulator()

    # 2. Create Objects
    rods = []
    # Rod 0 (soft_biological_tissue)
    rod_0 = make_rod(
        sim,
        n_elem=10,
        length=1.0,
        radius=0.01,
        density=1000,
        youngs_modulus=10000.0,
        poisson_ratio=0.5,
        start=[0.0, 0.0, 0.0],
        direction=[0.0, 0.0, 1.0],
        normal=[0.0, 1.0, 0.0]
    )
    rods.append(rod_0)
    clamp_start(sim, rod_0)
    add_gravity(sim, rod_0, g=1.0, direction=[0, 0, -9.81])
    add_endpoint_force(sim, rod_0, force=[5, 0, 0], ramp_up_time=0.1)
    add_damping(sim, rod_0, damping_constant=0.1, time_step=1e-4)

    # 3. Setup Diagnostics
    history_list = []
    for rod in rods:
        history_list.append(record_history(sim, rod, step_skip=200))

    # 4. Run Simulation
    final_time = 5
    dt = 1e-4
    total_steps = int(final_time / dt)
    print(f'Running simulation for {final_time}s ({total_steps} steps)...')
    finalize_and_integrate(sim, final_time=final_time, total_steps=total_steps)

    # 5. Save Results
    print('Saving results to simulation_data.pkl...')
    data = {'rods': history_list, 'metadata': {'fps': 30}}
    with open('simulation_data.pkl', 'wb') as f:
        pickle.dump(data, f)
    print('Done.')

if __name__ == '__main__':
    main()