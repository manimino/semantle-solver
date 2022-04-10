from training.read_vectors import fetch_goog_file, read_goog_file
from training.dim_reduce import 

def train():
    fetch_goog_file()
    mat_full = read_goog_file()


if __name__ == '__main__':
    train()