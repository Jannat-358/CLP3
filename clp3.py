import random

class Individual:
    def __init__(self, gene_length):
        self.gene_length = gene_length
        self.genes = [random.randint(0, 9) for _ in range(gene_length)]
        self.fitness = 0

    def calc_fitness(self, target_sum):
        sum_first_two = self.genes[0] + self.genes[1]
        self.fitness = max(0, target_sum - abs(target_sum - sum_first_two))


class Population:
    def __init__(self, size, gene_length):
        self.pop_size = size
        self.individuals = [Individual(gene_length) for _ in range(size)]
        self.fittest = 0

    def calculate_fitness(self, target_sum):
        for ind in self.individuals:
            ind.calc_fitness(target_sum)
        self.get_fittest()

    def get_fittest(self):
        fittest_ind = max(self.individuals, key=lambda ind: ind.fitness)
        self.fittest = fittest_ind.fitness
        return fittest_ind

    def get_second_fittest(self):
        sorted_inds = sorted(self.individuals, key=lambda ind: ind.fitness, reverse=True)
        return sorted_inds[1]

    def get_least_fittest_index(self):
        return min(range(self.pop_size), key=lambda i: self.individuals[i].fitness)


class SimpleGA:
    def __init__(self, target_sum, gene_length):
        self.target_sum = target_sum
        self.gene_length = gene_length
        self.population = Population(10, gene_length)
        self.fittest = None
        self.second_fittest = None

    def selection(self):
        self.fittest = self.population.get_fittest()
        self.second_fittest = self.population.get_second_fittest()

    def crossover(self):
        crossover_point = random.randint(0, self.gene_length - 1)
        for i in range(crossover_point):
            self.fittest.genes[i], self.second_fittest.genes[i] = \
                self.second_fittest.genes[i], self.fittest.genes[i]

    def mutation(self):
        mutation_point = random.randint(0, self.gene_length - 1)
        self.fittest.genes[mutation_point] = random.randint(0, 9)

        mutation_point = random.randint(0, self.gene_length - 1)
        self.second_fittest.genes[mutation_point] = random.randint(0, 9)

    def get_fittest_offspring(self):
        return self.fittest if self.fittest.fitness > self.second_fittest.fitness else self.second_fittest

    def add_fittest_offspring(self):
        self.fittest.calc_fitness(self.target_sum)
        self.second_fittest.calc_fitness(self.target_sum)
        idx = self.population.get_least_fittest_index()
        self.population.individuals[idx] = self.get_fittest_offspring()

    def run(self):
        self.population.calculate_fitness(self.target_sum)

        while self.population.fittest < self.target_sum:
            self.selection()
            self.crossover()
            if random.randint(0, 6) < 5:
                self.mutation()
            self.add_fittest_offspring()
            self.population.calculate_fitness(self.target_sum)

        result = self.population.get_fittest().genes
        print("Output:", *result)


# ======== User Input =========== #
if __name__ == "__main__":
    try:
        T = int(input("Enter target : "))
        k = int(input("Enter length of list : "))
        if k < 2:
            raise ValueError("List length must be at least 2.")

        ga = SimpleGA(target_sum=T, gene_length=k)
        ga.run()

    except ValueError as ve:
        print("Invalid input:", ve)
