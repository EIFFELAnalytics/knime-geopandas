"""A Python workflow script to simulate KNIME.

Each cell would represent a node in KNIME. Each cell imports a specific module
(py files) and has a specific functionality.

"""


#%%
# Example: Read shapefile
from os.path import join
from py.read_shapefile import read_shapefile

FOLDER = r'C:/Users/abos/Documents/Open-data/shapefiles/shp-provincie'
FILENAME = r'provincie-grenzen.shp'

df_provincie = read_shapefile(join(FOLDER, FILENAME))


#%%
# Example: Inspect shape
from py.inspect_shape import inspect_shape
_ = inspect_shape(df_provincie, column='id')


#%%
#Example: Reduce precision
from py.reduce_precision import reduce_precision
df_reduced = reduce_precision(df_provincie, 5)
_ = inspect_shape(df_reduced)


#%%
# Example: Simplify
from py.simplify import simplify
df_simple = simplify(df_provincie, 5)
_ = inspect_shape(df_simple)


#%%
# Example: Centroid
from py.centroid import centroid
df_centroids = centroid(df_provincie)
_ = inspect_shape(df_centroids)


#%%
# Example: Dissolve provincies naar regio's
df_provincie['Regio'] = ['Noord', 'Noord', 'Noord', 'Zuid', 'Noord',
    'Noord', 'Noord', 'Midden', 'Midden', 'Zuid', 'Midden', 'Zuid']
from py.dissolve import dissolve
df_regio = dissolve(df_provincie, by='Regio', as_index=False)
_ = inspect_shape(df_regio, column='Regio')


#%%
# Example: Isochrones
from py.isochrone import isochrone
df_isochrones = isochrone(df_centroids, driving_time=10)
_ = inspect_shape(df_isochrones)


#%%
# Example: Gebruik spatial join om alle gemeenten te filteren die in de
# provincies Noord- en Zuid-Holland liggen.
FOLDER = r'C:/Users/abos/Documents/Open-data/shapefiles/shp-gemeente'
FILENAME = r'gemeente-grenzen.shp'
df_gemeente = read_shapefile(join(FOLDER, FILENAME))
_ = inspect_shape(df_gemeente)

# Selecteer provincie Noord- en Zuid-Holland
df_holland = df_provincie[df_provincie.provincien.str.endswith('Holland')]
_ = inspect_shape(df_holland, column='provincien')

# Inner join alle gemeenten met de 2 provincies
# Bij een inner of een left join, neemt het resulterende dataframe de geometry
# van de left dataframe over
from py.spatial_join import spatial_join
df_gemeenten_holland = spatial_join(df_gemeente, df_holland, how='inner', op='intersects')
_ = inspect_shape(df_gemeenten_holland, column='provincien')


#%%
# Example: Duration matrix
from py.distance_matrix import distance_matrix

df_origins = df_centroids[0:3]
display(df_origins)
df_destinations = df_centroids[3:5]
display(df_destinations)

matrix = distance_matrix(df_origins, df_destinations)

# The returned index and column headers are the snapped coordinates. Let's set
# them to something meaningful.
matrix.index = df_origins.provincien
matrix.index.name = 'origin'
matrix.columns = df_destinations.provincien
matrix.columns.name = 'destination'

# I just hate matrices. Unpivot the all columns to 1 destination column.
import pandas as pd
matrix = pd.melt(matrix.reset_index(), id_vars=['origin'], value_name='travel_time')
matrix


#%%
