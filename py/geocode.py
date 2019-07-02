"""Module to show how to geocode with openrouteservice.

Geocoding can not be requested on our local ORS instance server. So we have to
query the official API and use a (free) API key.

API playground: https://openrouteservice.org/dev/#/api-docs/geocode/search/get

"""
import requests
from shapely.geometry import Point
try:
    import credentials
except:
    pass


def request_ors_geocode(query, api_key):
    params={
        # Insert API key here
        'api_key': api_key,
        'text': query,
        'boundary.country': 'NL',
        'size': 0,
    }
    headers = {
        'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
    }
    call = requests.get(
        'https://api.openrouteservice.org/geocode/search',
        params=params,
        headers=headers,
    )
    print(call.status_code, call.reason)
    # TODO: Could check properties > layer for correct geographic type
    return call.json()


# TODO: Write this:
def geocode(input_table, api_key):
    """Geocode all text (queries) in column `query` of input_table. Returns a
    point (WKT) for each query.
    
    This function requests the official openrouteservice API
    (https://openrouteservice.org/dev/#/api-docs/geocode/search/get), so you'll
    need a (free) API key to run.

    """
    
    assert ('query' in input_table.columns), "The geocode queries should be in column `query` in input_table."

    output_table = input_table.copy()
    output_table['wkt'] = input_table['query'].apply(lambda q: json_to_wkt(request_ors_geocode(q, api_key)))

    return output_table


def json_to_wkt(json):
    """Extract coordinates from ORS response json and return a shapely Point."""
    coordinates = json['features'][0]['geometry']['coordinates']
    return Point(*coordinates).wkt


def geocode_debug(*args, **kwargs):
    # Static return JSON for query = 5653AX
    # Using this won't cost me ORS quota
    return {'geocoding': {'version': '0.2', 'attribution': 'openrouteservice.org | OpenStreetMap contributors | Geocoding by Pelias', 'query': {'text': '5653AX', 'size': 1, 'layers': ['venue', 'street', 'country', 'macroregion', 'region', 'county', 'localadmin', 'locality', 'borough', 'neighbourhood', 'continent', 'empire', 'dependency', 'macrocounty', 'macrohood', 'microhood', 'disputed', 'postalcode', 'ocean', 'marinearea'], 'private': False, 'boundary.country': ['NLD'], 'lang': {'name': 'English', 'iso6391': 'en', 'iso6393': 'eng', 'defaulted': True}, 'querySize': 20, 'parser': 'libpostal', 'parsed_text': {'postalcode': '5653ax'}}, 'warnings': ["out-of-range integer 'size', using MIN_SIZE", "performance optimization: excluding 'address' layer"], 'engine': {'name': 'Pelias', 'author': 'Mapzen', 'version': '1.0'}, 'timestamp': 1562058766635}, 'type': 'FeatureCollection', 'features': [{'type': 'Feature', 'geometry': {'type': 'Point', 'coordinates': [5.455383, 51.427997]}, 'properties': {'id': '891069277', 'gid': 'whosonfirst:postalcode:891069277', 'layer': 'postalcode', 'source': 'whosonfirst', 'source_id': '891069277', 'name': '5653AX', 'postalcode': '5653AX', 'postalcode_gid': 'whosonfirst:postalcode:891069277', 'confidence': 1, 'match_type': 'exact', 'accuracy': 'centroid', 'country': 'Netherlands', 'country_gid': 'whosonfirst:country:85633337', 'country_a': 'NLD', 'region': 'Noord-Brabant', 'region_gid': 'whosonfirst:region:85687035', 'region_a': 'NB', 'locality': 'Eindhoven', 'locality_gid': 'whosonfirst:locality:101751819', 'continent': 'Europe', 'continent_gid': 'whosonfirst:continent:102191581', 'label': '5653AX, Eindhoven, Netherlands'}, 'bbox': [5.45502233505, 51.4277038574, 5.45573616028, 51.4282913208]}], 'bbox': [5.45502233505, 51.4277038574, 5.45573616028, 51.4282913208]}


if __name__ == "__main__":
    # Tests here!
    json = request_ors_geocode('5653AX', credentials.api_key)
    w = json_to_wkt(json)
    print(w)

    import pandas as pd
    df = pd.DataFrame({
        #'a': [1,2,3],
        #'b': [4,5,6],
        'query': ['Eindhoven Airport', 'Schiphol', '5653AX']
    })

    df2 = geocode(df, credentials.api_key)

    print(df)
    print(df2)
