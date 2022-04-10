def directed_point_in_dist(p1: np.array, p2: np.array, 
    p1_dist: float, p2_dist: float) -> Tuple[np.array, float]:
    """
    Input: two points, and their distances from the solution.

    Make a vector between the two points. The vector is directed towards
    the point that is closer to the solution.
    Return a target point that continues the vector from the nearer point towards
    the solution. Its distance is simply the nearer point's distance from the solution. 

    Does the vector point directly at the solution? If so, its magnitude
    will be equal to abs(p1_dist - p2_dist). The further it deviates from that,
    the worse of a vector this is. So we also return a "confidence" score based 
    on that ratio.

    See test cases for example scenarios.
    """
    # Generate a vector using p1 and p2.
    # Check if it will point in the general direction of our target.
    p1p2 = (p1-p2)
    p1p2mag = scipy.linalg.norm(p1p2)
    if p1p2mag < 0.00001:
        return None, 0
    p1p2_unit = p1p2 / p1p2mag
    if p1_dist < p2_dist:
        # p1 is closer to target
        mag = p1_dist
        target_point = p1 + p1p2_unit*mag
        confidence = (p2_dist-p1_dist) / p1p2mag
        assert confidence >= 0
    else:
        # p2 is closer to target
        # make a vector from p2 to a target that is p2_dist away
        mag = p2_dist
        target_point = p2 - p1p2_unit*mag
        confidence = (p1_dist-p2_dist) / p1p2mag
        assert confidence >= 0
    return target_point, confidence


def random_point_in_dist(point: np.array, dist: float) -> np.array:
    """
    If we cannot find a high-confidence direction to travel, we'll just make a random
    vector and hope it gives us some new information we can use later.
    If we're REALLY lucky, it will land right on the solution.
    """
    vec = np.random.random((len(point)))
    vec = vec / scipy.linalg.norm(vec)
    vec = vec * dist
    return vec+point


def score_to_dist(score: float) -> float:
    """
    Given a Semantle score (float -100 to 100), convert it into a Euclidean
    distance in our reduced space. The coefficients were computed
    from a polynomial fit; see training/dim_reduce.py for details.
    """
    sim_score = score / 100
    coef = [-0.93024736,  0.28175783, -0.73464682,  1.12342693]  # 100 dims
    return coef[0]*sim_score**3 + coef[1]*sim_score**2 + coef[2]*sim_score + coef[3]


def point_to_word(point: np.array, idx: AnnoyIndex, used_words: Set[str], n=10):
    """

    """
    

    # if we can't find a new word in the top n (unusual!), retry with the top n*10
    return point_to_word(point, )