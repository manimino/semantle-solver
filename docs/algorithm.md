# WIP

This file is not complete, but what's here so far is correct.

## How the solver works

We'll explain by solving a simple "toy" Semantle game, and then solve successively harder versions up to the real Semantle. 

But first, let's talk about word vectors.

### Word Vectors

Each word in Semantle is represented by a list of decimal numbers called a vector. They look like:

```
'strawberry': [1.334845, 0.034302, 2.5784931, ...]
'banana': [1.334845, 0.034302, 2.5784931, ...]
```

When you guess a word, Semantle gives you the distance between your word's vector and the secret word's vector. The solver will have to use that distance information to walk through the space of word vectors.

If you've heard of word vectors before, you'll know the famous result: `king - man + woman = queen`. When words are represented as vectors, you can add and subtract them to get intuitive results.

Now on to the show.

### 1D Euclidean Semantle

Imagine if we had three words: "A", "B", "S", and they were all on a number line like so:

```
A           B     S
+--+--+--+--+--+--+
0  1  2  3  4  5  6
```
A is at 0, B is at 4, and S - our secret word - is at 6.

Initially we guess "A". Semantle responds "6", because the secret word "S" is 6 units away.

Next we guess "B". Semantle responds "2", because "B" is 2 units away from S. 

We now know enough to solve the puzzle:
- **Starting point:** We have a point close to S, at B.
- **Magnitude:** We know B is exactly 2 units away from S. 
- **Direction:** When we travel 4 units from A to B, we get closer to the secret word by `(6-2) = 4` units. So we should keep going that way.

With a starting point at B, a magnitude of 2, and a direction (positive on the number line), we can travel straight to S. Our next guess is the word at position 6, which is S.


```
A           B --> S
+--+--+--+--+--+--+
0  1  2  3  4  5  6
```

#### Looking up words by position

Wait, how did we go knowing "position 6" to guessing word S? 

So, we need a data structure that lets us look up words by position. Furthermore, it would be nice if all we needed was *approximate* position. Ideally we could put in a position, and the data structure would tell us all the words near that spot, ranked in order of distance.

There are a few ways to solve that problem. The way we use here is locality-sensitive hashing, specifically the [annoy](https://github.com/spotify/annoy) library. It is easy to use and very fast. Here is an [excellent doc](https://www.pinecone.io/learn/locality-sensitive-hashing/) if you would like to learn more about the algorithm.

### 2D Euclidean Semantle

Now we have a 1-D solver. But word vectors are not 1-dimensional single numbers, they are much bigger. But let's just step up to 2-D first, we'll work out a lot more of the algorithm there.

#### Happy scenario

Let's say we have made 2 guesses, and the secret word is almost collinear to them:


Our next guess will be the word closest to the green X, which turns out to be the secret word. Yay! 


#### Overshoots



#### Many choices



#### Lousy scenario

Let's say we've made 5 guesses. A vector between any 2 of them gets us no closer to the secret word. Based on distance alone, we can't even tell which direction it is - is left or right of our previous guesses? 

In this case, we'll do something random to get more information. We'll take the best point we've found so far, and draw a random vector.

Using a random vector looks a bit silly here, since we could be smarter given the information we have. For example, we could use an RSSI circle-intersection algorithm to triangulate the secret word's position down to one of two spots. But that idea falls apart in higher-D spaces we'll need later. Random's easy, and it works.



### N-D Euclidean Semantle

The 2-D algorithm works great in higher dimensions. As long as the lookback window is long enough, we can find a pair of points that yield a vector pointing (roughly) towards the target word. 

So, adding more dimensions just costs us more guesses. Ideally, we'd work in the lowest-D space that preserves distances between words.

An intuitive way to test "Do I have enough dimensions?" is *strawberry, banana, envelope*.  Find distances between those three words. *Strawberry* and *banana* should be close together, *envelope* should be distant from both. Writing a bank of such tests is a good idea.

From my experiments, you need about 10 dimensions to represent word vectors well. Below that, the strawberries and envelopes start getting mixed up.

Using PCA, we can reduce the vector dimensions down substantially. This means we need fewer guesses on Euclidean Semantle problems. Nice!

### Cosine Distance Semantle

Well, we'd be done here if Semantle gave Euclidean distances as feedback. It doesn't! It gives cosine distances. Specifically, the word score is `100 * (1 - cosine dist (your word, secret word))`, also known as `cosine similarity * 100`.

Luckily, we can map cosine distances to Euclidean distances. A pair of vectors that are adjacent in cosine-space are also adjacent in Euclidean space, as long as you normalize the vectors first. The distances are proportional, so long as your vectors are normalized. We can do that! 

So, our preprocessing steps are:
1. Normalize all the vectors
1. Take the PCA to reduce the space
1. Make a mapping between cosine distance (Semantle word score) and Euclidean distance in our reduced space.

Then we have an N-D Euclidean space and can translate cosine Semantle scores into distances in that space.

### Full algorithm

Setup:
1. Read all 4 million words from the Google News word2vec dataset.
1. Normalize all vectors.
1. Compute a reduced space using PCA.
1. Sample cosine distances between words in the original space, and Euclidean distances between the same words in the new space. Use a polynomial fit to make a mapping between the two spaces. This mapping will convert Semantle guess scores to Euclidean distances in our reduced space.
1. Compute an LSH index on the reduced space. We will use the index for "find words near a given point" queries.

Playing the game:
1. Make a few random guesses.
2. Subtract each of the previous N guesses from the most recent guess. 
   - If that produces a vector that points towards the target: add the vector to the nearer point, and guess the word(s) closest to the result.
   - Otherwise, start from our best guess so far. Draw a vector in a random direction. Find the word(s) at that point.
3. If we've already guessed a word, don't guess it again. Guess the next-closest word to the position we calculated instead.
4. Repeat 2-3 until solved.

Annnd, that's it! That's how we solve Semantle.

### Future Improvements

The dimensionality reduction step is jank. Replace it with a distance-preserving autoencoder. 
