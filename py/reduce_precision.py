import numpy as np
import pandas as pd
import re


def crop_to_decimals(text, decimals=0):
    # Match all numbers with more than `decimals` numbers behind the dot and
    # replace the match with the captured group, thereby removing excess decimals
    return re.sub(
        r'([0-9]+\.[0-9]{' + str(decimals) + r'})[0-9]+',
        r'\1',
        text
    )


def reduce_precision(df_with_wkt, decimals=0):
    """Reduce the precision of (points of) the shapes to a given number of
    decimals.

    Crop each number it finds in the WKT with a regex. E.g. the point of EIFFEL
    Arnhem: `(5.9812899999999445, 51.9775966)` becomes `(5.98128, 51.97759)`.
    This will drastically reduce the length of the WKT string.

    In the Nederlands 1 m equals approximately 1e-5 degree (long/lat), so
    specify decimals as 5 for approximately 1 m precision.

    Args:
        df_with_wkt (DataFrame): Dataframe with a `wkt` column.
        decimals (int): Number of decimals to crop to

    Returns:
        DataFrame.

    """

    # Convert the data frame to plain text, JSON actually
    json = df_with_wkt.to_json()

    # Crop. Note: Rounding these digits rathing then cropping would be more
    # correct, but takes a long time
    cropped_json = crop_to_decimals(json, decimals)

    # Return as a dataframe
    return pd.read_json(cropped_json)


if __name__ == "__main__":
    # Do some tests
    assert crop_to_decimals('1.123456 and 0.00999', 2) == '1.12 and 0.00'
    assert crop_to_decimals('123.567') == '123'
