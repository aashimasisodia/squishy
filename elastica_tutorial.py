import numpy as np
from matplotlib import pyplot as plt
from matplotlib.colors import to_rgb


import elastica as ea
from elastica.utils import MaxDimension


class ButterflySimulator(ea.BaseSystemCollection, ea.CallBacks):
    pass


butterfly_sim = ButterflySimulator()
final_time = 40.0

# Options
PLOT_FIGURE = True
SAVE_FIGURE = True
SAVE_RESULTS = True
ADD_UNSHEARABLE_ROD = False

# setting up test params
# FIXME : Doesn't work with elements > 10 (the inverse rotate kernel fails)
n_elem = 4  # Change based on requirements, but be careful
n_elem += n_elem % 2
half_n_elem = n_elem // 2

origin = np.zeros((3, 1))
angle_of_inclination = np.deg2rad(45.0)

# in-plane
horizontal_direction = np.array([0.0, 0.0, 1.0]).reshape(-1, 1)
vertical_direction = np.array([1.0, 0.0, 0.0]).reshape(-1, 1)

# out-of-plane
normal = np.array([0.0, 1.0, 0.0])

total_length = 3.0
base_radius = 0.25
base_area = np.pi * base_radius**2
density = 5000
youngs_modulus = 1e4
poisson_ratio = 0.5
shear_modulus = youngs_modulus / (poisson_ratio + 1.0)

positions = np.empty((MaxDimension.value(), n_elem + 1))
dl = total_length / n_elem

# First half of positions stem from slope angle_of_inclination
first_half = np.arange(half_n_elem + 1.0).reshape(1, -1)
positions[..., : half_n_elem + 1] = origin + dl * first_half * (
    np.cos(angle_of_inclination) * horizontal_direction
    + np.sin(angle_of_inclination) * vertical_direction
)
positions[..., half_n_elem:] = positions[
    ..., half_n_elem : half_n_elem + 1
] + dl * first_half * (
    np.cos(angle_of_inclination) * horizontal_direction
    - np.sin(angle_of_inclination) * vertical_direction
)

butterfly_rod = ea.CosseratRod.straight_rod(
    n_elem,
    start=origin.reshape(3),
    direction=np.array([0.0, 0.0, 1.0]),
    normal=normal,
    base_length=total_length,
    base_radius=base_radius,
    density=density,
    youngs_modulus=youngs_modulus,
    shear_modulus=shear_modulus,
    position=positions,
)

# NOTE: The simulation part is now handled by elastica_render.py
# We only save the rod and necessary parameters here.

if SAVE_RESULTS:
    import pickle

    filename = "butterfly_data.dat"
    with open(filename, "wb") as file:
        data = {
            "rod": butterfly_rod,
            "final_time": final_time,
            "dl": dl, # Save dl to calculate dt in render
        }
        pickle.dump(data, file)
    print(f"Rod and parameters saved to {filename}")