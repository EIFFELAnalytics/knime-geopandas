from py.convert import df_to_gdf, gdf_to_df


def simplify(df_with_wkt, decimals):
    """Simplify shapes.

    The simplification algorithm tries to draw a new geometry from as few points
    as possible while remaining within the tolerance distance of the original
    geometry.

    Args:
        df_with_wkt (DataFrame).
        decimals (int): Desired precision in amount of decimals.

    Shapely docs: https://shapely.readthedocs.io/en/stable/manual.html#object.simplify

    """

    # Convert to geodataframe
    gdf = df_to_gdf(df_with_wkt)

    # Simplify with fixed tolerance
    tolerance = 10 ** -decimals
    gdf.geometry = gdf.geometry.simplify(tolerance, preserve_topology=True)

    # TODO: Dynamic simplify. Tolerance is 0.01% van de omtrek
    #def dynamic_simplify(geom):
    #    return geom.simplify(geom.length * 0.0001, preserve_topology=True)
    #
    #gdf.geometry = gdf.geometry.apply(dynamic_simplify)

    # Return as a dataframe
    return gdf_to_df(gdf)
