import math

import yaml
import random
from copy import copy
from itertools import chain

CITIES = {}
TABU_LIST = []
TABU_FITNESS = []
TABU_TENURE = []


def _generate_solution():
    max_key = _get_max_key()
    solution = []
    for i in range(max_key):
        solution.append(i + 1)
    random.shuffle(solution)
    solution.append(copy(solution[0]))
    _solve_TSP(solution)


# toto volam ked vypočítam cestu medzi mestami. táto časť využíva Hill Climbing algoritmus, vytvorená s pomocou:
# https://towardsdatascience.com/how-to-implement-the-hill-climbing-algorithm-in-python-1c65c29469de

def _solve_TSP(solution):
    curr_fitness = _get_two_cities(solution)
    neighbours = _get_neighbours(solution)
    bestFitness, bestNeighbour = _get_best_neighbour(neighbours, curr_fitness)

    while curr_fitness < bestFitness:
        curr_fitness = bestFitness
        curr_bestNeighbour = bestNeighbour
        neighbours = _get_neighbours(curr_bestNeighbour)
        bestFitness, bestNeighbour = _get_best_neighbour(neighbours, curr_fitness)

     # nasiel som lokalny extrem, teraz musím sa z neho dostať

    print(bestFitness, bestNeighbour)
    TABU_LIST.append(bestNeighbour)
    TABU_FITNESS.append(bestFitness)
    _tabu_search(bestNeighbour, bestFitness)


def _tabu_search(current_bestNeighbour, current_bestFitness): # zaciatok tabu search
    neighbours = _get_neighbours(current_bestNeighbour)
    print(len(neighbours))
    tabu_neighbours = _remove_tabod_solutions(neighbours)
    print(len(tabu_neighbours), len(neighbours))
    bestFitness, bestNeighbour = _get_best_neighbour(tabu_neighbours, current_bestFitness)

    while bestFitness == current_bestFitness:
        tabu_neighbours = _remove_tabod_solutions(tabu_neighbours)
        bestFitness, bestNeighbour = _get_best_neighbour(tabu_neighbours, current_bestFitness)
    print(bestFitness, bestNeighbour)
    pass


def _remove_tabod_solutions(neighbours):
    for i in range(len(TABU_LIST)):
        fitness_tabo = TABU_FITNESS[i]
        for f in range(len(neighbours)):
            fitness_neighbour = _get_two_cities(neighbours[f])
            # print(fitness_neighbour)
            if fitness_tabo == fitness_neighbour:
                print(fitness_neighbour)
                print(neighbours[f])
                neighbours.remove(neighbours[f])
                break
    return neighbours


def _get_best_neighbour(neighbours, fitness):
    best_fitness = 0
    best_neighbour = neighbours[0]
    for i in range(len(neighbours)):
        current_fitness = _get_two_cities(neighbours[i])
        if best_fitness < current_fitness:
            best_fitness = current_fitness
            best_neighbour = neighbours[i]
    return best_fitness, best_neighbour


# source: https://towardsdatascience.com/how-to-implement-the-hill-climbing-algorithm-in-python-1c65c29469de
def _get_neighbours(solution):
    neighbours = []
    starting_city = solution[0]
    solution.remove(starting_city)
    solution.remove(starting_city)
    for i in range(len(solution)):
        for j in range(i + 1, len(solution)):
            neighbour = solution.copy()
            neighbour[i] = solution[j]
            neighbour[j] = solution[i]
            neighbour.insert(0, starting_city)
            neighbour.append(copy(starting_city))
            neighbours.append(neighbour)
    solution.insert(0, starting_city)
    solution.append(copy(starting_city))
    return neighbours


def _calculate_distance(first_city, second_city):
    first_city = str(first_city)
    second_city = str(second_city)
    first_city_x = CITIES[first_city][0]
    second_city_x = CITIES[second_city][0]
    first_city_y = CITIES[first_city][1]
    second_city_y = CITIES[second_city][1]
    distance = math.pow((second_city_x - first_city_x), 2.0) + math.pow((second_city_y - first_city_y), 2.0)
    distance = math.sqrt(distance)
    return distance


def _get_two_cities(list_cities):  # zoberie dve mestá medzi ktorými vypočíta vzdialenosť
    max_key = _get_max_key()
    index = 0
    total_distance = []
    for i in range(max_key):
        if index == max_key:
            break
        distance = _calculate_distance(list_cities[index], list_cities[index + 1])
        total_distance.append(distance)
        index += 1
    fitness = _get_fitness(sum(total_distance))
    return fitness


def _get_fitness(total_distance):
    return 1 / total_distance


def _get_max_key():
    max_key = list(CITIES)[-1]
    max_key = int(max_key)
    return max_key


if __name__ == "__main__":
    with open("cities.yaml", "r") as file:
        CITIES = yaml.safe_load(file)
    print(CITIES)
    _generate_solution()
