import geopandas as gpd
from py.convert import knime_decorator_1_1

# Wrap geopandas dissolve function
dissolve = knime_decorator_1_1(gpd.GeoDataFrame.dissolve)
