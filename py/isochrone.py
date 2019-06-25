import requests
from shapely.geometry import shape
if __name__ == "__main__":
    from convert import df_to_gdf, gdf_to_df
else:
    from py.convert import df_to_gdf, gdf_to_df


def request_isochrone(location, range, **params):
    # Based on example Python code from https://openrouteservice.org/dev/#/api-docs/v2/isochrones/{profile}/post
    body = {'locations': location, 'range': range, **params}
    headers = {
        'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
        'Authorization': None
    }
    r = requests.post(
        'http://localhost:8080/ors/v2/isochrones/driving-car',
        json=body,
        headers=headers
    )
    # print(r.status_code, r.reason)
    return r.json()


def json_to_shape(json):
    # Use the geometry of the first feature
    return shape(json['features'][0]['geometry'])


def isochrone(df, driving_time):
    """Calculate an isochrone for each Point in the dataframe.

    Args:
        df: DataFrame with a `wkt` column. The geometry should represent a 
        Point. Other geometries such as Polygons are not supported because they
        don't have a X and Y property.
        driving_time (int): Requested driving time in minutes.

    Returns:
        DataFrame with a `wkt` column which represents the isochrones.

    Note:
        Multiple isochrones per point are not supported because a GeoDataFrame
        only has 1 `geometry` column.

    Isochrones: https://en.wiktionary.org/wiki/isochrone
    Openrouteservice docs (isochrone API): https://openrouteservice.org/dev/#/api-docs/v2/isochrones/{profile}/post

    """
    
    # Convert to geodataframe
    gdf = df_to_gdf(df)

    # Advanced parameters. Don't change these if you don't know what you are
    # doing. For all (optional) parameters, see
    # https://openrouteservice.org/dev/#/api-docs/v2/isochrones/{profile}/post
    params = {
        'range': [60*driving_time],
        'range_type': 'time',
        'location_type': 'start',
    }

    # Request isochrones. This overwrites the current geometry!
    gdf.geometry = gdf.geometry.apply(
        lambda P: json_to_shape(request_isochrone([[P.x, P.y]], **params))
    )

    # Return as dataframe
    return gdf_to_df(gdf)


import pandas as pd
if __name__ == "__main__":
    # Run a simple test
    isoc = request_isochrone([5, 52], 10)
    print(isoc)

    #
    df = pd.DataFrame(data={'id': 'Here', 'wkt': 'POINT (5 52)'}, index=[0])
    isoch = isochrone(df, 10)
