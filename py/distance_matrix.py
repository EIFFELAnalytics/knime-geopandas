# FIXME: It returns the wrong error when overloading the server
import requests
import pandas as pd
if __name__ == "__main__":
    from convert import df_to_gdf, gdf_to_df
else:
    from py.convert import df_to_gdf, gdf_to_df


def request_distance_matrix(locations, **params):
    # Based on example Python code from https://openrouteservice.org/dev/#/api-docs/v2/matrix/{profile}/post
    body = {'locations': locations, **params}
    headers = {
        'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
        'Authorization': None
    }
    r = requests.post(
        'http://localhost:8080/ors/v2/matrix/driving-car',
        json=body,
        headers=headers
    )
    #print(r.status_code, r.reason)

    # Return the response JSON
    return r.json()


def json_to_matrix(json):
    # FIXME: Wrong index (sources).
    # Bug in ORS: https://github.com/GIScience/openrouteservice/issues/560
    return pd.DataFrame(
        data=json['durations'],
        #index=[str(loc['location']) for loc in json['sources']],
        #columns=[str(loc['location']) for loc in json['destinations']]
    )


def distance_matrix(input_table_1, input_table_2):
    """Calculate travel distance or duration for origins and destinations. By
    default it returns the duration matrix in seconds.

    Args:
        input_table_1: DataFrame with the travel origins in the `wkt` column.
        The geometry should represent a Point. Other geometries such as
        Polygons are not supported because theydon't have a X and Y property.
        input_table_2: Same as input_table_1 but with the destinations.

    Returns:
        The duration matrix (DataFrame) with travel times from origins to
        destinations in seconds.
    
    Openrouteservice docs: https://openrouteservice.org/dev/#/api-docs/v2/matrix/{profile}/post

    """

    #
    gdf1 = df_to_gdf(input_table_1)
    gdf2 = df_to_gdf(input_table_2)

    # Extract 1 list of all XY and assign origins and destinations with indexes
    XY = [(Point.x, Point.y) for Point in gdf1.geometry.append(gdf2.geometry)]
    idx_origins = list(range(len(gdf1)))
    idx_destinations = list(range(len(gdf1), len(XY)))

    # Advanced parameters. Don't change these if you don't know what you are
    # doing. For all (optional) parameters, see
    # https://openrouteservice.org/dev/#/api-docs/v2/matrix/{profile}/post
    params = {
        'locations': XY,
        'sources': idx_origins,
        'destinations': idx_destinations,
    }

    # Request the distance / duration matrix
    response = request_distance_matrix(**params)

    # Parse the response into a dataframe
    matrix = json_to_matrix(response)
    return matrix


if __name__ == "__main__":
    # Run a simple test with staight-forward coordinates
    params = {
        'locations': [[5, 52], [5.2, 52], [5.4, 52], [5.6, 52], [5.8, 52]],
        'sources': [0, 1],
        'destinations': [2, 3, 4],
    }
    response = request_distance_matrix(**params)
    matrix = json_to_matrix(response)
    print(matrix)
