import csv
from typing import Iterable, Callable
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os

ROOT_PATH = os.path.join(__file__, os.pardir, os.pardir)


def path_from_root(*args):
    return os.path.normpath(os.path.join(ROOT_PATH, *args))


def spread_voxels(voxels):
    return voxels[:, 0], voxels[:, 1], voxels[:, 2]


def px_to_inch(w: int | tuple, h: int | None = None):
    size = (w, h) if h else w
    dpi = plt.rcParams["figure.dpi"]
    return [s / dpi for s in size]


def plot_points(
    x: Iterable | np.ndarray = [],
    y: Iterable | np.ndarray = [],
    z: Iterable | np.ndarray = [],
    voxels: np.ndarray = None,
    ax: Axes3D = None,
    **plot_kwargs
):
    if ax is None:
        fig = plt.figure()
        ax = fig.add_subplot(projection="3d")
    else:
        fig = ax.get_figure()

    if "figsize" in plot_kwargs:
        fig.set_size_inches(plot_kwargs.pop("figsize"))

    if voxels is None:
        ax.scatter(x, y, z, **plot_kwargs)
    else:
        ax.scatter(*spread_voxels(voxels), **plot_kwargs)

    ax.set_aspect("equal", "box")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    fig.tight_layout()
    return ax, fig


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
    else:
        fig = ax.get_figure()

    if "figsize" in plot_kwargs:
        fig.set_size_inches(plot_kwargs.pop("figsize"))

    # ax.plot_wireframe(x, y, z,  rstride=10, cstride=10, **plot_kwargs)
    colour = plot_kwargs.pop("color", "b")
    ax.plot_surface(x, y, z, color=colour, **plot_kwargs)
    ax.set_aspect("equal", "box")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    fig.tight_layout()
    return ax, fig


def save_cloud(filepath: str, data: Iterable, **writer_kwargs):
    with open(filepath, "w", newline="") as fp:
        wr = csv.writer(fp, **writer_kwargs)
        wr.writerows(data)


def read_cloud(filepath: str, **reader_kwargs):
    with open(filepath, newline="") as fp:
        reader = csv.reader(fp, **reader_kwargs)
        data = []
        for row in reader:
            data.append(row)
        xyz = np.array(data, dtype=float)
        return xyz
