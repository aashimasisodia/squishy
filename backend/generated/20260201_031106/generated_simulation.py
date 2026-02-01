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
    nu=None,
    velocity=(0.0, 0.0, 0.0),
    omega=(0.0, 0.0, 0.0),
    dt=None,
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

    # Set initial velocity and angular velocity
    rod.velocity_collection[:] = np.array(velocity)[:, None]
    rod.omega_collection[:] = np.array(omega)[:, None]

    sim.append(rod)

    if nu is not None:
        if dt is None:
            # Fallback or warning if dt is missing but needed for damping
            # For now, we assume dt is required for AnalyticalLinearDamper
            raise ValueError(
                "dt must be provided to make_rod when damping (nu) is used.")

        sim.dampen(rod).using(
            ea.AnalyticalLinearDamper,
            damping_constant=nu,
            time_step=dt,
            order=1
        )

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
        ea.FixedConstraint,
        constrained_position_idx=(-1,),
        constrained_director_idx=(-1,),
    )


def fix_node(sim, rod, index):
    """Fixes a specific node index of the rod."""
    sim.constrain(rod).using(
        ea.FixedConstraint,
        constrained_position_idx=(index,),
        constrained_director_idx=(index,),
    )


# --- Forcing ---

class MuscleTorques(ea.NoForces):
    """
    Applies a traveling wave of torque to the rod to simulate snake locomotion.
    """

    def __init__(self, amplitude, wave_length, frequency, phase, ramp, n_elems, direction):
        super().__init__()
        self.amplitude = amplitude
        self.wave_number = 2 * np.pi / wave_length
        self.frequency = frequency
        self.phase = phase
        self.ramp = ramp
        # Direction of the torque axis (usually normal to the plane)
        self.direction = np.array(direction)

        # Pre-compute spatial phase
        # s varies from 0 to L. We assume uniform elements.
        # We need the positions of the elements (s coordinate)
        # But we don't have L here easily unless passed.
        # We'll compute s on the fly or pass L.
        # Better: pass 'rod' to init? No, Forcing init usually just takes params.
        # We can compute s in apply_forces if we assume rod is uniform.
        # Or just pass an array of 's' values.
        pass

    def apply_torques(self, system, time: float = 0.0):
        # Ramp up
        factor = 1.0
        if time < self.ramp:
            factor = time / self.ramp

        # Calculate torque profile
        # s is approximate arc length
        # lengths = system.lengths # (n_elems,)
        # s = np.cumsum(lengths) - 0.5 * lengths
        # For efficiency, we can assume uniform initial s if small deformations,
        # or recompute. Recomputing is safer.

        s = np.cumsum(system.lengths)
        s -= 0.5 * system.lengths[0]  # Center of elements
        # Normalize s? No, wave_number handles it.

        # Traveling wave: A * cos(k*s - w*t + phi)
        torque_mag = factor * self.amplitude * np.cos(
            self.wave_number * s - 2 * np.pi * self.frequency * time + self.phase
        )

        # Apply to system.external_torques
        # shape: (3, n_elems)
        # We apply torque about the 'direction' axis.
        # direction shape: (3,)

        # Broadcast direction to (3, n_elems)
        # torque_mag shape: (n_elems,)

        torques = np.outer(self.direction, torque_mag)

        system.external_torques += torques


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


def add_muscle_activity(sim, rod, amplitude, wave_length, frequency, phase, ramp, direction=(0.0, 1.0, 0.0)):
    """
    Adds muscle activity (traveling wave torque) to the rod.

    Args:
        amplitude: Wave amplitude in meters (spatial displacement). 
                   Converted to torque internally: Torque = B * k^2 * Amp.
        direction: Vector normal to the plane of motion (axis of torque).
    """
    # Compute Bending Stiffness B
    # rod.bend_matrix shape is (3, 3, n_elems-1) usually, or n_elems.
    # PyElastica stores it as (3, 3, n_elems).
    # We use the average bending stiffness.
    if hasattr(rod, "bend_matrix"):
        # Average of B_xx and B_yy
        B_mean = (np.mean(rod.bend_matrix[0, 0, :]) +
                  np.mean(rod.bend_matrix[1, 1, :])) / 2.0
    else:
        # Fallback (should not be reached for CosseratRod)
        B_mean = 1.0

    # Calculate required torque amplitude
    # Curvature Kappa = A * k^2
    # Torque = B * Kappa
    k = 2 * np.pi / wave_length
    torque_amplitude = B_mean * (k**2) * amplitude

    sim.add_forcing_to(rod).using(
        MuscleTorques,
        amplitude=torque_amplitude,
        wave_length=wave_length,
        frequency=frequency,
        phase=phase,
        ramp=ramp,
        n_elems=rod.n_elems,
        direction=direction
    )


