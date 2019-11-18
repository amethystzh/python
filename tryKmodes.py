import numpy as np
import pandas as pd
from kmodes.kmodes import KModes

# random categorical data
# data = np.random.choice(20, (100, 10))
# print(data)
# print("\n")
#
# km = KModes(n_clusters=4, init='Huang', n_init=5, verbose=1)
#
# clusters = km.fit_predict(data)
#
# # Print the cluster centroids
# print(km.cluster_centroids_)

filename = "tz.xls"

data = pd.read_excel(filename)

km = KModes(n_clusters=6, init='Cao', n_init=8, verbose=1)

clusters = km.fit_predict(data)

# Print the cluster centroids

print(km.cluster_centroids_)
