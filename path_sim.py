# Path simulator
"""
Definition of the linear scan to be performed

X-sweeps: 2 mm/s, 1 mm/s2
Y-sweeps: 20 mm/s, 10 mm/s2
Z-sweeps: 3 mm/s, 3 mm/s2

Sweep path:

300 mm along YL  (2s accelerate + 2s decelerate + 13s constant V)
30 mm along ZL (1s accelerate + 1s decelerate + 9s constant velocity)
300 mm along -YL  (17s)
30 mm along ZL (11s)
repeat 10 times (10 x 56 s = 560 s = 9.33 min)

10 mm along XL   (2s accelerate + 2s decelerate + 3s constant V)

repeat 30 times (30 x 560 s = 16800 s = 280 min = 4.67 hours)
"""
import numpy as np
import matplotlib.pyplot as plt

import magpylib as magpy

from config import FILES, MOTION_PROFILE, SYSTEM_PARAMETERS, SAMPLING, SIMULATION_OBJECTS

# All a in m/s**2
x_a = MOTION_PROFILE['acceleration_m_per_s2']['x']
y_a = MOTION_PROFILE['acceleration_m_per_s2']['y']
z_a = MOTION_PROFILE['acceleration_m_per_s2']['z']

# All v in m/s
x_maxv = MOTION_PROFILE['max_velocity_m_per_s2']['x']
y_maxv = MOTION_PROFILE['max_velocity_m_per_s2']['y']
z_maxv = MOTION_PROFILE['max_velocity_m_per_s2']['z']

# time step is related to sample rate
# sample rate in samples/s
min_sample_rate = SAMPLING["min_rate_hz"]
max_sample_rate = SAMPLING["max_rate_hz"]

# sample freq in Hz
min_sample_freq = min_sample_rate / 1
max_sample_freq = max_sample_rate / 1

sample_clock_start = SAMPLING["clock_start"]
encoder_resolution = SYSTEM_PARAMETERS["encoder_resolution"]


pos_y_sweep = np.array([0, 300, 0])
pos_z_shift = np.array([0, 0, 15])
neg_y_sweep = -1 * pos_y_sweep
neg_z_shift = -1 * pos_z_shift
x_shift = np.array([10, 0, 0])

# dummy magnet
# add a sphere that defines the system under test
D = SIMULATION_OBJECTS["system_under_test"]["diameter"]
Xs = SIMULATION_OBJECTS["system_under_test"]["position_m"]["x"]
Ys = SIMULATION_OBJECTS["system_under_test"]["position_m"]["y"]
Zs = SIMULATION_OBJECTS["system_under_test"]["position_m"]["z"]
obj_sphere = magpy.magnet.Sphere(position=(Xs, Ys, Zs), diameter=D)


def walk_sequence(sequence_of_steps):
    """
    Recursively walks through the nested list of sequences and yields
    each individual position vector one by one.
    """
    for step in sequence_of_steps:
        # Check if step is a list/tuple (and therefore a subsequence)
        if isinstance(step, (list, tuple)):
            yield from walk_sequence(step)
        else:
            # Otherwise it is assumed to be a vector and is yielded directly
            yield step


origin = SYSTEM_PARAMETERS["origin_m"]

pos_yz_sequence = [pos_y_sweep, pos_z_shift, neg_y_sweep, pos_z_shift]
neg_yz_sequence = [pos_y_sweep, neg_z_shift, neg_y_sweep, neg_z_shift]
# neg_yz_sequence = [pos_y_sweep, neg_z_shift, neg_y_sweep, neg_z_shift]
# yz_sequence repeated 10 times
full_yz_sequence = [
    pos_yz_sequence,
    pos_yz_sequence,
    pos_yz_sequence,
    pos_yz_sequence,
    pos_yz_sequence,
    pos_yz_sequence,
    pos_yz_sequence,
    pos_yz_sequence,
    pos_yz_sequence,
    pos_yz_sequence,
]

full_neg_yz_sequence = [
    neg_yz_sequence,
    neg_yz_sequence,
    neg_yz_sequence,
    neg_yz_sequence,
    neg_yz_sequence,
    neg_yz_sequence,
    neg_yz_sequence,
    neg_yz_sequence,
    neg_yz_sequence,
    neg_yz_sequence,
]

