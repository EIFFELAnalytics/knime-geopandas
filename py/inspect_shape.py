import numpy as np
import pandas as pd
import re
from io import BytesIO
from py.convert import df_to_gdf

# Don't hide columns
pd.set_option('display.max_columns', None)


def inspect_shape(df, **kwargs):
    """Inspect a shape.

    Args:
        df (DataFrame): Dataframe with a `wkt` column.
            See well-known text: https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry
        **kwargs: Optional arguments get passed on to GeoDataFrame.plot()

    Returns:
        binary: Image of the shape.

    """

    # First, print a bunch of useful info
    print('Shape:', df.shape)
    print('Average number of character/geometry: %.1f' %
          np.mean(df.wkt.apply(lambda wkt: len(wkt))))
    print('Average number of points/geometry: %.1f' %
          np.mean(df.wkt.apply(lambda wkt: len(wkt.split(',')))))
    print('Average precision/point: %.1f' %
          np.mean(
            df.wkt.apply(
                lambda wkt: np.mean([len(decimals)
                for decimals in re.findall('[0-9]+\.([0-9]*)', wkt)])
    )))
    print('Columns:', *list(df.columns), sep='\n')

    # Show the first 5 rows when using Jupyter
    try:
        display(df.head())
    except NameError:
        pass

    # Create plot and write the binary image into a buffer
    # Note: plot() will show in Jupyter with %matplotlib inline
    gdf = df_to_gdf(df)
    buffer = BytesIO()
    gdf.plot(**kwargs).get_figure().savefig(buffer, format='png')

    # Return the buffer content for the output_image in KNIME
    return buffer.getvalue()
