import magpylib as magpy
import numpy as np
from scipy.spatial.transform import Rotation as R

# 1. Define the Tokamak's Parameters
n_coils = 1  # Number of toroidal field coils
major_radius = 10  # Major radius of tokamak (center of torus to center of coils)

# Parameters to define the shape of each coil "plate"
coil_inner_rad = 5
coil_outer_rad = 15
coil_height = 1  # Height of the coil [m]
coil_angle = 360  # Angular width of the coil plate [deg]

# Field strength
polarization_strength = 2.0  # Polarization


# Create a sensor for measuring the field
sensor = magpy.Sensor()

def make_cylinder_seg(height=0.6):
    # Create a ring magnet with magnetic polarization
    inner_r = 1  # Inner radius of the coil's curvature [m]
    outer_r = 2  # Outer radius of the coil's curvature [m]
    start_sec_angle = 0
    end_sec_angle = 360
    return magpy.magnet.CylinderSegment(
        polarization=(0.1, 0.2, 0.3),
        dimension=(inner_r, outer_r, height, start_sec_angle, end_sec_angle),
    )


coils = []
n_coils = 8
for i in range(n_coils):
    # Calculate the angle for placing each coil around the z-axis
    angle_deg = 360 * i / 8
    angle_rad = np.deg2rad(angle_deg)
    position = (major_radius * np.sin(angle_rad), major_radius * np.cos(angle_rad), 0)
    coils.append(position)
print(coils)


torus1 = make_cylinder_seg(height=1)
torus2 = make_cylinder_seg(height=1)
torus3 = make_cylinder_seg(height=2)
torus4 = make_cylinder_seg(height=2)
torus5 = make_cylinder_seg(height=3)
torus6 = make_cylinder_seg(height=3)
torus7 = make_cylinder_seg(height=4)
torus8 = make_cylinder_seg(height=4)

tokascale = 10  # scale size of full ring
torus1.position = (1 * tokascale, 0, 0)
torus1.orientation = R.from_rotvec((0, 0, 0), degrees=True)
torus2.position = (-1 * tokascale, 0, 0)
torus2.orientation = R.from_rotvec((0, 0, 0), degrees=True)
torus3.position = (0, 1 * tokascale, 0)
torus3.orientation = R.from_rotvec((0, 90, 0), degrees=True)
torus4.position = (0, -1 * tokascale, 0)
torus4.orientation = R.from_rotvec((0, 90, 0), degrees=True)
torus5.position = (0.7 * tokascale, -0.7 * tokascale, 0)
torus5.orientation = R.from_rotvec((0, 90, 45), degrees=True)
torus6.position = (-0.7 * tokascale, 0.7 * tokascale, 0)
torus6.orientation = R.from_rotvec((0, 90, 45), degrees=True)
torus7.position = (0.7 * tokascale, 0.7 * tokascale, 0)
torus7.orientation = R.from_rotvec((0, 90, -45), degrees=True)
torus8.position = (-0.7 * tokascale, -0.7 * tokascale, 0)
torus8.orientation = R.from_rotvec((0, 90, -45), degrees=True)
# By default, the position of a Magpylib object is
# (0,0,0) and its orientation is the unit rotation,
# given by a scipy rotation object.
print("Default subject position and orientation")
print(f"Position: {torus1.position}")
print(f"Orientation rotation vector {torus1.orientation.as_rotvec()}")
print()

tokamak_coils = [torus1, torus2, torus3, torus4, torus5, torus6, torus7, torus8]

# Use a Collection to group all the coils
tokamak = magpy.Collection(tokamak_coils)

print("Moved subject position and orientation")
print(f"Position {torus1.position}")
print(f"Orientation rotation vector {torus1.orientation.as_rotvec(degrees=True)}")
print()


print("Default sensor position and orientation")
print(f"Sensor position:{sensor.position}")
print(f"Sensor orientation {sensor.orientation.as_rotvec(degrees=True)}")
print()

# Apply relative motion with the powerful `move`
# and `rotate` methods.
# sensor.move((-0.01, 0, 0))
# sensor.rotate_from_angax(angle=-45, axis="z")
print("Moved sensor position and orientation")
print(f"Sensor position:{sensor.position}")
print(f"Sensor orientation {sensor.orientation.as_rotvec(degrees=True)}")
print()

# Compute the B-field for some positions
points = [(0, 0, -0.01), (0, 0, 0), (0, 0, 0.01)]
B = magpy.getB(torus1, points)
print(f"B-field : {B.round(2)}")
print(f"computed for points: {points}")
print()

# compute the H-field at the sensor
H = magpy.getH(torus1, sensor)
print(f"H-field: {H.round()}")
print(
    f"computed with sensor at {sensor.position} {sensor.orientation.as_rotvec(degrees=True)}"
)
print()

# visualize
magpy.show(tokamak, sensor, backend="plotly")
