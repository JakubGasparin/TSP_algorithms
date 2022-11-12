import math
import random
from copy import copy
import matplotlib.pyplot as plt
from itertools import islice
import numpy
import numpy as np

import yaml

POPULATION_NUMBER = 60
TOTAL_STEPS = 1000

CITIES = {}
BEST_FITNESS = 0
BEST_PARENTS = []
ALL_FITNESS_VALUES = []
NEW_GENERATION = []
FITNESS_FOR_PLOTTING = []

MAX_ELITISM = 10  # VÝBER V PERCENTÁCH
MAX_ROULETTE = 10  # VÝBER V PERCENTÁCH
MUTATION_CHANCE = 10 # VÝBER V PERCENTÁCH


def _solve_TSP(list_cities):
    _get_two_cities(list_cities)


def _calculate_distance(first_city, second_city, list_cities):
    first_city = str(first_city)
    second_city = str(second_city)
    first_city_x = CITIES[first_city][0]
    second_city_x = CITIES[second_city][0]
    first_city_y = CITIES[first_city][1]
    second_city_y = CITIES[second_city][1]
    distance = math.pow((second_city_x - first_city_x), 2.0) + math.pow((second_city_y - first_city_y), 2.0)
    distance = math.sqrt(distance)
    return distance


def _get_two_cities(list_cities): # zoberie dve mestá medzi ktorými vypočíta vzdialenosť
    max_key = _get_max_key()
    index = 0
    total_distance = []
    for i in range(max_key):
        if index == max_key:
            break
        distance = _calculate_distance(list_cities[index], list_cities[index + 1], list_cities)
        total_distance.append(distance)
        index += 1
    fitness = _get_fitness(sum(total_distance))
    ALL_FITNESS_VALUES.append(fitness)
    _compare_current_highest_fitness(fitness)


def _get_fitness(total_distance):
    return 1 / total_distance


def _compare_current_highest_fitness(fitness):
    global BEST_FITNESS
    if fitness > BEST_FITNESS:
        return


def _get_max_key():
    max_key = list(CITIES)[-1]
    max_key = int(max_key)
    return max_key


def _get_max_fitness_and_its_city():
    global BEST_FITNESS
    global BEST_PARENTS
    temp = max(ALL_FITNESS_VALUES)
    if BEST_FITNESS < temp:
        BEST_FITNESS = temp
        index = ALL_FITNESS_VALUES.index(BEST_FITNESS)
        BEST_PARENTS.clear()
        BEST_PARENTS.append(copy(NEW_GENERATION[index]))



def _TSP_hub(list_cities):
    old_generation = list_cities
    new_generation = _select_parents(list_cities)
    _one_point_crossover(new_generation)
    _swap_mutation()

    i = 0
    for steps in range(TOTAL_STEPS):
        ALL_FITNESS_VALUES.clear()
        for i in range(len(NEW_GENERATION)):    # vypocet fitness values
            _solve_TSP(NEW_GENERATION[i])
            i += 1

        _get_max_fitness_and_its_city()

        list_cities = NEW_GENERATION            # tvorba novej generacie
        new_generation = _select_parents(list_cities)
        NEW_GENERATION.clear()
        _one_point_crossover(new_generation)
        _swap_mutation()
        FITNESS_FOR_PLOTTING.append(copy(BEST_FITNESS))

    print(BEST_FITNESS, BEST_PARENTS)

    _plot_TSP()
    _plot_FITNESS()


def _plot_FITNESS():
    plt.plot(FITNESS_FOR_PLOTTING)
    plt.show()


def _plot_TSP():
    keys = CITIES.keys()
    plot_parents = BEST_PARENTS[0]
    x_cor = []
    y_cor = []
    for key, cor in CITIES.items():
        #print(key, ":", cor[0], cor[1])
        x_cor.append(copy(cor[0]))
        y_cor.append(copy(cor[1]))
    plt.scatter(x_cor, y_cor)
    x_cor.clear()
    y_cor.clear()

    for i in range(21):
        str_key = str(plot_parents[i])
        value = CITIES[str_key]
        x_cor.append(copy(value[0]))
        y_cor.append(copy(value[1]))
    plt.plot(x_cor, y_cor)
    plt.show()
    return


def _swap_mutation():
    global NEW_GENERATION
    for i in range(len(NEW_GENERATION)):
        if random.randrange(1, 100) >= MUTATION_CHANCE:
            pass
        else:
            temp = NEW_GENERATION[i]
            first_bit = random.choice(temp)
            while first_bit == temp[0]:
                first_bit = random.choice(temp)
            second_bit = random.choice(temp)
            f = 0
            while f < 100:  # infinite loop
                second_bit = random.choice(temp)
                if second_bit != first_bit:
                    if second_bit != temp[0]:
                        break
            first_index = temp.index(first_bit)
            second_index = temp.index(second_bit)
            temp[first_index], temp[second_index] = temp[second_index], temp[first_index]
            NEW_GENERATION[i] = temp


