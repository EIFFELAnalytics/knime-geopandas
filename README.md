# Documentation geopandas in KNIME
## Quick start
1. In your current workspace (project) click File > Import KNIME Workflow...
1. Browse to N:\Projectbureau\KNIME\geopandas-workflow\ and open geopandas-workflow.knwf.
1. Copy and paste the specific node(s) you need to your own workflow.
1. Optionally (probably) adjust parameters.
	1. Double-click on the node.
	1. Check the code section `# PARAMETERS` for relevant parameters and adjust them accordingly.

## Available geo-nodes
* *Source*: Read a [shapefile](https://nl.wikipedia.org/wiki/Shapefile). Adjust parameters `folder` and `filename`.
	* Note: the direction of the path separators (backslash or forward slash) does not matter here. To be sure, have the path as a raw string (`r'/path/to/file.shp'`).
* *Inspect Shape*: Inspection node. View output image for shape. View standard output for detailed info.
* *WKT To AC*: Convert WKT ([well-known text](https://en.wikipedia.org/wiki/Well-known_text)) to "AC" format.
* *Reduce Precision*: Reduce the precision of each (point in each) geometry. E.g. value 5.14958324 will reduce to 5.14958. Adjust `decimals`. This will significantly reduce the string length of each geometry.
* *Centroid*: Calculate the centroids of each polygon. The centroid geometry will overwrite the current geometry.
* *Simplify*: [Simplify](http://toblerity.org/shapely/manual.html#object.simplify) polygons will reduce the amount of points in a polygon. E.g. a heavily simplified circle will become a square. Adjust `tolerance`.
* *Dissolve*: Similar to a SQL group by statement, except for [dissolving](http://geopandas.org/aggregation_with_dissolve.html) (merging) the geometry column. Adjust `group_by_column`.
* *Spatial Join*: Similar to a SQL join, except that it will join geome on the geometry column of the left and right table. Adjust the join operation (`intersects`, `within` or `containts`) and the join type (`inner`, `left`, `right` or `outer`).
* *Isochrone*: Calculate the [isochrone](https://en.wikipedia.org/wiki/Isochrone_map) for each point in the geometry column. [Openrouteservice](https://github.com/GIScience/openrouteservice-py) is used for this. Adjust  `driving_time`. If you know what you are doing, you could adjust the advanced parameters in the code. <span style="color:red">Please also change the API `key` and/or `base_url` because the current key is my personal API development key and is very restricted.</span>
	* We're still working on hosting our own ORS server.
* *Distance Matrix*: Calculate a distance matrix from a table with origins and a table with destinations. Optionally supply the `table['column']` with origin names and the `table['column']` with destination names to use in the matrix. This uses openrouteservice and <span style="color:red">please change the API `key` and/or `base_url`.</span>

## How does such "geo-node" work?
The source code usually starts with a `# PARAMETERS` section where the user should make their own changes.

Below that is the functional code, which is specific for each node. In general, we transform the `input_table` into a [GeoDataFrame](http://geopandas.org/data_structures.html#geodataframe) called `gdf`. After that follows the node specific geographic operation and we transform `gdf` back to a regular [DataFrame](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html) called `output_table` which is passed on to the next KNIME node.

## Technical geographical information
### About projections
Geopandas has excellent [documentation about projections and coordinate reference systems](http://geopandas.org/projections.html).

Some properties of two very common CRS:

* *WGS84* - [EPSG: 4326](https://epsg.io/4326)
    * Amersfoort at (52.1561110, 5.3878270)
    * In degrees
    * ~ 70 km/degree longitude (horizontal)
    * ~ 110 km/degree latitude (vertical)
* *RD New Amersfoort* - [EPSG: 28992](https://epsg.io/28992)
    * Amersfoort at (142892.19, 470783.87)
    * In meters
