import tokamak_sim_setup
import numpy as np
import magpylib as magpy

tokamak = tokamak_sim_setup.create_tokamak()
sensor = tokamak_sim_setup.create_sensor()

# calculate and display the magnetic field
B_field = tokamak.getB(sensor)
print(f"Magnetic field at sensor position {sensor.position} m: B = {B_field} T")
print(f"Field magnitude: {np.linalg.norm(B_field):.2f} T")

# move sensor and re-measure
print("\n--- Moving sensor to a new position ---")
sensor.position = (sensor.position[0] + 0.1, 0.1, 0)  # Move it slightly off-center
B_field_new = tokamak.getB(sensor)
print(f"Magnetic field at new position {sensor.position} m: B = {B_field_new} T")
print(f"Field magnitude: {np.linalg.norm(B_field_new):.2f} T")

sensor.position = (-2, -2, -2)
# Do it in a loop
results = {}
grid_density = 10  # grid_density**3 = x * y * z points


fig = magpy.show(tokamak, sensor, backend="plotly")

for x in np.linspace(-2, 2, grid_density):
    print(f"x={x}")
    sensor.position = (x / grid_density, sensor.position[1], sensor.position[2])
    for y in np.linspace(-2, 2, grid_density):
        sensor.position = (sensor.position[0], y / grid_density, sensor.position[2])
        for z in np.linspace(-2, 2, grid_density):
            # move sensor and re-measure
            # print("\n--- Moving sensor to a new position ---")
            sensor.position = (
                sensor.position[0],
                sensor.position[1],
                z / grid_density,
            )  # Move it slightly off-center
            sensor.position = (
                sensor.position[0],
                sensor.position[1],
                sensor.position[2] + z / grid_density,
            )  # Move it slightly off-center
            B_field_new = tokamak.getB(sensor)
            results[tuple([x, y, z])] = B_field_new
            # print(f"Magnetic field at new position {sensor.position} m: B = {B_field_new} T")
            # print(f"Field magnitude: {np.linalg.norm(B_field_new):.2f} T")
            print(sensor.position)
# visualize the simulation ⚛️
# display the collection of magnets and the sensor's location
fig = magpy.show(tokamak, sensor, backend="plotly")

results = []
for x in results.values():
    results.append(np.sqrt(x.dot(x)))

fig = magpy.show(tokamak, sensor, backend="plotly")

# TODO: how to display sensor movement?
