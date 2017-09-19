from my_module import *  # my functions
import matplotlib.pyplot as plt  # for plotting results
from time import clock  # to measure time

n = 37  # number of cities
# Reading data
data = []  # for distances data
read_data("distances.txt", data)

cases = [2**i for i in range(2, 8)]
results = open("results.txt", "w")

for case in cases:
    start = clock()  # time start
    pop_size = case  # population size
    population = []  # stores the population as matrix
    fitness_list = []  # for storing fitness values
    prob_list = []  # for storing probabilities of selecting

    # Generating population
    gen_pop(population, n, pop_size)

    # Body
    tot_it = 12000  # maximum number of iterations
    p_cross = 0.6  # crossover probability
    p_mut = 0.1  # mutation probability
    x = []  # for storing iteration numbers
    y = []  # for storing the shortest distance in each population
    M = 3000  # if minimal value has not change in M iterations, break loop
    best = []  # for storing information about yhe best individual
    for it in range(tot_it):
        # Fitness calculations
        dist = fitness(population, n, pop_size, data)

        # Selecting new population
        best = select(population, dist, pop_size)
        # '''
        if it % 1000 == 0:  # Prints data while in progress
            print(it, "\t", best[0])
        # '''
        x.append(it)  # data for plotting
        y.append(best[0])  # data for plotting

        if it > M:  # check if converged or out of range
            m = np.mean(y[it - M:it])
            if m == y[-1] or it == tot_it:
                break

        # Crossover
        to_cross = []
        for i in range(pop_size):  # choose individuals to crossover
            if random() < p_cross:
                to_cross.append(i)
        if len(to_cross) % 2 == 1:  # if odd number chosen, add another one
            can = randrange(pop_size)
            while can in to_cross:
                can = randrange(pop_size)
            to_cross.append(can)
        while len(to_cross) != 0:  # cross random individuals
            ind_a = to_cross[randrange(len(to_cross))]
            to_cross.remove(ind_a)
            ind_b = to_cross[randrange(len(to_cross))]
            to_cross.remove(ind_b)
            crossover(population, ind_a, ind_b, n)

        # Mutation
        for i in range(pop_size):
            if random() < p_mut:
                mutate(population, i, n)

    # Review
    print("N =", pop_size)
    print("Final result:", y[-1], ", iterations:", x[-1])
    min_res = min(y)  # minimal distance
    min_ind = y.index(min_res)  # at iteration min_ind
    final_ind = best[2]  # the FINAL individual
    print("The best result:", min_res, "in iteration", min_ind)
    stop = clock()
    time = format(stop - start, ".3f")
    print("Time:", time, "s\n")
    results.write(str(pop_size) + "\t" + str(min_res) + "\t" + str(time) + "\n")  # write data to file
    plt.plot(x, y, label="N = " + str(pop_size))
    if min_res <= 16515:
        print(final_ind)
        break

results.close()
plt.legend()
plt.ylabel("Total distance")
plt.xlabel("# iterations")
plt.show()
