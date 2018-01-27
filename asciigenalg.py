#!/usr/bin/env python
import random
import sys

SPACE = ' '
START_CHA_ORD = ord(SPACE)
END_CHAR_ORD = 126
END_LINE = '\n'

POPULATION_SIZE = 50
ITERATION = 5000
TOP = 10
CROSSOVER_SOLUTION = 10
MUTATION_SOLUTION = 10
NEW_SOLUTION = 5
BOT = CROSSOVER_SOLUTION + MUTATION_SOLUTION + NEW_SOLUTION

MUTATION_EDGE = 0.8
CROSSOVER_EDGE = 0.8

SHOW_ITERATION = 1000

class Solution:
    score = -1
    chromosome = []

    def __init__(self, chromosome=[], score=-1):
        self.score = score
        self.chromosome = chromosome
  
    def print_score_solution(self):
        print(self.score)
        print_solution(self.chromosome)

def main(argv):
    template = []
    line_size = 0
    lines_count = 0
    
    with open(argv[1]) as f:
        origin = list(f)
    line_size = max(map(lambda x: len(x), origin))
    lines_count = len(origin)

    for l in origin:
        striped = l.replace(END_LINE, SPACE);
        new_list = list(striped)
        new_list.extend([SPACE] * (line_size-len(striped)))
        template.append(new_list)
    
    best_score = score_solution(template, template)
            
    population = create_population(line_size, lines_count, POPULATION_SIZE, template)
    show = 0
    for i in range(ITERATION):
        if i == show:
            show = 2 * show + 1
            print("\n\n\n\n\nIteration: ", i)
            population[0].print_score_solution()
      
        population.sort(key=lambda x: x.score, reverse=True)
        if population[0].score == best_score:
            print("\n\n\n\n\nBest solution found. Iteration: ", i)
            break

        new_solutions = []

        for _ in range(CROSSOVER_SOLUTION):  
            new_solutions.append(crossover(population[random.randint(0, TOP - 1)], population[random.randint(0, POPULATION_SIZE - 1)], template))

        for _ in range(MUTATION_SOLUTION):
            new_solutions.append(mutation(population[random.randint(0, POPULATION_SIZE - 1)], template))

        for _ in range(NEW_SOLUTION):
            new_solutions.append(create_solution(line_size, lines_count, template))

        del population[-BOT:]
    
        population.extend(new_solutions)

    
    population[0].print_score_solution()
    

def create_population(line_size, lines_count, population_size, template):
    population = []
    for _ in range(population_size):
        population.append(create_solution(line_size, lines_count, template))
    
    return population
        
def create_solution(line_size, lines_count, template):
    chromosome = []
    #  for _ in range(lines_count):
    #    solution.chromosome.append([chr(random.randrange(START_CHA_ORD, END_CHAR_ORD + 1, 1)) for _ in range (line_size)])
    for _ in range(lines_count):
        l = []
        for _ in range(line_size):
            l.append(template[random.randint(0, lines_count-1)][random.randint(0, line_size-1)])
        chromosome.append(l)
    solution = Solution(chromosome, score_solution(chromosome, template))
    return solution
  
def score_solution(solution, template):
    score = 0
    for x in range(len(solution)):
        for y in range(len(solution[x])):
            if solution[x][y] == template[x][y]:
                score += 1
    return score
    
def mutation(solution, template):
    chromosome = []
    for l in solution.chromosome:
        new_l = []
        for i in l:
            if random.random() > MUTATION_EDGE:
#                new_l.append(chr(random.randint(START_CHA_ORD, END_CHAR_ORD)))
                new_l.append(template[random.randint(0, len(template)-1)][random.randint(0, len(template[0])-1)])
            else:
                new_l.append(i)
        chromosome.append(new_l)
    new_solution = Solution(chromosome, score_solution(chromosome, template))
    return new_solution

def crossover(top_solution, other_solution, template):
    chromosome = []
    for x in range(len(top_solution.chromosome)):
        line = []
        for y in range(len(top_solution.chromosome[x])):
            if random.random() > CROSSOVER_EDGE:
                line.append(other_solution.chromosome[x][y])
            else:
                line.append(top_solution.chromosome[x][y])
        chromosome.append(line)
  
    new_solution = Solution(chromosome, score_solution(chromosome, template))
    return new_solution

def print_solution(solution):        
    for l in solution:
        print(''.join(l))
            

if __name__ == "__main__":
    main(sys.argv)
    