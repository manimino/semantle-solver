### Semantle solver

[Semantle](https://semantle.novalis.org/) is a guess-the-word game. Any word is a valid solution. The only feedback
you get from guesses is the semantic distance from your guess to the solution.

A human will typically need 100+ guesses to solve a Semantle puzzle. Most people just give up entirely. Let's see
if a computer can beat it.

At time of writing, there do not seem to be any existing Semantle solvers. What fun!

### Dataset

To start, we need vectors for every word. Those vectors must be context-independent: 1 word gets 1 vector, without
taking into account any context. This means we'll have the same vector for `pen`, whether it's a pig pen or a writing 
pen.

GLoVe is one source for such vectors. And there precomputed vectors
[available for download](https://nlp.stanford.edu/projects/glove/). Here we will use the "400K vocab (6B)" 
50-dimensional dataset.

### Brainstorming

We need some way of traversing that dataset to approach and find the solution word efficiently.

#### Ideas

- (1) **Brute Force** - guess all 400K words.
- (2) **ANNealing** - Put all the words into an approximate nearest neighbor structure, such as [annoy](https://github.com/spotify/annoy).
Guess randomly until we find a low-distance word, then guess words that are close to that word. An annealing
approach would work here; start with large-distance random jumps, then decrease to smaller distances
as we get closer.
- (3) **Graph Search** - Find pairwise distances between all words. Build a connected graph from the pairwise distances. 
Perform a beam search or monte carlo search to traverse the graph.
- (4) **Low-d Triangulation** - Reduce the GLoVe vectors to a low-dimensional space. Compute the approximate position of the solution based on a 
triangulation all previous guesses (e.g. minimize squared error). Pick the word closest to that postion using
a nearest-neighbor search (k-d tree or ball-tree can be used). 

#### Evaluation

- (1) Well, it would distribute well. Never underestimate brute force - with enough computers, anything can work. And
we have a lot of cheap computers because cloud. Brute force might be of use if we could first eliminate most of the
solution space with another method.
- (2) Really easy to write. Worth a shot. But it might get close to the solution and never reach it.
- (3) This is guaranteed to reach the solution, but traversal could be fairly slow. 
- (4) This would visualize really well. But it may not find the solution if the low-d space loses too much information.

A combination of these ideas might be the strongest, e.g. use one strategy for early guesses and another for late
guesses. Brute Force and Graph Search look like short-range "putters"; ANNealing and Low-d Triangulation look like
long-range "irons".

### Algorithm Implementation - Graph search

#### Data structure

Each node in the graph will contain the word and its vector. The tricky bit is the edges. 

Computing all pairwise distances to build the graph looks heavy - 400K vectors ^ 2 = 80B distance, but is viable on a 
GPU. Based on this [helpful benchmark](https://github.com/ekvall93/distanceMatrixGPU), we can expect it to take about an hour 
on a modern GPU.

But, we want each node to have a useful number of neighbors, and we want the graph to stay at least 1-connected. 
We can start with the fully-connected "all pairwise distances" graph and compute a spanning tree. Then remove
any edges above some distance threshold that are not in the spanning tree.


#### Traversal

The solver will start at some node and guess a few of its neighbor nodes to find one that has a shorter distance to
the target than the current one. That gives information about the direction of the solution, which we can use to 
better select guesses on future nodes. A gradient, actually. 

The search will backtrack if we get to a dead-end node or a node whose neighbors have all been guessed already.
