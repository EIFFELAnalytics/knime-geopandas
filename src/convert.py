# HEADER
# Includes some functions which are required for the KNIME geopandas nodes.
import pandas as pd
import geopandas as gpd
from shapely import wkt as WKT

# Convert geopandas (with geometry column) to pandas (with wkt column)
def gdf_to_df(gdf):
    df = pd.DataFrame(gdf, copy=True)
    df['wkt'] = gdf.geometry.apply(lambda wkt: WKT.dumps(wkt, trim=True))
    df.drop(columns='geometry', inplace=True)
    return df

# Convent pandas (with wkt column) to geopandas (with geometry column)
def df_to_gdf(df):
    gdf = gpd.GeoDataFrame(df, copy=True)
    gdf['geometry'] = df.wkt.apply(WKT.loads)
    gdf.drop(columns='wkt', inplace=True)
    return gdf