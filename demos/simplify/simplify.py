#%%
from shapely.geometry import Polygon
p = Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])
x, y = p.exterior.xy

import matplotlib.pyplot as plt
plt.plot(x, y)

#%%
import numpy as np 
xi = np.linspace(1, 0, num=10)

from random import uniform
yi = [uniform(0.95, 1.05) for i in range(len(xi))]


#%%
list(zip(xi, yi))

po = [(0, 0), (1, 0), (1, 1)] + list(zip(xi, yi)) + [(0, 1)]
po = Polygon(po)
x, y = po.exterior.xy

#%%
plt.plot(x, y)

#%%
# Now simplify
