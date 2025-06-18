import numpy as np
import magpylib as magpy
from scipy.spatial.transform import Rotation as R


def create_tokamak():
    # Define the tokamak parameters
    n_coils = 18  # Number of toroidal field coils
    major_radius = (
        2.0  # Major radius of the tokamak (center of torus to center of coils) [m]
    )
    coil_radius_inner = 0.4  # inner radius of the coils [m]
    coil_radius_outer = 0.6  # outer radius of the coils [m]
    coil_height = 0.2  # height of the coils [m]
    magnetization_strength = 1.25e6  # magnetization in A/m

    # create collection of toroidal field coils
    tokamak_coils = []
    for i in range(n_coils):
        # calculate angle for each coil
        angle_deg = 360 * i / n_coils
        angle_rad = np.deg2rad(angle_deg)

        # position each coil in a circle in the x-y plane
        position = (
            major_radius * np.cos(angle_rad),
            major_radius * np.sin(angle_rad),
            0,
        )

        # model each TF coil as a full ring (CylinderSegment with 360 degrees)
        # The segment's natural axis is z
        # rotate it to align with toroidal field direction
        orientation = (
            R.from_euler("z", angle_deg, degrees=True)
            * R.from_euler("y", 90, degrees=True)
            * R.from_euler("x", 90, degrees=True)
        )

        # for simple toroidal field, make magnetization along coil's axis.
        # define it along the object's local z-axis.
        coil = magpy.magnet.CylinderSegment(
            position=position,
            orientation=orientation,
            dimension=(
                coil_radius_inner,
                coil_radius_outer,
                coil_height,
                0,
                360,
            ),
            magnetization=(0, 0, magnetization_strength),
        )
        tokamak_coils.append(coil)

    # use a collection to group all the coils
    tokamak = magpy.Collection(tokamak_coils)

    return tokamak


def create_sensor(x=2, y=0, z=0):
    # create a Sensor to Measure the B-field
    # place the sensor inside the 'vacuum vessel' area
    sensor_pos = (x, 0, 0)
    sensor = magpy.Sensor(position=sensor_pos)
    return sensor
