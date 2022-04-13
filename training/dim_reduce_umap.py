import umap


def make_apply_umap(mat_full: np.array, n_dims=10) -> np.array:
    fit = umap.UMAP(n_neighbors=5,
                    min_dist=0.1,
                    n_components=n_dims,
                    metric='euclidean')
    mat_reduced = fit.fit_transform(data)
    return mat_reduced
