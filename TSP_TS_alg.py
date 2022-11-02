import math

import yaml
import random
from copy import copy

CITIES = {}
TABU_LIST = []


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

    print(bestFitness, bestNeighbour)  # nasiel som lokalny extrem, teraz musím sa z neho dostať



def _get_best_neighbour(neighbours, fitness):
    best_fitness = fitness
    best_neighbour = neighbours[0]
    for i in range(len(neighbours)):
        current_fitness = _get_two_cities(neighbours[i])
        if best_fitness < current_fitness:
            best_fitness = current_fitness
            best_neighbour = neighbours[i]
    return best_fitness, best_neighbour


def _get_neighbours(solution):  # source: https://towardsdatascience.com/how-to-implement-the-hill-climbing-algorithm-in-python-1c65c29469de
    neighbours = []
    starting_city = solution[0]
    solution.remove(starting_city)
    solution.pop()
    for i in range(len(solution)):
        for j in range(i + 1, len(solution)):
            neighbour = solution.copy()
            neighbour[i] = solution[j]
            neighbour[j] = solution[i]
            neighbour.insert(0, starting_city)
            neighbour.append(copy(starting_city))
            neighbours.append(neighbour)
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
