"""
Computes an iterative PCA on all them vectors. 
Gotta be iterative or it will take >16GB of RAM at peak, which will OOM on many systems.
TODO: Do we actually need to do this? What about just living with 300 dims?
"""


def make_apply_pca(mat_full: np.array, n_dims: int):
    """
    
    """
    pass



def write_test_data(mat: np.array, word_to_idx: Dict[str, int]):
    """
    Writes out a small subset of the word vectors to a file.
    This subset contains many common English words that are useful for testing.
    """
