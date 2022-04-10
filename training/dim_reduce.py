"""
Computes an iterative PCA on all them vectors. 
Gotta be iterative or it will take >16GB of RAM at peak, which will OOM on many systems.
TODO: Do we actually need to do this? What about just living with 300 dims?
"""

def make_apply_pca(mat_full: np.array, n_dims: int):
    pass

