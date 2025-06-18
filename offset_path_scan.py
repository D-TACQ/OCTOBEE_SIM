"""
Offset an existing path by a constant along one, two or three axes
"""

import numpy as np
import time
import magpylib as magpy


if __name__ == "__main__":
    # Load path of sample coordinates
    path_generation_start = time.time()
    sampled_points = np.load("data/simulated_path.npy")
    print(f"Shape of loaded array {sampled_points.shape}")
    path_generation_end = time.time()
    print(
        f"Path loading finished in {path_generation_end - path_generation_start:.2f} seconds."
    )
    print(f"Generated {sampled_points.shape[0]:,} coordinate points.")
    print("-" * 40)

    # Add z-axis offset
    print(f"sampled_points {sampled_points[0]}")
    print(f"sampled_points {sampled_points[245785]}")
    print(f"sampled_points {sampled_points[-1]}")

    z_offset_values = (0, 5, 10, 15, 20, 25, 30, 35)
    for z_offset_value in z_offset_values:

        sampled_points = np.load("data/simulated_path.npy")
        z_offset = np.array([0, 0, z_offset_value])
        sampled_points = sampled_points + z_offset

        print(f"sampled_points {sampled_points[0]}")
        print(f"sampled_points {sampled_points[245785]}")
        print(f"sampled_points {sampled_points[-1]}")
        # Perform the B-field calculation on the generated path
        print("Starting B-field calculation...")
        b_field_start = time.time()

        # Define the magnetic source
        source_sphere = magpy.magnet.Sphere(polarization=(500, 0, 500), diameter=2.0)

        # Calculate the B-field for every single point in our path
        # The 'sampled_points' array is the "grid" that getB needs.
        B_field_data = source_sphere.getB(sampled_points)

        b_field_end = time.time()
        print(
            f"B-field calculation finished in {b_field_end - b_field_start:.2f} seconds."
        )
        print("-" * 40)

        # View the results
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
        np.save(f"B-field_zoff_{z_offset_value}.npy", B_field_data)
        # np.save("simulated_path.npy", sampled_points)
