"""A Python workflow script to simulate KNIME.

Note about importing the other modules:
Run this script through VS Code with the project folder open. This sets sys.path
to the pwd and lets you import modules from `py`.

See https://chrisyeh96.github.io/2017/08/08/definitive-guide-python-imports.html
for more information about imports.

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
inspect_shape(df_provincie, column='id');


#%%
#Example: Reduce precision
from py.reduce_precision import reduce_precision
df_reduced = reduce_precision(df_provincie, 5)
inspect_shape(df_reduced);


#%%
# TODO
from py.simplify import simplafy
df = simplafy(df, 0.001)


#%%
# Example: Middelpunt bepaling
from py.centroid import centroid
df_provincie_centroids = centroid(df_provincie)
inspect_shape(df_provincie_centroids);


#%%
# Example: Dissolve provincies naar regio's
df_provincie['Regio'] = ['Noord', 'Noord', 'Noord', 'Zuid', 'Noord',
    'Noord', 'Noord', 'Midden', 'Midden', 'Zuid', 'Midden', 'Zuid']
from py.dissolve import dissolve
df_regio = dissolve(df_provincie, by='Regio', as_index=False)
inspect_shape(df_regio, column='Regio');


#%%
# TODO
from py.isochrone import isochrone
df = isochrone(df_centroids, 10)


#%%
# Example: Gebruik spatial join om alle gemeenten te filteren die in de
# provincies Noord- en Zuid-Holland liggen.
FOLDER = r'C:/Users/abos/Documents/Open-data/shapefiles/shp-gemeente'
FILENAME = r'gemeente-grenzen.shp'
df_gemeente = read_shapefile(join(FOLDER, FILENAME))
inspect_shape(df_gemeente);

# Selecteer provincie Noord- en Zuid-Holland
df_holland = df_provincie[df_provincie.provincien.str.endswith('Holland')]
inspect_shape(df_holland, column='provincien');

# Inner join alle gemeenten met de 2 provincies
# Bij een inner of een left join, neemt het resulterende dataframe de geometrie
# van de left dataframe over
from py.spatial_join import spatial_join
df_gemeenten_holland = spatial_join(df_gemeente, df_holland, how='inner', op='intersects')
inspect_shape(df_gemeenten_holland, column='provincien');