def add_anisotropic_friction(sim, rod, static_friction, kinetic_friction, plane_normal=(0.0, 1.0, 0.0), plane_origin=(0.0, -0.025, 0.0)):
    """
    Adds anisotropic friction with a ground plane.

    Args:
        static_friction: [mu_forward, mu_backward, mu_sideways]
        kinetic_friction: [mu_forward, mu_backward, mu_sideways]
    """
    sim.add_forcing_to(rod).using(
        ea.AnisotropicFrictionalPlane,
        k=1.0,  # Wall stiffness (repulsion)
        nu=1e-6,  # Wall damping
        plane_origin=np.array(plane_origin),
        plane_normal=np.array(plane_normal),
        slip_velocity_tol=1e-6,
        static_mu_array=np.array(static_friction),
        kinetic_mu_array=np.array(kinetic_friction),
    )


# --- Connections ---

def connect_fixed(sim, rod_one, rod_two, index_one=-1, index_two=0, k=1e5, nu=0.0, kt=1e5):
    """
    Connects two rods using a FixedJoint (rigid connection).
    """
    sim.connect(rod_one, rod_two, first_connect_idx=index_one, second_connect_idx=index_two).using(
        ea.FixedJoint,
        k=k,
        nu=nu,
        kt=kt,
        nut=0.0,
    )


def connect_spherical(sim, rod_one, rod_two, index_one=-1, index_two=0, k=1e5, nu=0.0):
    """
    Connects two rods using a FreeJoint (spherical joint).
    """
    sim.connect(rod_one, rod_two, first_connect_idx=index_one, second_connect_idx=index_two).using(
        ea.FreeJoint,
        k=k,
        nu=nu,
    )


def connect_hinge(sim, rod_one, rod_two, index_one=-1, index_two=0, k=1e5, nu=0.0, kt=1e1, normal=(0.0, 1.0, 0.0)):
    """
    Connects two rods using a HingeJoint.
    """
    sim.connect(rod_one, rod_two, first_connect_idx=index_one, second_connect_idx=index_two).using(
        ea.HingeJoint,
        k=k,
        nu=nu,
        kt=kt,
        normal_direction=np.array(normal),
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
    dt = 0.0005

    # 2. Create Objects
    rods = []
    # Rod 0 (soft_biological_tissue)
    rod_0 = make_rod(
        sim,
        n_elem=100,
        length=5.0,
        radius=0.05,
        density=1000,
        youngs_modulus=10000.0,
        poisson_ratio=0.5,
        start=[0.0, 0.0, 0.0],
        direction=[0.0, 0.0, 1.0],
        normal=[0.0, 1.0, 0.0],
        velocity=[0.0, 0.0, 0.0],
        omega=[0.0, 0.0, 0.0],
        nu=0.1,
        dt=dt
    )
    rods.append(rod_0)
    add_muscle_activity(sim, rod_0, amplitude=0.02, wave_length=1.0, frequency=0.2, phase=0.0, ramp=0.1)
    # 3. Setup Diagnostics
    history_list = []
    for rod in rods:
        history_list.append(record_history(sim, rod, step_skip=200))

    # 4. Run Simulation
    final_time = 10.0
    total_steps = int(final_time / dt)
    print(f'Running simulation for {final_time}s ({total_steps} steps)...')
    finalize_and_integrate(sim, final_time=final_time, total_steps=total_steps)

    # 5. Save Results
    print('Saving results to simulation_data.pkl...')
    data = {'rods': history_list, 'metadata': {'fps': 60.0}}
    with open('simulation_data.pkl', 'wb') as f:
        pickle.dump(data, f)
    print('Done.')

if __name__ == '__main__':
    main()