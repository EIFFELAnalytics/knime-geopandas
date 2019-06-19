import pandas as pd
import geopandas as gpd
from shapely import wkt as WKT
from functools import wraps


def df_to_gdf(df):
    """Convert a DataFrame (with wkt column) to a GeoDataFrame (with geometry
    column)."""
    gdf = gpd.GeoDataFrame(df, copy=True)
    gdf['geometry'] = df.wkt.apply(WKT.loads)
    return gdf.drop(columns='wkt')


def gdf_to_df(gdf):
    """Convert a GeoDataFrame (with geometry column) to a DataFrame (with wkt
    column)."""
    df = pd.DataFrame(gdf, copy=True)
    df['wkt'] = gdf.geometry.apply(WKT.dumps, trim=True)
    return df.drop(columns='geometry')


def knime_decorator_1_1(func):
    """Decorator for a KNIME 1 -> 1 Python script node.

    A convenient and generic way to operate native geopandas functions on KNIME
    input_table and output_table.

    """

    # Use functools.wraps to inherit the docstring from the original function
    @wraps(func)
    def wrapper(input_table, *args, **kwargs):
        """This docstring should not be seen.

        Unfortunately this is not the case with the IntelliSense popup window
        in VS Code on Windows 10. However, `func.__doc__` does give the correct
        docstring.

        """

        # Convert to a geodataframe
        input_gdf = df_to_gdf(input_table)

        # Execute the 1 -> 1 function
        output_gdf = func(input_gdf, *args, **kwargs)

        # Convert back to a dataframe
        output_table = gdf_to_df(output_gdf)
        return output_table

    return wrapper


def knime_decorator_2_1(func):
    """Decorator for a KNIME 2 -> 1 Python script node"""

    # Use functools.wraps to inherit the docstring of the original function
    @wraps(func)
    def wrapper(input_table_1, input_table_2, *args, **kwargs):

        # Convert to geodataframes
        input_gdf_1 = df_to_gdf(input_table_1)
        input_gdf_2 = df_to_gdf(input_table_2)

        # Execute the 2 -> 1 function
        output_gdf = func(input_gdf_1, input_gdf_2, *args, **kwargs)

        # Convert back to dataframe
        output_table = gdf_to_df(output_gdf)
        return output_table

    return wrapper
