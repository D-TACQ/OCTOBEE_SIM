# Setup
To install the dependencies a `requirements.txt` file has been provided.
Create a virtual environment and install the requirements with pip:

```
python -m venv env_octo-bee
source env_octo-bee/bin/activate
pip install -r requirements.txt
```

# Run full simulation
The definition of all simulation parameters is done inside `config.yml`.
An example has been provided to get started.
You can copy this `config.yml` and edit `config.py` to point to your edited version.

To run a full simulation, from definition of simulation to output to disk of muxed data, run these files in order:

`path_scan_bfield_computation.py`

After this first run you can plot and check out your generated path with the `path_sim.py`

Then:
`offset_path_scan.py`

This will generate `.npy` files with results saved to disk in numpy array format. 
Example configuration will use ~15GB of disk space.

Finally to generate a data file in ACQ400 format:
`write_muxed_data.py`

# Path visualization
To run the simulator of the 3D raster path scanner with a visualization of the object under test then run:
`python path_sim.py`
