# Semantle Solver

Implements a vector search that can solve [Semantle](https://semantle.novalis.org/) and related mathematical problems.

This solver has the same primary constraint a human player does: it only has information about the words it has guessed so far. So it cannot use [the triangulation method](https://www.github.com/manimino/semantle-crab). 

However, it is also able to use a point in space as a guess. The word nearest to the guessed point is considered to be the word that is guessed.

It wins in ~100 guesses, roughly human-level performance. See an [example game](docs/game.md).

This is currently a proof-of-concept, code is in `notebooks/`.

## Algorithm (high-level)

### Intuition

Here's a 1-dimensional Semantle problem. 

Imagine if we had three words: "**B**all", "**M**oon", and "**P**lanet", and they were all on a number line like so:

```
B           M     P
+--+--+--+--+--+--+
0  1  2  3  4  5  6
```
Ball is at 0, Moon is at 4, and Planet - the solution - is at 6.

Initially we guess Ball. Semantle tells us the distance to the solution, 6 units.

Next we guess Moon. Semantle tells us the solution is 2 units away. 

We now have the information that leads us to the solution:
- **Magnitude:** We know Moon is exactly 2 units away from the solution. 
- **Direction:** When we traveled 4 units from Ball to Moon, we get closer to the solution by `(6-2) = 4` units. So we should keep going that way (+ on the number line).

```
B           M --> P
+--+--+--+--+--+--+
0  1  2  3  4  5  6
```

With a starting point at Moon, a magnitude of 2, and a direction (positive on the number line), we can travel straight to Planet. Our next guess is the word at position 6, which is the solution.

Each new point adds significant information about where the target is.

## Implementation

### Setup steps:
1. Reduce dimensionality using PCA.
1. Build an LSH index using [annoy](https://github.com/spotify/annoy). This will give us the word closest to any point in space.
1. Guess two random words.

### Iteration steps:
1. Compare each pair of previously-guessed words. 
1. Determine the point along that vector that is nearest to the target (projection)
1. Move orthogonally (in a randomly chosen dimension) from that point to a new guess-point.
1. Look up the word at that point using the LSH index. Guess the word.

## Future work

Right now we only work with triangles, which are built using two guessed points plus their distances to the target. 

Comparing larger numbers of points could improve performance. For example, in 3-D, we could have a tetrahedron and project the target onto that plane. And so on to larger simplices. 