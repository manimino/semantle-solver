from numbaDistanceMatrix.cudaDistanceMatrix import DistanceMatrix
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
n = 200
X = np.random.rand(n, n).astype(np.float32)

DM = DistanceMatrix()
DM.calculate_distmatrix(X)

DM.get_similarity(10,2)
#0.77965623
cosine_similarity(X)[10,2]
#0.77965623

SKlearn_under = cosine_similarity(X)[np.tril_indices(n, k=-1)]
under_dist = DM.get_distance_matrix(fullMatrix=False)
np.allclose(np.sort(under_dist), np.sort(SKlearn_under))
#True

SKlearn_full = cosine_similarity(X)
DM_full = DM.get_distance_matrix(fullMatrix=True)
np.allclose(SKlearn_full, DM_full)
#True