# x_shift
full_sequence = [
    full_yz_sequence,
    x_shift,
    full_neg_yz_sequence,
    x_shift,
    full_yz_sequence,
    x_shift,
    full_neg_yz_sequence,
    x_shift,
    full_yz_sequence,
    x_shift,
    full_neg_yz_sequence,
    x_shift,
    full_yz_sequence,
    x_shift,
    full_neg_yz_sequence,
    x_shift,
    full_yz_sequence,
    x_shift,
    full_neg_yz_sequence,
    x_shift,
    full_yz_sequence,
    x_shift,
    full_neg_yz_sequence,
    x_shift,
    full_yz_sequence,
    x_shift,
    full_neg_yz_sequence,
    x_shift,
    full_yz_sequence,
    x_shift,
    full_neg_yz_sequence,
    x_shift,
    full_yz_sequence,
    x_shift,
    full_neg_yz_sequence,
    x_shift,
    full_yz_sequence,
    x_shift,
    full_neg_yz_sequence,
    x_shift,
    full_yz_sequence,
    x_shift,
    full_neg_yz_sequence,
    x_shift,
    full_yz_sequence,
    x_shift,
    full_neg_yz_sequence,
    x_shift,
    full_yz_sequence,
    x_shift,
    full_neg_yz_sequence,
    x_shift,
    full_yz_sequence,
    x_shift,
    full_neg_yz_sequence,
    x_shift,
    full_yz_sequence,
    x_shift,
    full_neg_yz_sequence,
    x_shift,
]


def run():
    position = np.array(origin, dtype=np.float64)
    position_history = [origin.copy()]
    for vector in walk_sequence(full_sequence):
        position += vector
        position_history.append(position.copy())
        # debug print
        # print(position)
        # build the dataset here with the Bx,By,Bz values
        # SPAD
        # counters
    return position_history


def initial_position(position_history):
    return position_history[0]


def final_position(position_history):
    return position_history[-1]


def plot_path(path_history):
    # Convert the list of positions into a single NumPy array
    print(path_history)
    path_array = np.array(path_history)

    # Extract the x, y, and z coordinates
    x_coords = path_array[:, 0]
    print(x_coords)
    y_coords = path_array[:, 1]
    print(y_coords)
    z_coords = path_array[:, 2]
    print(z_coords)

    # Create the 3D plot
    fig = plt.figure(figsize=(12, 9))
    ax = fig.add_subplot(111, projection="3d")

    magpy.show(obj_sphere, canvas=ax, style={"color": "grey", "opacity": 0.4})
    # Plot the path with a line and markers for each point
    ax.plot(x_coords, y_coords, z_coords, marker=".", markersize=2, linestyle="-")
    # Highlight the start and end points
    ax.scatter(
        x_coords[0], y_coords[0], z_coords[0], color="lime", s=100, label="Start"
    )
    ax.scatter(
        x_coords[-1], y_coords[-1], z_coords[-1], color="red", s=100, label="End"
    )

    # Calculate the extents of your path data
    x_min, x_max = np.min(x_coords), np.max(x_coords)
    y_min, y_max = np.min(y_coords), np.max(y_coords)
    z_min, z_max = np.min(z_coords), np.max(z_coords)

    # Determine the center of the path
    x_center, y_center, z_center = (
        np.mean([x_min, x_max]),
        np.mean([y_min, y_max]),
        np.mean([z_min, z_max]),
    )

    # Determine the largest range needed to encompass the whole path
    max_range = np.array([x_max - x_min, y_max - y_min, z_max - z_min]).max()

    # Set the limits to be a cube centered on the path
    ax.set_xlim(x_center - max_range / 2, x_center + max_range / 2)
    ax.set_ylim(y_center - max_range / 2, y_center + max_range / 2)
    ax.set_zlim(z_center - max_range / 2, z_center + max_range / 2)

    # Set labels and title
    # ax.set_xlabel("X axis (m)")
    # ax.set_ylabel("Y axis (m)")
    # ax.set_z_label("Z axis (m)")
    ax.set_title("3D Linear Scan Path Simulation")
    ax.legend()

    # Improve layout
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    position_history = run()
    print(initial_position(position_history))
    print(final_position(position_history))
    plot_path(position_history)
    print(f"starting at origin {origin}")
    print(f"ending at {final_position(position_history)}")
