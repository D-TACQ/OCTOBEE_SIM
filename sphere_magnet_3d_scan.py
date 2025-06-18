import matplotlib.pyplot as plt
import numpy as np

import magpylib as magpy


def compute_b_field(grid):
    # Compute the B-field of a sphere magnet on the grid
    sphere = magpy.magnet.Sphere(polarization=(500, 0, 500), diameter=2.0)
    B = sphere.getB(grid)
    return B


def create_streamplot(P1, P2, B, plane="xy"):
    """
    Creates a streamplot along the plane.

    P1 and P2 are the plane data (e.g. P1 = X and P2 = Y if plane = xy)
    plane = xy, xz, or yz
    """
    # Create a Matplotlib figure
    fig, ax = plt.subplots()

    if plane.lower() == "xy":
        B1, B2, _ = np.moveaxis(B, 2, 0)
        log10_norm_B = np.log10(np.linalg.norm(B, axis=2))
        xlabel = "x"
        ylabel = "y"
    if plane.lower() == "xz":
        # Original, others need modded
        B1, _, B2 = np.moveaxis(B, 2, 0)
        log10_norm_B = np.log10(np.linalg.norm(B, axis=2))
        xlabel = "x"
        ylabel = "z"
    if plane.lower() == "yz":
        _, B1, B2 = np.moveaxis(B, 2, 0)
        log10_norm_B = np.log10(np.linalg.norm(B, axis=2))
        xlabel = "y"
        ylabel = "z"

    # Display the B-field with streamplot using log10-scaled
    # color function and linewidth
    splt = ax.streamplot(
        P1,
        P2,
        B1,
        B2,
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
        xlabel=f"{xlabel}-position (mm)",
        ylabel=f"{ylabel}-position (mm)",
    )

    plt.tight_layout()
    plt.show(block=False)


if __name__ == "__main__":

    # Create an observer grid in the xz-symmetry plane
    ts = np.linspace(-5, 5, 40)
    grid_xz = np.array([[(x, 0, z) for x in ts] for z in ts])
    Xxz, _, Zxz = np.moveaxis(grid_xz, 2, 0)

    # Create an observer grid in the xy-symmetry plane
    ts = np.linspace(-5, 5, 40)
    grid_xy = np.array([[(x, y, 0) for x in ts] for y in ts])
    Xxy, Yxy, _ = np.moveaxis(grid_xy, 2, 0)

    # Create an observer grid in the yz-symmetry plane
    ts = np.linspace(-5, 5, 40)
    grid_yz = np.array([[(0, y, z) for y in ts] for z in ts])
    _, Yyz, Zyz = np.moveaxis(grid_yz, 2, 0)

    # Create an observer grid in the xyz volume
    ts = np.linspace(-5, 5, 40)
    grid_xyz = np.array([[[(x, y, z) for x in ts] for y in ts] for z in ts])

    Bxz = compute_b_field(grid_xz)
    Bxy = compute_b_field(grid_xy)
    Byz = compute_b_field(grid_yz)

    Bxyz = compute_b_field(grid_xyz)

    create_streamplot(Xxz, Zxz, Bxz, plane="xz")
    create_streamplot(Xxy, Yxy, Bxy, plane="xy")
    create_streamplot(Yyz, Zyz, Byz, plane="yz")
    plt.show()
    print(f"Shape of Bxyz {Bxyz.shape}")
    magnitudes = np.linalg.norm(Bxyz, axis=3)
    max_magnitude = magnitudes.max()
    index_max_mag = np.unravel_index(magnitudes.argmax(), magnitudes.shape)
    print(f"index of max magnitude is {index_max_mag} and value is {max_magnitude}")
    sorted_flattened_magnitudes = magnitudes.flatten()
    sorted_flattened_magnitudes.sort()
    plt.hist(sorted_flattened_magnitudes)
    plt.show()