def _one_point_crossover(list_cities):    # oredelit list v strede a delime pravu cast
    first_offspring = []
    second_offspring = []
    offsprings_list = []
    global POPULATION_NUMBER
    length = len(list_cities)
    length = round(length)
    length = int(length)
    #for i in range(0, len(list_cities), 2):
    while len(NEW_GENERATION) < POPULATION_NUMBER:
        # _produce_offsprings(list_cities[i:i + 2])
        _produce_offsprings(random.sample(list_cities, 2))
    pass


def _produce_offsprings(list_of_parents):
    # print(list_of_parents)
    first_parent = list_of_parents[0]
    second_parent = list_of_parents[1]
    length = round(len(first_parent)/2)
    # print(length)
    first_half = first_parent[length:]
    del first_half[-1]
    second_half = second_parent[length:]
    del second_half[-1]
    first_offspring = first_parent[:length]
    second_offspring = second_parent[:length]
    list_of_first = []
    list_of_second = []
    for i in range(len(first_half)):  # spravy dummy pole do ktorého budem vkladat nove deti
        list_of_first.append(0)
        list_of_second.append(0)

    for i in range(len(first_half)):
        if first_half[i] in second_half:    # algoritmus na crossover
            index1 = first_half.index(first_half[i])
            index2 = second_half.index(first_half[i])
            list_of_first[index2] = first_half[i]
            list_of_second[index1] = first_half[i]
    for i in range(len(first_half)):    # vyplnenie udajov ktoré nám chýbajú
        if first_half[i] not in list_of_first:
            for f in range(len(list_of_first)):
                if list_of_first[f] == 0:
                    list_of_first[f] = first_half[i]
                    break
    for i in range(len(second_half)):
        if second_half[i] not in list_of_second:
            for f in range(len(list_of_second)):
                if list_of_second[f] == 0:
                    list_of_second[f] = second_half[i]
                    break
    first_offspring = first_offspring + list_of_first
    second_offspring = second_offspring + list_of_second
    first_offspring.append(copy(first_offspring[0]))
    second_offspring.append(copy(second_offspring[0]))
    NEW_GENERATION.append(copy(first_parent))
    NEW_GENERATION.append(copy(second_parent))
    NEW_GENERATION.append(copy(first_offspring))
    NEW_GENERATION.append(copy(second_offspring))


def _select_parents(list_cities):
    elitism_list, list_cities = _elitism_parent_selection(list_cities) #vyber pomocou elitismu
    elitism_list, list_cities = _roulette_selection(list_cities, elitism_list) # zozvysku potom vyberieme pomocou rulety
    return elitism_list


def _elitism_parent_selection(list_cities):
    parents = []
    elites = (MAX_ELITISM/100) * len(list_cities)
    elites = math.ceil(elites)
    #print(elites)
    for i in range(elites):
        best_fitness = (max(ALL_FITNESS_VALUES))
        index = ALL_FITNESS_VALUES.index(best_fitness)
        parents.append(copy(list_cities[index]))
        ALL_FITNESS_VALUES.pop(index)
        list_cities.remove(list_cities[index])
    #print(len(parents))
    return parents, list_cities


def _roulette_selection(list_cities, elitism_list):
    roulette = (MAX_ROULETTE/100) * len(list_cities)
    roulette = math.ceil(roulette)
    s = sum(ALL_FITNESS_VALUES)
    rand = random.uniform(0, s)

    ss = 0
    for h in range(roulette):
        for i in range(0, len(list_cities)):
            ss += ALL_FITNESS_VALUES[i]
            if ss > rand:
                best_fitness = (max(ALL_FITNESS_VALUES))
                index = ALL_FITNESS_VALUES.index(best_fitness)
                elitism_list.append(copy(list_cities[index]))
                ALL_FITNESS_VALUES.pop(index)
                list_cities.remove(list_cities[index])
                break
    #print(len(list_cities))
    #print(len(elitism_list))
    return elitism_list, list_cities


def _generate_first_population():
    max_key = _get_max_key()
    list_cities = []
    current_population_list = []

    for i in range(max_key):
        list_cities.append(i + 1)

    for i in range(POPULATION_NUMBER):
        random.shuffle(list_cities)
        list_cities.append(list_cities[0])
        current_population_list.append(copy(list_cities))
        _solve_TSP(list_cities)
        list_cities.pop()
    print(current_population_list)
    _TSP_hub(current_population_list)


if __name__ == "__main__":
    with open("cities.yaml", "r") as file:
        CITIES = yaml.safe_load(file)
    print(CITIES)
    _generate_first_population()
