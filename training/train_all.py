from training.read_vectors import fetch_goog_file, read_goog_file
from training.dim_reduce import do_pca, write_test_data, fit_distances

def train():
    fetch_goog_file()
    mat_full = read_goog_file()
    mat, word_to_idx = do_pca(mat_full)
    write_test_data(mat, word_to_idx)
    fit_distances(mat_full, mat)

if __name__ == '__main__':
    train()