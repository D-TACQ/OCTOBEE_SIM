# Introduction
This is a magnetic simulation that simulates a linear scan in 3 dimensions of 3D Hall Effect sensors through a magnetic field.

The various files generate the scan path, do a simulation to get B-field reading of all points on that path.
This uses a configurable sample rate and time per axis of scan, with the default configuration 10kSPS.
A full path scan with one sensor and default time per axis generates ~80M points to be solved by the simulation.
The default number of sensors simulated is 8, each offset by 5mm from the adjacent sensor along a single axis.

# Setup
To install the dependencies a `requirements.txt` file has been provided.
This is easiest install and run from a virtual environment.
Create a virtual environment and install the requirements with pip:

```
python -m venv env_octo-bee
source env_octo-bee/bin/activate
pip install -r requirements.txt
```

To exit the virtual environment simpy type `deactivate` in the shell prompt.

# Run full simulation
The definition of all simulation parameters is done inside `config.yml`.
An example has been provided to get started.
You can copy this `config.yml` to create your own simulations.
After copying you must edit `config.py` to point to your edited version.

To run a full simulation, from definition of simulation to output to disk of muxed data, run these files in order:

`python path_scan_bfield_computation.py`  
After this first run with a single sensor you can plot and check out your generated path with the `path_sim.py`

`python offset_path_scan.py`  
This will generate `.npy` files for 7 more sensors, with results saved to disk in numpy array format. 
The example configuration will use ~15GB of disk space.

`python write_muxed_data.py`  
Finally to generate a data file in ACQ400 format.
By default this will only munge the first ~200k points into the binary format to keep the file size small.
The format is defined in the module docstring on `write_muxed_data.py`.

## Output
An example of the final binary output should look something like:

```
~/PROJECTS/octo-bee$ hexdump -e '32/2 "%04x," 8/4 "%08x," "\n"' <  data/binary_data.bin | head

3cc4,21a4,14f4,3cc4,3d62,22fd,149b,3d62,3ea9,2490,13af,3ea9,407b,2671,12c9,407b,42c7,27a4,11e4,42c7,4581,2890,1106,4581,4897,29ad,1027,4897,4c03,2b0a,0f09,4c03,00000000,00000000,00000000,00000000,00000000,00002222,00003333,00005555,
3cc4,21a4,14f4,3cc4,3d63,22fd,149b,3d63,3ea9,2490,13af,3ea9,407b,2671,12c9,407b,42c8,27a4,11e4,42c8,4582,2890,1106,4582,4898,29ad,1027,4898,4c04,2b0a,0f09,4c04,00000000,00000011,00000000,00000001,00000064,00002222,00003333,00005555,
3cc5,21a4,14f4,3cc5,3d63,22fe,149b,3d63,3eaa,2490,13af,3eaa,407c,2671,12c9,407c,42c8,27a4,11e4,42c8,4583,2890,1107,4583,4899,29ad,1027,4899,4c05,2b0a,0f09,4c05,00000000,00000023,00000000,00000002,000000c8,00002222,00003333,00005555,
3cc5,21a4,14f4,3cc5,3d64,22fe,149b,3d64,3eaa,2490,13af,3eaa,407c,2672,12c9,407c,42c9,27a4,11e5,42c9,4583,2890,1107,4583,4899,29ad,1027,4899,4c05,2b0a,0f09,4c05,00000000,00000034,00000000,00000003,0000012c,00002222,00003333,00005555,
```

# Path visualization

`python path_sim.py`  
To run the simulator of the 3D raster path scanner with a visualization of the object under test.
