# Setup
To install the dependencies a `requirements.txt` file has been provided.
Create a virtual environment and install the requirements with pip:

```
python -m venv env_octobee
source env_octobee/bin/activate
pip install -r requirements.txt
```

# Run
To run the simulation do:

`python run_tokamak_sim.py`

# Pathsim
To run the simulator of a 3D raster path scanner run:
`python path_sim.py`

# Magnetic simulation
To see examples of streamplots of B-fields of basic magnets e.g. sphere run:
`python sphere_magnet_streamplot.py`
