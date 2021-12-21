from . import var
import matplotlib as mpl
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.util import add_cyclic_point
import numpy as np

mpl.rcParams['axes.formatter.limits'] = (2, -2)


def plot_vertical_profile(fig, state, name, var_names):
    """Plots all zonal winds for different rotation rates"""
    fig.clf()
    fig.text(0.02, 0.92, name)
    fig.text(0.82, 0.92, state['time'].strftime(var.DATETIME_FORMAT))
    for i, v in enumerate(var_names):
        ax = fig.add_subplot(1, 3, i + 1)
        state[v].coords['lat'] = state['latitude'][:, 0]
        state[v].mean(dim='lon').plot.contourf(ax=ax, cmap=var_names[v]['cm'], levels=100)  # , robust=True)
        ax.set_title(var_names[v]['title'])
    fig.tight_layout()
    fig.subplots_adjust(top=0.8)
    fig.suptitle('Vertical Profile', fontsize=16)
    fig.show()


def plot_sfc_map(fig, state, name, var_names):
    """Plots all zonal winds for different rotation rates"""
    fig.clf()
    fig.text(0.02, 0.96, name)
    fig.text(0.82, 0.96, state['time'].strftime(var.DATETIME_FORMAT))
    for i, v in enumerate(var_names):
        ax = fig.add_subplot(2, 2, i + 1, projection=ccrs.PlateCarree())
        state[v].coords['lat'] = state['latitude'][:, 0]
        state[v].coords['lon'] = state['longitude'][0]
        if 'surface' in v:
            plot_state = state[v]
        else:
            plot_state = state[v][0]
        data = plot_state
        data, lon = add_cyclic_point(data, coord=state['longitude'][0])
        lat = state['latitude'][:, 0]
        if np.min(data) < 0.:
            levels = np.linspace(-np.max(np.abs(data)), np.max(np.abs(data)), 100)
        else:
            levels = 100
        cont = ax.contourf(lon, lat, data, cmap=var_names[v]['cm'], levels=levels)  # , robust=True)
        ax.ticklabel_format(scilimits=(2, -2), useMathText=True)
        fig.colorbar(cont, ax=ax)
        ax.set_title(var_names[v]['title'])
        ax.add_feature(cfeature.COASTLINE.with_scale('50m'))
        ax.set_aspect('auto', adjustable=None)
    fig.tight_layout()
    fig.subplots_adjust(top=0.9)
    fig.suptitle('Surface Map', fontsize=16)

