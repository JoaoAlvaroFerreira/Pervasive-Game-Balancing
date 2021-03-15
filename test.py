import rasterio
from rasterio.plot import show

raster_url = "Resources/Geotiff Files/France.tif"



img = rasterio.open(raster_url)
show(img)