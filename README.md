# Semantle Solver

Solves [Semantle](https://semantle.novalis.org/).

This solver has the same primary constraint a human player does: it only has information about the words it has guessed so far. So it cannot use [the triangulation method](https://www.github.com/manimino/semantle-crab). 

It usually wins in under 100 guesses, roughly human-level performance. See an [example game](docs/game.md).

It also generalizes to other vector spaces (e.g. GLoVe embeddings).

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
- **Direction:** When we travel 4 units from Ball to Moon, we get closer to the solution by `(6-2) = 4` units. So we should keep going that way (+ on the number line).

```
B           M --> P
+--+--+--+--+--+--+
0  1  2  3  4  5  6
```

With a starting point at Moon, a magnitude of 2, and a direction (positive on the number line), we can travel straight to Planet. Our next guess is the word at position 6, which is the solution.

This idea works in higher-dimensional spaces, albeit with some extra steps. It is a distant cousin of gradient descent.

### Setup steps:
1. Reduce dimensionality using PCA.
1. Build an LSH index using [annoy](https://github.com/spotify/annoy). This will give us the word closest to any point in space.
1. Guess two random words.

### Iteration steps:
1. Compare each pair of previously-guessed words. 
1. If the vector between them points towards the target, continue that vector towards the target.
1. Look up the word at that point in the LSH index. Guess the word.
