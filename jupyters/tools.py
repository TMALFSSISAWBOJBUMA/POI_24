import csv
from typing import Iterable, Callable
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def spread_voxels(voxels):
    return voxels[:, 0], voxels[:, 1], voxels[:, 2]


def plot_points(
    x: Iterable | np.ndarray = [],
    y: Iterable | np.ndarray = [],
    z: Iterable | np.ndarray = [],
    voxels: np.ndarray = None,
    ax: Axes3D = None,
):

    if ax is None:
        fig = plt.figure()
        ax = fig.add_subplot(projection="3d")

    if voxels is None:
        ax.scatter(x, y, z)
    else:
        ax.scatter(*spread_voxels(voxels))

    ax.set_aspect("equal", "box")
    ax.get_figure().tight_layout()
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    return ax, ax.get_figure()


def create_surface_mesh(
    x_lim: Iterable | np.ndarray,
    y_lim: Iterable | np.ndarray,
    z_func: Callable[[np.ndarray, np.ndarray], np.ndarray],
    n_points: int = 5,
):
    x = np.linspace(min(x_lim), max(x_lim), n_points)
    y = np.linspace(min(y_lim), max(y_lim), n_points)
    x, y = np.meshgrid(x, y)
    z = z_func(x, y)
    return x, y, z


def plot_surface(
    x: Iterable | np.ndarray = [],
    y: Iterable | np.ndarray = [],
    z: Iterable | np.ndarray = [],
    ax: Axes3D = None,
    **plot_kwargs
):

    if ax is None:
        fig = plt.figure()
        ax = fig.add_subplot(projection="3d")

    # ax.plot_wireframe(x, y, z,  rstride=10, cstride=10, **plot_kwargs)
    colour = plot_kwargs.pop("color", "b")
    ax.plot_surface(x, y, z, color=colour, **plot_kwargs)
    ax.get_figure().tight_layout()
    ax.set_aspect("equal", "box")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    return (
        ax,
        ax.get_figure(),
    )


def save_cloud(filepath: str, data: Iterable):
    with open(filepath, "w", newline="") as fp:
        wr = csv.writer(fp)
        wr.writerows(data)


def read_cloud(filepath: str):
    with open(filepath, newline="") as fp:
        reader = csv.reader(fp)
        data = []
        for row in reader:
            data.append(row)
        xyz = np.array(data, dtype=float)
        return xyz
