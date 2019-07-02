"""Example code to show how to geocode some queries (such as postal codes)
and requests the travel times between them.

"""

#%%
# Geocode
# Note: You'll need an API key from https://openrouteservice.org/sign-up/.
import pandas as pd
from py.geocode import geocode
try:
    from credentials import api_key
except:
    # Manually set your API key if not found in credentials.py
    api_key = ''

# Geocode een aantal PC4 gebieden in Arnhem
input_table_1 = pd.DataFrame({'query': ['3811', '5222', '6661', '6666', '6681', '6811']})
output_table_1 = geocode(input_table_1, api_key)
display(output_table_1)

# Geocode EIFFEL Arnhem
input_table_2 = pd.DataFrame({'query': ['EIFFEL Arnhem']})
output_table_2 = geocode(input_table_2, api_key)
display(output_table_2)


#%%
# Request duration matrix
# This reads the `wkt` column from the dataframes
from py.distance_matrix import distance_matrix
matrix = distance_matrix(output_table_1, output_table_2)
display(matrix)

# The returned index and column headers are the snapped coordinates. Let's set
# them to something meaningful.
matrix.index = df_origins['query']
matrix.index.name = 'origin'
matrix.columns = df_destinations['query']
matrix.columns.name = 'destination'

# I just hate matrices. Unpivot the all columns to 1 destination column.
import pandas as pd
matrix = pd.melt(matrix.reset_index(), id_vars=['origin'], value_name='travel_time')

# Travel times are preferred in minutes
import numpy as np
matrix.travel_time = np.round(matrix.travel_time / 60)
display(matrix)


#%%
