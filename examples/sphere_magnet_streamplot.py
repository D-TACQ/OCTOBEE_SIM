import matplotlib.pyplot as plt
import numpy as np

import magpylib as magpy

# Create a Matplotlib figure
fig, ax = plt.subplots()

# Create an observer grid in the xz-symmetry plane
ts = np.linspace(-5, 5, 40)
grid = np.array([[(x, 0, z) for x in ts] for z in ts])
X, _, Z = np.moveaxis(grid, 2, 0)

# Compute the B-field of a sphere magnet on the grid
cube = magpy.magnet.Sphere(polarization=(500, 0, 500), diameter=2.0)
B = cube.getB(grid)
Bx, _, Bz = np.moveaxis(B, 2, 0)
log10_norm_B = np.log10(np.linalg.norm(B, axis=2))

# Display the B-field with streamplot using log10-scaled
# color function and linewidth
splt = ax.streamplot(
    X,
    Z,
    Bx,
    Bz,
    density=1.5,
    color=log10_norm_B,
    linewidth=log10_norm_B,
    cmap="autumn",
)

# Add colorbar with logarithmic labels
cb = fig.colorbar(splt.lines, ax=ax, label="|B| (mT)")
ticks = np.array([3, 10, 30, 100, 300])
cb.set_ticks(np.log10(ticks))
cb.set_ticklabels(ticks)

# Create a circle patch
# The first argument is the center (x, y), the second is the radius
circle = plt.Circle((0, 0), 1, fill=False, color="k", linestyle="--", linewidth=2)

# Add the circle to the axes
ax.add_patch(circle)

# Set the aspect ratio to be equal, so the circle is not distorted
ax.set_aspect("equal", adjustable="box")

# Figure styling
ax.set(
    xlabel="x-position (mm)",
    ylabel="z-position (mm)",
)

plt.tight_layout()
plt.show()
