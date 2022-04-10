from solver.vec_math import directed_point_in_dist

def test_directed_math_collinear():
    # test case - target at [0,6], both points on y axis
    p1 = np.array([0,0])
    p2 = np.array([0,2])
    target = np.array([0,6])
    d1 = euclidean(p1, target)
    d2 = euclidean(p2, target)
    print('expect [0,6]', directed_point_in_dist(p1, p2, d1, d2))
    print('expect [0,6]', directed_point_in_dist(p2, p1, d2, d1))


