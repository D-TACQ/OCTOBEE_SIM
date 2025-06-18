# Path simulator
"""
# Definition of the linear scan to be performed

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

# All a in mm/s**2
x_a = 1
y_a = 10
z_a = 3

# All v in mm/s
x_maxv = 2
y_maxv = 20
z_maxv = 3

# time step is related to sample rate
# sample rate in samples/s
min_sample_rate = 10000
max_sample_rate = 200000

# sample freq in Hz
min_sample_freq = min_sample_rate / 1
max_sample_freq = max_sample_rate / 1

# one tick per mm
encoder_resolution = 1

sample_clock_start = 0

pos_y_sweep = np.array([0, 300, 0])
pos_z_shift = np.array([0, 0, 15])
neg_y_sweep = -1 * pos_y_sweep
neg_z_shift = -1 * pos_z_shift
x_shift = np.array([10, 0, 0])


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


origin = [0, 0, 0]

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
    position = np.array(origin)
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

    # Plot the path with a line and markers for each point
    ax.plot(x_coords, y_coords, z_coords, marker=".", markersize=2, linestyle="-")

    # Highlight the start and end points
    ax.scatter(
        x_coords[0], y_coords[0], z_coords[0], color="lime", s=100, label="Start"
    )
    ax.scatter(
        x_coords[-1], y_coords[-1], z_coords[-1], color="red", s=100, label="End"
    )

    # Set labels and title
    # ax.set_xlabel("X axis (mm)")
    # ax.set_ylabel("Y axis (mm)")
    # ax.set_z_label("Z axis (mm)")
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
