

def replace_wkt_with_ac(wkt):
    ac = (wkt
          .replace('MULTIPOLYGON (((', '')
          .replace(')))', '')
          .replace(')), ((', '@')
          .replace('POLYGON ((', '')
          .replace('))', '')
          .replace('), (', '@')
          .replace(', ', ':')
          .replace(' ', ',')
          )
    return ac


def wkt_to_ac(df_with_wkt):
    """Convert WKT format to AC format."""

    # Copy input table and convert wkt to AC into new column
    df_with_ac = df_with_wkt.copy()
    df_with_ac['AC'] = df_with_wkt.wkt.apply(replace_wkt_with_ac)

    # Return as a dataframe
    return df_with_ac


#TODO: if __name__ == "__main__":
    # Run some tests
