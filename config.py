import yaml

try:
    with open("config.yml", "r") as file:
        config = yaml.safe_load(file)
except FileNotFoundError:
    print("Error: config.yml not found. Please create the file.")
    exit()

FILES = config["files"]
SYSTEM_PARAMETERS = config["system_parameters"]
MOTION_PROFILE = config["motion_profile"]
SIMULATION_OBJECTS = config["simulation_objects"]
SAMPLING = config["sampling"]
SCAN_SETUP = config["scan_setup"]
