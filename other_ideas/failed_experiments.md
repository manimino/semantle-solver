### LSH alone

Idea: randomly guess words. When you get to some "close" word, guess all its nearest neighbors until you find a closer one.
Repeat on the closest word till you find the target.

This didn't work at all. Getting even slightly close in a 400K-word space took 1000+ guesses. And even that wasn't close enough for the naive traversal to get in range. It would get lost in "pocket dimensions" of densely packed wrong answers.

Without backtracking search, this won't even terminate without a truly silly number of guesses. 

It's not just bad, it's terrible. Almost as bad as totally random guessing. 


### Uncased GLoVE embeddings

Still, LSH nearest-neighbors does tell us some interesting stuff.

The nearest neighbors of "apple" in uncased GLoVe space are:

`['apple', 'blackberry', 'pc', 'iphone', 'chips', 'ipod', 'dell', 'sells', 'amd', 'cisco', 'microsoft', 'ibm', 'macintosh', 'app', 'hewlett', 'brand', 'micro', 'netscape', 'packard', 'android']`

So now we know:
 - Cased embeddings will give more intuitive results. Let's switch to those.
 - GLoVE cares about whatever the Internet thinks is important, so fruit is less important than computers.
 - `netscape` etc being on there indicates that GLoVE is based on a pretty dated corpus.

### LSH + distance based methods

OK, what if we use the distance signal somehow? Like, as a gradient? You got two points, one of them's closer to the target than the other. Keep going in that direction and guess something over there!

Unfortunately:
 - Distance is a miserable signal in a 50-dimensional space. In 2D, a distance tells you that your target must be on the perimeter of a circle around your point; with more points, you can narrow that down. In 50D, a distance describes some awful hypersphere. You need a ton of points to narrow it down.
 - Getting a real gradient is hard, since these are discrete points. You can't just guess any point in space you want, it has to be a real word. 
 - We hope that the GLoVe embedding corresponds to real Semantle space somehow... but we don't really know. Gradients in Semantle-space may not help much in GLoVe-space.

 So... yeah. Not much we can do with the distance signal. We can use it as a "warmer / colder", that's about it.

### DBSCAN

So we've got pocket-dimensions with lots of points in 'em. Density based clustering should tease those out, right?

Unfortunately, word clustering is kinda rough. A lot of words are really similar to `"the"`. Very few words are similar to `"baozi"` (for corpus reasons). 

That means you get one cluster with half of your words, and a million with three words each. Can't build a good search tree on such an imbalanced setup.


### T-SNE

Let's cram it into a 2D space!

So, runtime isn't too bad, this could work for 400k words if we're patient.

| words | secs |
|-------|------|
| 2000  | 2    |
| 10000 | 14   |
| 20000 | 31   |
| 50000 | 110  |
 
 Unfortunately, the results are trash.

In the original space:
```
euclidean(strawberry, peach) = 3.408
euclidean(strawberry, banana) = 4.489
euclidean(strawberry, envelope) = 5.775
```

In T-SNE space:
```
euclidean(strawberry, peach) = 0.8519
euclidean(strawberry, banana) = 7.247  # <--- what?!
euclidean(strawberry, envelope) = 4.120
```

It preserves the very close neighbors well, but anything beyond that is not useful. Not really T-SNE's fault; 2D is way too small of a space to embed words for what we want.

T-SNE can go up to 3D, but that fared no better on the strawberry-banana-envelope test.

It can't go higher than 3D because quadtree / octree is part of the implementation.

### What about like... 5D? 

OK, did a PCA and reduced the dims down. Gradient search starts working really well at 10 and below.

Elbow in explained variance is at 10-D.

Intuitively, the strawberry-peach-envelope test starts passing at 7 dimensions, and gets better as you add more.


### Distance function / embedding problems

Cosine similarity is used by Semantle, but our algorithm's based on Euclidean.

Low-D representations are great for our algorithm, but unfortunately destroy the "cosine dist" -> "euclidean dist" relationship between the original space and the dim-reduced space.

Presently we do two things:

- Normalize the vectors before PCA. Cosine similarity cannot use vector magnitudes, only directions. If we use the original vector's magnitudes as input to the PCA, the resulting spatial relationships are much further from the cosine-dist based original relationships.

- Use a high-D PCA. For the 50-D GLoVe vectors, we can go down to 20D. For the 300-D Google vectors, we need more like 100-D. That's a huge space, unfortunately, and the performance suffers for it. 

TODO: Find a better spatial-embedding algorithm that preserves distance. Probably a kind of constrained autoencoder that takes in two vectors at once and has a loss function that guarantees the latent vectors have a Euclidean distance similar to the Cosine distance of the original vectors.
