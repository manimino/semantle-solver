"""
Run a few quick checks on our low-d embedding to make sure
that word distance still lines up with intuitive meaning.
"""

import os
import pickle


THIS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.abspath(os.path.join(THIS_FILE_DIR, '../models'))
TEST_DATA_FILE = os.path.join(MODELS_DIR, 'test_vecs.pkl')

def load_test_data():
    with open(TEST_DATA_FILE, 'rb') as fh:
        return pickle.load(fh)


def test_low_d_intuitive_strawberry():
    w_vecs = load_test_data()
    s_p = euclidean(w_vecs['strawberry'], w_vecs['peach'])
    s_b = euclidean(w_vecs['strawberry'], w_vecs['banana'])
    s_e = euclidean(w_vecs['strawberry'], w_vecs['envelope'])
    assert s_p < s_e and s_b < s_e


def test_low_d_intuitive_pets():
    w_vecs = load_test_data()
    c_d = euclidean(w_vecs['cat'], w_vecs['dog'])
    c_r = euclidean(w_vecs['cat'], w_vecs['rock'])
    assert c_d < c_r


def test_low_d_intuitive_weather():
    w_vecs = load_test_data()
    r_c = euclidean(w_vecs['rainy'], w_vecs['cloudy'])
    r_p = euclidean(w_vecs['rainy'], w_vecs['porcupine'])
    assert r_c < r_p