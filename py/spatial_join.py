import geopandas as gpd
from py.convert import knime_decorator_2_1

# Wrap the geopandas function sjoin
spatial_join = knime_decorator_2_1(gpd.sjoin)
