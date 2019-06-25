# Geopandas in KNIME
## Quick start
1. In KNIME click File > Import KNIME Workflow...
1. Browse to N:\Projectbureau\KNIME\geopandas-workflow\ and open the example workflow geopandas-workflow.knwf.
    * Or clone this repository to your local computer take it from there.
1. Copy the entire folder py into your KNIME workspace folder. This is where the nodes will import the source code from.
1. Copy and paste the specific nodes you need from the example workflow to your own workflow.
1. Optionally (probably) edit parameters in the nodes. See the `# PARAMETERS` section inside each node.

## Available nodes
* Read shapefile
* Inspect shape
* Reduce precision
* Simplify
* WKT to AC
* Centroids
* Distance/duration matrix
* Isochrones
* Dissolve
* Spatial join

View the KNIME workflow and the demos folder for examples on how to use these.

## Some extra info
### Geographic projections
Geopandas has great [documentation](http://geopandas.org/projections.html) about projections and coordinate reference systems.

Some properties of two very common CRS:

* WGS84 ([EPSG: 4326](https://epsg.io/4326))
    * Amersfoort at (52.1561110, 5.3878270)
    * In degrees
    * ~ 70 km/degree longitude (horizontal)
    * ~ 110 km/degree latitude (vertical)
* RD New Amersfoort ([EPSG: 28992](https://epsg.io/28992))
    * Amersfoort at (142892.19, 470783.87)
    * In meters
