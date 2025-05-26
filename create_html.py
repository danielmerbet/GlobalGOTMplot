import xarray as xr
import plotly.graph_objects as go
import numpy as np
import plotly.io as pio

# === Parameters ===
nc_path = "gotm_20crv3-era5_obsclim_histsoc_default_surftemp_global_annual_1901_2021.nc"
output_html = "index.html"
year_to_plot = 2021  # Change year as needed

# === Load Data ===
ds = xr.open_dataset(nc_path)
years = ds.time.dt.year.values
if year_to_plot not in years:
    raise ValueError(f"Year {year_to_plot} not found in dataset")

t_index = int(np.where(years == year_to_plot)[0][0])
temp = ds['surftemp'].isel(time=t_index) - 273.15  # Kelvin to °C

# === Plotly Heatmap ===
fig = go.Figure(data=go.Heatmap(
    z=temp.values,
    x=ds['lon'].values,
    y=ds['lat'].values,
    colorscale='Jet',
    colorbar=dict(title='°C'),
    zmin=-2,
    zmax=35
))

fig.update_layout(
    title=f"Lake Surface Temperature in {year_to_plot}",
    xaxis_title="Longitude",
    yaxis_title="Latitude",
    height=700
)

# === Export to Standalone HTML ===
pio.write_html(fig, file=output_html, full_html=True, include_plotlyjs='cdn')

print(f"✅ Created {output_html}. You can now commit it to GitHub Pages.")

