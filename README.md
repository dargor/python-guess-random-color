# Colors, algorithms and fun

A standard `#RRGGBB` color is a 24-bit number, meaning it has `256^3` = `16777216` possible combinations (!).

I wondered how genetic algorithms worked, and how many iterations would be needed to find a given color.

I thought it was a good choice, because colors are easy to compare, right ?

![I've never been so wrong, in all my life.](wrong.jpg)

## Quick note about terminal emulators

I lost some time wondering why my algorithms sometimes returned me colors that did not match, so I warn you : terminal emulators more or less correctly implement true colors, which are needed in our use case.

You can test your terminal emulator by running `./test_color.py` :
![True colors or not, that is the question.](test_color.png)

If you don't have a nice output, try [st](http://st.suckless.org/) : it's easy to compile and run locally, no need to install it as root !
```bash
wget http://dl.suckless.org/st/st-0.6.tar.gz
tar xzf st-0.6.tar.gz
cd st-0.6/
make
tic -s st.info
./st &
```
And voilà, ready to run with some nice colors !

## run.py

This is the benchmark main entry point.

```
$ ./run.py -h
usage: run.py [-h] -a {random,brute,genetic} [-d DELAY] [-f FITNESS]
              [-i ITERATIONS] [-p POPULATION_SIZE] [-s SEED]

optional arguments:
  -h, --help            show this help message and exit
  -a {random,brute,genetic}, --algorithm {random,brute,genetic}
                        Algorithm to run
  -d DELAY, --delay DELAY
                        Delay between each iteration
  -f FITNESS, --fitness FITNESS
                        ΔE considered acceptable
  -i ITERATIONS, --iterations ITERATIONS
                        Number of iterations
  -p POPULATION_SIZE, --population-size POPULATION_SIZE
                        Size of population at each iteration
  -s SEED, --seed SEED  Seed to initialize the random number generator
```

Play with the various options, but the only really useful one is `-a`.

## But what's a ΔE, my precious ?

It's a measure of distance between two colors, lesser being closer.

The `wikipedia` page and `python-colormath` documentation explain everything :
* https://en.wikipedia.org/wiki/Color_difference
* http://python-colormath.readthedocs.io/en/latest/

ΔE are noted below their corresponding colors in the output of `run.py`.

The `-f` option sets the minimum ΔE value required to pass the test, and default to `1.0`.

## Algo*.py

All our algorithms derive an abstract base class `Algo`, which is used by `run.py` to abstract annoying details.

The base population of all algorithms is randomly chosen.

## AlgoBrute.py

Brute force, the worst possible thing to do when you have 16 millions of combinations.

```
$ ./run.py -a brute -s 42
[...]
Color to find   : ████ #390C8C
Color found     : ████ #330A8B (ΔE = 0.980)
Iterations      : 139377
Population size : 24
Colors tested   : 3345048
All that in     : 789.034 seconds
```

This one erases the default random population to set its own, which allows it to try `N` (`N` being the population size) variations at each iteration.

## AlgoRandom.py

Random, not necessarily a bad idea.

```
$ ./run.py -a random -s 42
[...]
Color to find   : ████ #390C8C
Color found     : ████ #3A0892 (ΔE = 0.896)
Iterations      : 516
Population size : 24
Colors tested   : 12384
All that in     : 2.984 seconds
```

This one has absolutely no subtlety : it generates a new random population at each iteration.

## AlgoGenetic.py

Genetic algorithm.

```
$ ./run.py -a genetic -s 42
[...]
Color to find   : ████ #390C8C
Color found     : ████ #3C108D (ΔE = 0.698)
Iterations      : 5
Population size : 26
Colors tested   : 130
All that in     : 0.221 seconds
```

Faster, with a much better result and quite nice to watch.

It works by picking an alpha color (the one with the best ΔE), and mating it with all the other colors of our tiny population.

This process gives `N * 4` children colors (there are four genetic operators - excluding mutations, and of course here the genes are the red/green/blue values of the colors).

Only the best children survive to form a new population, which is returned as the result of the current iteration.

After some iterations, the algorithm converges to a quite good solution.

See this [page](https://en.wikipedia.org/wiki/Genetic_algorithm) for more details on genetic algorithms.

## License

ISC.
