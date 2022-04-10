"""
Computes an iterative PCA on all them vectors
todo: Do we actually need to do this? What about just living with 300 dims?
"""

def score_to_dist(score):
    sim_score = score / 100
    coef = [-0.93024736,  0.28175783, -0.73464682,  1.12342693]  # 100 dims lets goooooo
    #coef = [-0.17479252, -0.29550786, -0.50620742,  0.90186038] # goog 1M @ 40 dims, works okay (1k guesses)
    # coef = [0.04471114, 0.0740919, -0.74640201, 0.95066707] # glove dataset
    return coef[0]*sim_score**3 + coef[1]*sim_score**2 + coef[2]*sim_score + coef[3]