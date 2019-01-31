# HEADER
# Includes some defined functions which are required for the KNIME geopandas nodes.
import geopandas as gpd
import pandas as pd
from shapely import wkt as WKT
import re
import numpy as np

# Convert geopandas (with geometry column) to pandas (with wkt column)
def geometry_to_wkt(gdf, **kwargs):
    df = pd.DataFrame(gdf, copy=True)
    df['wkt'] = gdf.geometry.apply(
        lambda wkt: WKT.dumps(wkt, trim=True, rounding_precision=kwargs.get('rounding_precision', -1))
    )
    df.drop(columns='geometry', inplace=True)
    return df

# Convent pandas (with wkt column) to geopandas (with geometry column)
def wkt_to_geometry(df):
    gdf = gpd.GeoDataFrame(df, copy=True)
    gdf['geometry'] = df.wkt.apply(WKT.loads)
    gdf.drop(columns='wkt', inplace=True)
    return gdf

# Bereken wat extra info (vind ik interessant)
def extract_info(wkt, *args):
    # Calculate specs
    info = {'points': len(wkt.split(',')),\
            'chars': len(wkt),\
            'precision': np.mean([len(decimals) for decimals in re.findall('\.([0-9]*)', wkt)])}
    # Return dictionary or list with values of one spec
    if not args:
        return info
    else:
        return info.get(args[0])