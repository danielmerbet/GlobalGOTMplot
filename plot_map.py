import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cmocean.cm as cmo
import hvplot.xarray
import panel as pn
import geoviews
import holoviews as hv
from bokeh.io import save
from bokeh.plotting import figure
import numpy as np
from matplotlib.cm import get_cmap
from matplotlib.colors import ListedColormap

ds = xr.open_dataset('/home/dmercado/Documents/GlobalGOTMplot/data/gotm_20crv3-era5_obsclim_histsoc_default_surftemp_global_annual_1901_2021.nc')

# Extract surface temperature for the year 2021 (last time step)
temp = ds['surftemp'].isel(time=-1)

title = f"Surface Temperature in {ds.time[-1].dt.year.values}"

# Optional: Create a custom colormap with more colors
# Take an existing cmap and extend it with more interpolated colors
base_cmap = get_cmap('coolwarm', 256)
extended_colors = base_cmap(np.linspace(0, 1, 512))  # Double the number of color samples
custom_cmap = ListedColormap(extended_colors)

# Ensure it's 2D
temp_2d = temp.isel()  # This removes extra dimensions

# Set up map
fig = plt.figure(figsize=(14, 8))
ax = plt.axes(projection=ccrs.Robinson())
ax.set_global()

# Add geographic features
ax.add_feature(cfeature.LAND, zorder=1, facecolor='lightgray')
ax.add_feature(cfeature.COASTLINE)

# Plot contour
contour = temp_2d.plot.contourf(
    ax=ax,
    transform=ccrs.PlateCarree(),
    cmap=cmo.thermal,
    levels=20,
    add_colorbar=True,
    cbar_kwargs={'shrink': 0.7, 'label': 'Temperature [°C]'},
    vmin=temp_2d.min(), vmax=temp_2d.max()
)

plt.title("Global Surface Temperature", fontsize=16)
plt.tight_layout()
plt.savefig("global_temperature_heatmap.png", dpi=300, bbox_inches='tight')
plt.show()




# Animated plot with extended/custom cmap and more levels
animated_plot = temp.hvplot.contourf(
    x='lon', y='lat',
    geo=True,
    projection=ccrs.Robinson(),
    transform=ccrs.PlateCarree(),
    cmap=custom_cmap,  # Use the extended/custom colormap
    coastline=True,
    title='Surface Temperature Over Time',
    clabel='Temperature [°C]',
    #groupby='time',  # Uncommented so animation happens over time
    levels=50,       # Increased number of contour levels for smoother gradients
    width=1500,
    height=900,
    xlim=(-180, 180),
    ylim=(-90, 90)
)

# Save to HTML
hv.extension('bokeh')
save(hv.render(animated_plot), filename="index.html")
