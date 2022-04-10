# Semantle Solver

[Semantle](https://semantle.novalis.org/) is a word game about finding a secret word. After each guess, the player gets a score based on how close their guess is to the secret word. 

The secret word could be anything, so the game is quite difficult. Let's see if a computer can do it!

## Demo / Running / Results

[Here is the solver's output on an actual Semantle game.]()

See the [demo in a webpage here.](www.manimino.com/semantle-solver)

To run the code yourself, clone the repo, do `docker build -t semantle-solver .` and `docker run semantle-solver`. The build will download a 3.4GB file of word vectors.

## How the solver works

It involves dimensionality reduction, vector arithmetic, and locality-sensitive hashing. [Long explanation here.](algorithm.md)

## These are not how the solver works

### Cheat method 1

If you look at the JavaScript source code on the Semantle website, you will find a list of words, one for each day. You could look up the word for today and solve it in one guess. 

### Cheat method 2

Pick a word, let's say `rock`. Precompute the cosine distance from `rock` to every other word in the Semantle dataset. Open Semantle, guess `rock`, get the score. Then look in your distance table to find a word with exactly that score's distance from `rock`. Probably there is only one such word. You win in two (or very few) guesses!
