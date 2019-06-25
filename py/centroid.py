from py.convert import df_to_gdf, gdf_to_df


def centroid(df_with_wkt):
    """Convert shapes to centroids (Points).

    Shapely docs: https://shapely.readthedocs.io/en/stable/manual.html#object.centroid

    """

    # Convert to geodataframe
    gdf = df_to_gdf(df_with_wkt)

    # Calculate centroids
    # Note: this overwrites the current geometry column
    gdf.geometry = gdf.geometry.centroid

    # Return as a dataframe
    return gdf_to_df(gdf)
