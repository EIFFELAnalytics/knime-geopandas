from os.path import join
import geopandas as gpd
from py.convert import gdf_to_df


def read_shapefile(filename, *args, **kwargs):
    """Read a shapefile, map it to WGS84 and return as a dataframe with WKT.

    Further reading: http://geopandas.org/io.html

    Args:
        filename (str): The absolute or relative path to the file or URL to be
        opened.
        *args and **kwargs are passed on to `gpd.read_file()`.

    """

    # Read the file with geopandas
    print('Reading file:', filename)
    gdf = gpd.read_file(filename, *args, **kwargs)

    # Reproject to the coordinate reference system WGS84 (a.k.a. long/lat)
    # This HAS to be done here, because we'll lose the CRS when converting to a
    # dataframe. WGS84 is the official standard for GeoJSON: https://tools.ietf.org/html/rfc7946#section-4
    wgs84 = {'init': 'epsg:4326'}
    if gdf.crs != wgs84:
        print('Reprojecting to WGS84')
        # In case of error here, downgrading fiona to 1.7 might help
        gdf.to_crs(wgs84, inplace=True)

    # Return as a dataframe
    return gdf_to_df(gdf)


# Maybe: Can we wrap gpd.read_file so we can preserve the docstring?
