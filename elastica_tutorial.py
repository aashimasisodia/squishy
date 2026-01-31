__doc__ = """Snake friction case from X. Zhang et. al. Nat. Comm. 2021"""

import os
import numpy as np
import elastica as ea
from numpy.typing import NDArray
from elastica.typing import RodType

# from continuum_snake_postprocessing import (
#     plot_snake_velocity,
#     plot_video,
#     compute_projected_velocity,
#     plot_curvature,
# )


class SnakeSimulator(
    ea.BaseSystemCollection,
    ea.Constraints,
    ea.Forcing,
    ea.Damping,
    ea.CallBacks,
    ea.Contact,
):
    pass



def create_snake_system(
    b_coeff: NDArray[np.float64]
) -> dict:
    # Simulation parameters
    period = 2
    final_time = (11.0 + 0.01) * period

    # setting up test params
    n_elem = 50
    start = np.zeros((3,))
    direction = np.array([0.0, 0.0, 1.0])
    normal = np.array([0.0, 1.0, 0.0])
    base_length = 0.35
    base_radius = base_length * 0.011
    density = 1000
    E = 1e6
    poisson_ratio = 0.5
    shear_modulus = E / (poisson_ratio + 1.0)

    shearable_rod = ea.CosseratRod.straight_rod(
        n_elem,
        start,
        direction,
        normal,
        base_length,
        base_radius,
        density,
        youngs_modulus=E,
        shear_modulus=shear_modulus,
    )

    # Initialize lists for system reconstruction
    features = []
    auxiliary_systems = []

    # Add gravitational forces
    gravitational_acc = -9.80665
    features.append({
        "type": "forcing",
        "target": shearable_rod,
        "class": ea.GravityForces,
        "kwargs": {"acc_gravity": np.array([0.0, gravitational_acc, 0.0])}
    })

    # Add muscle torques
    wave_length = b_coeff[-1]
    features.append({
        "type": "forcing",
        "target": shearable_rod,
        "class": ea.MuscleTorques,
        "kwargs": {
            "base_length": base_length,
            "b_coeff": b_coeff[:-1],
            "period": period,
            "wave_number": 2.0 * np.pi / (wave_length),
            "phase_shift": 0.0,
            "rest_lengths": shearable_rod.rest_lengths,
            "ramp_up_time": period,
            "direction": normal,
            "with_spline": True,
        }
    })

    # Add friction forces
    ground_plane = ea.Plane(
        plane_origin=np.array([0.0, -base_radius, 0.0]), plane_normal=normal
    )
    auxiliary_systems.append(ground_plane)
    
    slip_velocity_tol = 1e-8
    froude = 0.1
    mu = base_length / (period * period * np.abs(gravitational_acc) * froude)
    kinetic_mu_array = np.array(
        [mu, 1.5 * mu, 2.0 * mu]
    )  # [forward, backward, sideways]
    static_mu_array = np.zeros(kinetic_mu_array.shape)
    
    features.append({
        "type": "contact",
        "system_one": shearable_rod,
        "system_two": ground_plane,
        "class": ea.RodPlaneContactWithAnisotropicFriction,
        "kwargs": {
            "k": 1.0,
            "nu": 1e-6,
            "slip_velocity_tol": slip_velocity_tol,
            "static_mu_array": static_mu_array,
            "kinetic_mu_array": kinetic_mu_array,
        }
    })

    # add damping
    damping_constant = 2e-3
    time_step = 1e-4
    features.append({
        "type": "damping",
        "target": shearable_rod,
        "class": ea.AnalyticalLinearDamper,
        "kwargs": {
            "damping_constant": damping_constant,
            "time_step": time_step,
        }
    })
    
    return {
        "rod": shearable_rod,
        "auxiliary_systems": auxiliary_systems,
        "features": features,
        "final_time": final_time,
        "time_step": time_step
    }

if __name__ == "__main__":

    # Options
    PLOT_FIGURE = True
    SAVE_FIGURE = True
    SAVE_VIDEO = True
    SAVE_RESULTS = True
    CMA_OPTION = False

    if CMA_OPTION:
       pass
       # Optimization code removed for brevity/simplicity as we just want to render one instance
    else:
        # Add muscle forces on the rod
        if os.path.exists("optimized_coefficients.txt"):
            t_coeff_optimized = np.genfromtxt(
                "optimized_coefficients.txt", delimiter=","
            )
        else:
            wave_length = 1.0
            t_coeff_optimized = np.array(
                [3.4e-3, 3.3e-3, 4.2e-3, 2.6e-3, 3.6e-3, 3.5e-3]
            )
            t_coeff_optimized = np.hstack((t_coeff_optimized, wave_length))

        # Create the system configuration
        system_config = create_snake_system(t_coeff_optimized)

        # Save to pickle for elastica_render.py
        if SAVE_RESULTS:
            import pickle

            filename = "butterfly_data.dat"
            with open(filename, "wb") as file:
                # We save the whole config dict
                pickle.dump(system_config, file)
            print(f"System configuration saved to {filename}")