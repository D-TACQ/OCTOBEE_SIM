import magpylib as magpy

# Create a toroid magnet with magnetic polarization
# of 1 T pointing in x-direction and sides of
# 1, 2, and 3 cm respectively (note the use of SI units)
inner_r = 0.01
outer_r = 0.02
height = 0.01
start_section_angle = 0
end_section_angle = 360

ring = magpy.magnet.CylinderSegment(
    polarization=(0.1, 0.2, 0.3),
    dimension=(inner_r, outer_r, height, start_section_angle, end_section_angle),
)

# Create a Sensor for measuring the field
sensor = magpy.Sensor()

# By default, the position of a Magpylib object is
# (0,0,0) and its orientation is the unit rotation,
# given by a scipy rotation object.
print("Default subject position and orientation")
print(f"Position: {ring.position}")
print(f"Orientation rotation vector {ring.orientation.as_rotvec()}")
print()

# Manipulate object position and orientation through
# the respective attributes (move 10 mm and rotate 45 deg):

from scipy.spatial.transform import Rotation as R

ring.position = (0.01, 0, 0)
ring.orientation = R.from_rotvec((0, 0, 45), degrees=True)
print("Moved subject position and orientation")
print(f"Position {ring.position}")
print(f"Orientation rotation vector {ring.orientation.as_rotvec(degrees=True)}")
print()


print("Default sensor position and orientation")
print(f"Sensor position:{sensor.position}")
print(f"Sensor orientation {sensor.orientation.as_rotvec(degrees=True)}")
print()

# Apply relative motion with the powerful `move`
# and `rotate` methods.
sensor.move((-0.01, 0, 0))
sensor.rotate_from_angax(angle=-45, axis="z")
print("Moved sensor position and orientation")
print(f"Sensor position:{sensor.position}")
print(f"Sensor orientation {sensor.orientation.as_rotvec(degrees=True)}")
print()

# Use the `show` function to view your system
# through Matplotlib, Plotly or Pyvista backends.
magpy.show(ring, sensor, backend="plotly")

# Compute the B-field for some positions.
points = [(0, 0, -0.01), (0, 0, 0), (0, 0, 0.01)]
B = magpy.getB(ring, points)
print(f"B-field : {B.round(2)}")
print(f"computed for points: {points}")
print()

# Compute the H-field at the sensor.
H = magpy.getH(ring, sensor)
print(f"H-field: {H.round()}")
print(f"computed with sensor at {sensor.position} {sensor.orientation.as_rotvec(degrees=True)}")
print()
