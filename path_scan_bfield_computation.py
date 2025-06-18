import numpy as np
import time
import magpylib as magpy


def simulate_constant_velocity_path():
    """
    Simulates the data acquisition path assuming constant velocity for each sweep.
    This generates a PATH, not a grid.
    """
    # System Parameters
    SAMPLE_RATE = 10000  # samples/sec

    # Scan Dimensions (mm) and Repetitions
    MAX_X, MAX_Y, MAX_Z = 300.0, 300.0, 300.0
    STEP_Z, STEP_X = 30.0, 10.0
    N_X_REPEATS = 30
    N_Z_STEPS_PER_PLANE = 10

    # Scan Durations (seconds)
    TIME_Y_SCAN = 17.0
    TIME_Z_STEP = 11.0
    TIME_X_STEP = 7.0

    # Calculate samples per movement
    SAMPLES_PER_Y_SCAN = int(SAMPLE_RATE * TIME_Y_SCAN)
    SAMPLES_PER_Z_STEP = int(SAMPLE_RATE * TIME_Z_STEP)
    SAMPLES_PER_X_STEP = int(SAMPLE_RATE * TIME_X_STEP)

    # Simulation
    path_segments = []
    current_x, current_y, current_z = 0.0, 0.0, 0.0

    print("Simulating constant velocity scan path...")
    start_time = time.time()

    for i_x in range(N_X_REPEATS):
        # Scan a full plane (10 Y-sweeps and 10 Z-steps)
        for i_z_step in range(N_Z_STEPS_PER_PLANE):
            # Y-Axis Scan (back and forth)
            start_y, end_y = current_y, MAX_Y if i_z_step % 2 == 0 else 0.0

            y_coords = np.linspace(start_y, end_y, SAMPLES_PER_Y_SCAN)
            x_coords = np.full(SAMPLES_PER_Y_SCAN, current_x)
            z_coords = np.full(SAMPLES_PER_Y_SCAN, current_z)
            path_segments.append(np.column_stack((x_coords, y_coords, z_coords)))
            current_y = end_y

            # Z-Axis Step
            start_z, end_z = current_z, current_z + STEP_Z

            z_coords = np.linspace(start_z, end_z, SAMPLES_PER_Z_STEP)
            x_coords = np.full(SAMPLES_PER_Z_STEP, current_x)
            y_coords = np.full(SAMPLES_PER_Z_STEP, current_y)
            path_segments.append(np.column_stack((x_coords, y_coords, z_coords)))
            current_z = end_z

        current_z = 0.0  # Reset Z for the next plane

        # X-Axis Step (if it's not the last plane)
        if i_x < N_X_REPEATS - 1:
            start_x, end_x = current_x, current_x + STEP_X

            x_coords = np.linspace(start_x, end_x, SAMPLES_PER_X_STEP)
            y_coords = np.full(SAMPLES_PER_X_STEP, current_y)
            z_coords = np.full(SAMPLES_PER_X_STEP, current_z)
            path_segments.append(np.column_stack((x_coords, y_coords, z_coords)))
            current_x = end_x

        print(f"  Completed plane {i_x + 1}/{N_X_REPEATS}...")

    print("\nConcatenating all path segments...")
    all_sample_points = np.vstack(path_segments)
    end_time = time.time()

    print("-" * 30)
    print(f"Simulation finished in {end_time - start_time:.2f} seconds.")
    print(f"Final array shape: {all_sample_points.shape}")
    print(f"Memory usage: ~{all_sample_points.nbytes / 1e9:.2f} GB")

    return all_sample_points


if __name__ == "__main__":
    # 1. Generate the entire path of sample coordinates
    path_generation_start = time.time()
    sampled_points = simulate_constant_velocity_path()
    path_generation_end = time.time()
    print(
        f"Path generation finished in {path_generation_end - path_generation_start:.2f} seconds."
    )
    print(f"Generated {sampled_points.shape[0]:,} coordinate points.")
    print("-" * 40)

    # 2. Perform the B-field calculation on the generated path
    print("Starting B-field calculation...")
    b_field_start = time.time()

    # Define the magnetic source
    source_sphere = magpy.magnet.Sphere(polarization=(500, 0, 500), diameter=2.0)

    # Calculate the B-field for every single point in our path
    # The 'sampled_points' array is the "grid" that getB needs.
    B_field_data = source_sphere.getB(sampled_points)

    b_field_end = time.time()
    print(f"B-field calculation finished in {b_field_end - b_field_start:.2f} seconds.")
    print("-" * 40)

    # 3. View the results
    print(f"Shape of the coordinate array: {sampled_points.shape}")
    print(f"Shape of the resulting B-field array: {B_field_data.shape}")
    print(
        "\nThis means for each of our N coordinates, we have a corresponding (Bx, By, Bz) vector."
    )

    print("\nExample Data:")
    print("Coordinate Point [0]:", sampled_points[0])
    print("B-field Vector   [0]:", B_field_data[0])

    print(
        "\nCoordinate Point [170000]:", sampled_points[170000]
    )  # End of first Y-sweep
    print("B-field Vector   [170000]:", B_field_data[170000])
    B_field_data.tofile("B-field.npy")
    sampled_points.tofile("simulated_path.npy")
