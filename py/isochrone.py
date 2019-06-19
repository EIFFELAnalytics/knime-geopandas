from shapely.geometry import shape
import openrouteservice
from openrouteservice.isochrones import isochrones
from py.convert import df_to_gdf, gdf_to_df


def isochrone(df_with_wkt, driving_time):
    """Calculate an isochrone for each Point in the dataframe.

    The geometry must be a Point. Other geometries as Polygons are not
    supported.

    Isochrones: https://en.wiktionary.org/wiki/isochrone
    Openrouteservice docs (isochrone API): https://openrouteservice.org/documentation/#/reference/isochrones  
    Openrouteservice docs (Python API): http://openrouteservice-py.readthedocs.io/en/latest/

    """

    # Initialize openrouteservice
    client = openrouteservice.Client(
        key='5b3ce3597851110001cf6248bbe961d3ef8c4b2ab871c873f96e3c82',
        #base_url='http://localhost:8080/ors'
    )

    # Request an isochrone for a Point
    # How to use **kwargs: http://book.pythontips.com/en/latest/args_and_kwargs.html#usage-of-kwargs
    def request_isochrone(Point, **kwargs):
        # First extract (X,Y) from the Point
        XY = (Point.x, Point.y)
        # Then request the isochrone
        isochrone = isochrones(client, locations=[XY], **kwargs)
        # The returned JSON is always a FeatureCollection of 1 Feature with a geometry (= GeoJSON)
        return shape(isochrone['features'][0]['geometry'])

    # Advanced parameters. Don't change these if you don't know what you are doing.
    # See: https://openrouteservice.org/dev/#/api-docs/isochrones/get
    params = {
        'range': [60 * driving_time],
        'interval': [],
        'range_type': 'time',
        'profile': 'driving-car'
    }

    # Convert to geodataframe
    gdf = df_to_gdf(df_with_wkt)

    # Request isochrones. This overwrites the current geometry!
    gdf.geometry = gdf.geometry.apply(lambda P: request_isochrone(P, **params))

    # Return as dataframe
    return gdf_to_df(gdf)
