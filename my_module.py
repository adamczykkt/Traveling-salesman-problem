from random import randrange, random
import numpy as np


def read_data(path, data):
    f = open(path, "r")
    for line in f:
        num = line.split()
        for i in range(len(num)):
            num[i] = int(num[i])
        data.append(num)
    f.close()


# printing in matrixform
def pprint(mat):
    print(np.matrix(mat))


# generation of the population
def gen_pop(population, n, pop_size):
    for i in range(pop_size):
        cities = [k for k in range(n)]
        temp = []
        for j in range(n):
            index = randrange(len(cities))
            temp.append(cities[index])
            cities.remove(cities[index])
        population.append(temp)


def distance(population, i, n, data):
    value = 0
    for j in range(n):
        value += data[population[i][j - 1]][population[i][j]]
    return value


# Fitness for the whole population
def fitness(population, n, pop_size, data):
    dist = []
    for i in range(pop_size):
        dist.append(distance(population, i, n, data))
    return dist


# Selection
def select(population, dist, pop_size):
    min_value = min(dist)
    min_index = dist.index(min_value)
    #    if len(list(filter(lambda x: x == min_value, dist))) != 1:
    #        print("There's more!")
    temp = list(map(lambda x: 1.0 / float(x), dist))
    s = sum(temp)
    temp = [i / s for i in temp]
    sel_list = []
    for i in range(pop_size):
        sel_list.append(sum(temp[:i + 1]))
    copy = population[:]
    for j in range(pop_size):
        if dist[j] != min_value:
            p = random()
            for i in range(pop_size):
                if p < sel_list[i]:
                    population[j] = copy[i]
                    break
    return [min_value, min_index, copy[min_index]]


# mutation
def mutate(population, i, n):
    a = randrange(n)
    b = a
    while b == a:
        b = randrange(n)
    pos_1 = min(a, b)
    pos_2 = max(a, b)
    ind = population[i]
    temp = ind[pos_1:pos_2 + 1]
    temp = temp[::-1]
    population[i] = ind[:pos_1] + temp + ind[pos_2 + 1:]


# introducing crossover
def crossover(population, i, j, n):
    ind = [randrange(n)]
    it = 0
    cycle = [population[i][ind[it]]]
    while True:
        b = population[j][ind[it]]
        if b == cycle[0]:
            break
        else:
            cycle.append(b)
            ind.append(population[i].index(b))
            it += 1
    off_1 = population[i][:]
    off_2 = population[j][:]
    for k in range(n):
        if k not in ind:
            off_1[k] = population[j][k]
            off_2[k] = population[i][k]
    population[i] = off_1[:]
    population[j] = off_2[:]
