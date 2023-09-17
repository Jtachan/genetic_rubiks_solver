# Genetic Algorithms

Genetic algorithms (GA) are stochastic global optimization algorithms.
Just like many other topics in AI, this is based on living biology, in specific in the [theory of evolution](https://en.wikipedia.org/wiki/Evolution).

## Terminology

When describing a GA, there is some terminology to be aware of:

- **Generation**: It refers to the whole population contained in an iteration stage of the algorithm. Each population is defined by multiple candidates, and each generation shares the same length of population. Each generation is identified by a number, which refers to the number of iterations since the start of the algorithm.
- **Genes** or **solution**: Defined by the elements that compose one candidate. For example, if each candidate is defined by the RGB colors with `1` as 'use the color' and `0` as 'don't use the color', two possible candidates are `010` and `110`. These sequences of choices are the genes of each candidate.
- **Parent/Child**: A parent is a candidate from the previous generation which was selected. Two parents define a new child for the next generation. The child contains genes from both parents through crossover functions.

## Crossover functions

The [Crossover](https://en.wikipedia.org/wiki/Crossover_(genetic_algorithm)) function allows defining two new children with the genes from the parents.
To do so, each parent splits its genes into groups. 
Then, the same group is changed among the candidates considering the children must have the same number of genes as the parents.

For example, the following are the parents of a new generation:

    parent_1 = 000000
    parent_2 = 111111

By splitting the genes into groups and changing them, the following are the two children obtained:

    child_1 = 00011
    child_2 = 11100

In this example, children's genes were calculated by the **single-point crossover**, where the genes were split only once.
However, it is also possible to use the **k-point crossover** to split genes 'k' times and cross them.
The groups then can be distributed uniformly or with random splits.

## Basic theory of genetic algorithms

The whole point of GA is to find the optimal solutions of very complicated problems, finding the best candidate among generations obtained with the theory of evolution.
When a problem is set for the algorithm, the GA works over the next stages:

1. **Creation of first generation**: Generation 0 is created with a fix number of candidates. Because there is no possibility of these candidates to be children of any previous generation, each one is defined with a random sequence of genes.
2. **Natural selection**: Each candidate is processed by a `fitness()` function to define how good it is (low error to our desired solution). The `fitness()` function differs for each problem and/or strategy. It's key to identify the best candidate of a generation does not mean the best solution for the problem. No candidate is killed in this process.
3. **Reproduction**: Pairs of candidates reproduce to generate a new generation. A pair of candidates with a good fitness score is more likely to reproduce than two with a poorly fitness score. The new generation is created through the established crossover function.
4. **Elitism**: This is an optional step, in which the best candidates of the previous generation are included within the new generation. Because the reproduction and the crossover are defined by a random factor, elitism is usually included to avoid destroying the best solutions of a generation.
5. **Mutation**: For each candidate of the new generation, a number of genes suffers a mutation, changing its value to a different possible generating a new solution. The same number of genes is mutated at each candidate, but not strictly the same genes are mutated.
6. **Iterate**: Steps 2-6 are processed over and over until the fitness converges into the desired solution.
