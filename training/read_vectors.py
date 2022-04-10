def download_goog_file():
    # fetch and unzip the 1.4GB -> 3.4GB file of Google News word vectors
    pass


def read_goog_file(size=None):
    vec_file = '/mnt/Spookley/datasets/semantle/GoogleNews-vectors-negative300.bin'
    kv = models.KeyedVectors.load_word2vec_format(vec_file, binary=True, limit=size)
    words = kv.index_to_key
    w_vecs = {}
    for w in words:
        w_vecs[w] = kv[w] / np.linalg.norm(kv[w])
    return w_vecs

# usage
w_vecs = read_goog_file(size=1000000)
w_list = list(w_vecs.keys())