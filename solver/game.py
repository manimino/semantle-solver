
class SemantleGame():
    def __init__(self, w_vecs):
        w_list = list(w_vecs.keys())
        self.target_word = random.choice(w_list[1000:10000])
        self.target_vec = w_vecs[self.target_word]
        
    def guess(self, word, vec) -> Tuple[bool, float]:
        # construct guess
        # dist = euclidean(vec, self.target_vec) lol nope!
        sim_score = 1-cos_dist(vec, self.target_vec)
        dist = score_to_dist(sim_score)
        # check if win
        if word == self.target_word:
            return True, dist
        else:
            return False, dist
    
    def display_guesses(self):
        s = []
        for g in sorted(self.guesses, key = lambda g: g.dist):
            s.append(str(g))
        print('\n'.join(s))
        
    def __str__(self):
        return '\n'.join('{}: {}'.format(k, v) for k, v in self.__dict__.items())




@dataclasses.dataclass
class Guess:
    word: str
    num: int
    dist: float
    
    
@dataclasses.dataclass
class SolverParams:
    conf_thresh: float


class SemantleSolver:
    
    def __init__(self, n_random_guesses=2, game=None, conf_thresh=0.1):
        self.n_random_guesses = n_random_guesses
        self.closest_dist = float('inf')
        self.guesses = []  # List[Guess]
        self.guessed_words = set()  # for fast lookup
        self.best_guess = None
        self.game = game
        
        self.N_RANDOM = 5
        self.CONF_THRESH = conf_thresh
        
        self.stats = {
            'grd_high_conf': 0,
            'grd_random_dist': 0,
            'times_gradient': 0,
            'times_exhaustive': 0,
            'times_random': 0,
        }
        
    def _gradient_method(self, w_vecs, ann_index):
        # Use gradient method to get a closer guess.
        p1 = np.array(w_vecs[self.guesses[-1].word])
        p1_dist = self.guesses[-1].dist
        
        # Consider the few most recent points. 
        # Try and find one with a vector through p1 that points towards the target.
        best_point = None
        best_confidence = 0
        best_p2_dist = float('inf')
        for i in range(2, min(10, len(self.guesses))):
            p2 = np.array(w_vecs[self.guesses[-i].word])
            p2_dist = self.guesses[-i].dist
            
            # where does p2->p1 point? and how well aligned is that spot with the target?
            target_point, confidence = directed_point_in_dist(p1, p2, p1_dist, p2_dist)
            if confidence > best_confidence:
                best_confidence = confidence
                best_point = target_point
        if best_confidence < self.CONF_THRESH:
            self.stats['grd_random_dist'] += 1
            vec = np.array(w_vecs[self.best_guess])
            best_point = random_point_in_dist(vec, self.closest_dist)
            print('grd_rand')
        else:
            self.stats['grd_high_conf'] += 1
            print('grd_conf')

        return best_point

    
    def find_next_guess(self, w_vecs, ann_index, idx_to_word) -> bool:
        if len(self.guesses) < self.N_RANDOM:
            self.stats['times_random'] += 1
            next_word = random.choice(list(w_vecs.keys()))
        else:
            self.stats['times_gradient'] += 1
            v = self._gradient_method(w_vecs, ann_index)
            idxs_near_best = ann_index.get_nns_by_vector(v, 1000)
            for idx in idxs_near_best:
                w = idx_to_word[idx]
                if w not in self.guessed_words:
                    next_word = w
                    break
            
        return next_word

    def make_guess(self, word):
        # guess the word
        win, dist = self.game.guess(word, w_vecs[word])
        self.guessed_words.add(word)
        self.guesses.append(Guess(word=word, dist=dist, num=len(self.guesses)+1))
        
        # see if this one's better
        if self.best_guess is None or dist < self.closest_dist:
            #print(word, round(dist, 3))
            self.closest_dist = dist
            self.best_guess = word
        
        if win:
            #print("I win!")
            return True
        else:
            return False
    
    def add_guess(self, word, score):
        # Adds a guess from an external source. For playing Real Semantle.
        dist = score_to_dist(score)
        self.guessed_words.add(word)
        self.guesses.append(Guess(word=word, dist=dist, num=len(self.guesses)+1))
        if self.best_guess is None or dist < self.closest_dist:
            #print(word, round(dist, 3))
            self.closest_dist = dist
            self.best_guess = word
        