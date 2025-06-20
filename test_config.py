import yaml
import numpy as np


# Load configuration
print("Loading configuration from config.yaml")
try:
    with open("config.yml", "r") as file:
        config = yaml.safe_load(file)
except FileNotFoundError:
    print("Error: config.yml not found. Please create the file.")
    exit()

# Accessing variables
print("Accessing basic parameters")
# Use dictionary key access to navigate the nested structure
sensor_count = config["system_parameters"]["sensor_count"]
max_velocity_y = config["motion_profile"]["max_velocity_mm_per_s"]["y"]
output_file = config["files"]["output_muxed_result"]

print(f"Sensor count: {sensor_count}")
print(f"Max y-axis velocity: {max_velocity_y} mm/s")
print(f"Output file: {output_file}")


# Reconstructing variables
print("Reconstructing complex and calculated variables")

# Convert lists from yaml back into numpy arrays
print("Reconstructing numpy arrays...")
scan_vectors = config["simulation_objects"]["scan_vectors"]
pos_y_sweep = np.array(scan_vectors["pos_y_sweep"])
# Now you can perform vector operations that yaml couldn't handle
neg_y_sweep = -1 * pos_y_sweep

print(f"pos_y_sweep (as numpy.ndarray): {pos_y_sweep}")
print(f"Derived neg_y_sweep: {neg_y_sweep}")

# Perform calculations that were removed from the static yaml
print("Re-calculating derived values...")
sampling_rate = config["sampling"]["rate_hz"]
y_scan_time = config["scan_setup"]["durations_s"]["y_scan"]
samples_per_y_scan = int(sampling_rate * y_scan_time)

print(f"Sampling Rate: {sampling_rate} Hz")
print(f"Y Scan Time: {y_scan_time} s")
print(f"Calculated Samples per Y Scan: {samples_per_y_scan}")

# Using the variables in simulation
print("All variables are now ready for the simulation")
