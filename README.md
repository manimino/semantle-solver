# Semantle Solver

[Semantle](https://semantle.novalis.org/) is a word game about finding a secret word. After each guess, the player gets a score based on how close their guess is to the secret word. 

This project poses Semantle as a high-dimensional spatial search problem, and solves it.

The solver roughly matches human performance on Semantle puzzles with common words. And it generalizes to puzzles that humans would not be able to solve.

[Here is the solver's output on an actual Semantle game.](docs/semantle-button.png)

See a [demo here.](www.manimino.com/semantle-solver)

### Computational challenges

Usually in a search space, you know **direction** but not **distance**, e.g. with gradient descent.
But in Semantle, each guess gives you only distance. You have to figure out direction.

Furthermore, it's discrete. You must guess a word, not a point in space. So you can't step a little in each direction to find your gradient.

Semantle uses a corpus of 3 million words. Exhaustive searches and low-dimensional representations will not work.

Last, the score isn't Euclidean. Semantle scores reflect cosine distance in a 300-dimensional space. That's a pretty cursed signal!

### Solver description

To generate a guess, the solver compares pairs of previous guesses. If one guess is closer than the other, we know the solution is in that (general) direction. For example, if the guess 'ball' is close and 'moon' is much closer, 'planet' is a good next guess! 

The word-vector math doesn't produce 'planet' directly; it just gives a point in the search space. To convert that point to a word, the solver uses [annoy](https://github.com/spotify/annoy), an approximate nearest-neighbor index based on locality-sensitive hashing. 

It's easy to get lost in high-dimensional spaces, so the solver uses dimensionality reduction as a preprocessing step. Cosine similarities in the original space are mapped to Euclidean distances in the reduced space via [curve fitting](). To perform the reduction, PCA and [UMAP](https://umap-learn.readthedocs.io/en/latest/) are both viable; the solver currently uses PCA.

### Implementation / Progress



### Range query

Ahh, yes. There's also the cheaty quick way to win Semantle.

1. Guess the word 'cheat'
1. Run `python cheat.py [score]` where `[score]` is the Semantle score for 'cheat'.
1. You get a list of words back.
1. Type one of those in and win.

If you precalculate the distance from 'cheat' to every Semantle word and make a lookup table, you can run a range query on that. It will usually win on move 2.