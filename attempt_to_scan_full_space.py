"""
Runs the full simulation
"""

import sys
import numpy as np

# define magnet environment
import sphere_magnet

# define scan path
import path_sim

# create large data array

# define and run scan

# run scan to collect data
# populating large data array

# cast large data array to structured array
import data_writer


def create_linspace(left, right, spacing):
    return np.linspace(left, right, spacing)


def volume_of_space(tsx, tsy, tsz):
    return (tsx[-1] - tsx[0]) * (tsy[-1] - tsy[0]) * (tsz[-1] - tsz[0])


def points_in_space(tsx, tsy, tsz):
    return (
        (tsx[-1] - tsx[0]) * len(tsx)
        + (tsy[-1] - tsy[0]) * len(tsy)
        + (tsz[-1] - tsz[0]) * len(tsz)
    )


if __name__ == "__main__":
    print(f"running {sys.argv[0]}")
    print("Defining magnet parameters...")
    sphere = sphere_magnet.create()
    MINIMUM_COORD_X = 0
    MAXIMUM_COORD_X = 300
    MINIMUM_COORD_Y = 0
    MAXIMUM_COORD_Y = 300
    MINIMUM_COORD_Z = 0
    MAXIMUM_COORD_Z = 300
    VELOCITY_X = 2
    VELOCITY_Y = 20
    VELOCITY_Z = 3
    TIME_X = 7
    TIME_Y = 17
    TIME_Z = 11
    SPACING = 40
    SAMPLE_RATE = 10000
    SCAN_RATE_X = VELOCITY_X
    SCAN_RATE_Y = VELOCITY_Y
    SCAN_RATE_Z = VELOCITY_Z
    SPACING_X = SAMPLE_RATE * TIME_X
    SPACING_Y = SAMPLE_RATE * TIME_Y
    SPACING_Z = SAMPLE_RATE * TIME_Z
    ts = np.linspace(-5, 5, 40)
    # get values for tsx, tsy, tsz from path_sim
    print("creating x linspace")
    tsx = create_linspace(MINIMUM_COORD_X, MAXIMUM_COORD_X, SPACING_X)
    print("creating y linspace")
    tsy = create_linspace(MINIMUM_COORD_Y, MAXIMUM_COORD_Y, SPACING_Y)
    print("creating z linspace")
    tsz = create_linspace(MINIMUM_COORD_Z, MAXIMUM_COORD_Z, SPACING_Z)
    print(f"linspaces x: {tsx.shape} y: {tsy.shape} z: {tsz.shape} \n")
    volume_to_scan = volume_of_space(tsx, tsy, tsz)
    n_points_to_scan = points_in_space(tsx, tsy, tsz)
    print(f"Volume to scan is {volume_to_scan} units^3")
    print(f"Points to scan is {n_points_to_scan}")
    inp = input("Press any key to create grid from these")
    grid = np.array([[[(x, y, z) for x in tsx] for y in tsy] for z in tsz])

    inp = input("Press any key to continue...")
    B = sphere_magnet.compute_b_field(sphere, grid)

    # once you have the 3D grid of the B-field -- reorder it into scan order
    # then convert to muxed data and call it a day

    print("Defining linear scan")
    position_history = path_sim.run()

    # For a specific position history... sample teh B-field for the magnet
    # at each of those points

    # TODO: some kind of interpolation required?
    # Can we just assume it's linear between two points?
    # Are we not interpolating in 3D though?

    print("Running scan")
    # Move sensor and collate data here

    print("Exporting data")
    # save data to file
    a = np.array([1, 2, 3])
    a.tofile("hello.npy")
    data_writer.to_file(a, "hello_data_writer.npy")
