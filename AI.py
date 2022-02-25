import pygame, random
import numpy as np
from copy import deepcopy
from main import Game
from genome import Genome

def w_data_save(genome):
  f = open("save.txt", 'w')
  f.write(str(genome.w1) + "\n\n" + str(genome.w2) + "\n\n" + str(genome.w3) + "\n\n" + str(genome.w4))
  f.close()
  
N_POPULATION = 50
N_BEST = 5
N_CHILDREN = 4
PROB_MUTATION = 0.5

genomes = [Genome() for _ in range(N_POPULATION)]
best_genomes = None

n_gen = 0
while True:
  n_gen += 1

  for i, genome in enumerate(genomes):
    game = Game(genome=genome)
    fitness, score = game.runGame()

    genome.fitness = fitness
    genome.score = score

  if best_genomes is not None:
    genomes.extend(best_genomes)
  genomes.sort(key=lambda x: x.fitness, reverse=True)

  print('===== Generaton #%s\tBest Fitness %s Score %s =====' % (n_gen, genomes[0].fitness, genomes[0].score))

  best_genomes = deepcopy(genomes[:N_BEST])

  w_data_save(best_genomes[0])
  # crossover
  for i in range(N_CHILDREN):
    new_genome = deepcopy(best_genomes[0])
    a_genome = random.choice(best_genomes)
    b_genome = random.choice(best_genomes)
    c_genome = random.choice(best_genomes)
    d_genome = random.choice(best_genomes)

    cut = random.randint(0, new_genome.w1.shape[1])
    new_genome.w1[i, :cut] = a_genome.w1[i, :cut]
    new_genome.w1[i, cut:] = b_genome.w1[i, cut:]

    cut = random.randint(0, new_genome.w2.shape[1])
    new_genome.w2[i, :cut] = a_genome.w2[i, :cut]
    new_genome.w2[i, cut:] = b_genome.w2[i, cut:]

    cut = random.randint(0, new_genome.w3.shape[1])
    new_genome.w3[i, :cut] = a_genome.w3[i, :cut]
    new_genome.w3[i, cut:] = b_genome.w3[i, cut:]

    cut = random.randint(0, new_genome.w4.shape[1])
    new_genome.w4[i, :cut] = a_genome.w4[i, :cut]
    new_genome.w4[i, cut:] = b_genome.w4[i, cut:]
    

    cut = random.randint(0, new_genome.b1.shape[0])
    new_genome.b1[:cut] = c_genome.b1[:cut]
    new_genome.b1[cut:] = d_genome.b1[cut:]

    cut = random.randint(0, new_genome.b2.shape[0])
    new_genome.b2[:cut] = c_genome.b2[:cut]
    new_genome.b2[cut:] = d_genome.b2[cut:]

    cut = random.randint(0, new_genome.b3.shape[0])
    new_genome.b3[:cut] = c_genome.b3[:cut]
    new_genome.b3[cut:] = d_genome.b3[cut:]

    cut = random.randint(0, new_genome.b4.shape[0])
    new_genome.b4[:cut] = c_genome.b4[:cut]
    new_genome.b4[cut:] = d_genome.b4[cut:]

    best_genomes.append(new_genome)


  # mutation
  genomes = []
  for i in range(int(N_POPULATION / (N_BEST + N_CHILDREN))):
    for bg in best_genomes:
      new_genome = deepcopy(bg)

      mean = 20
      stddev = 10

      if random.uniform(0, 1) < PROB_MUTATION:
        new_genome.w1 += new_genome.w1 * np.random.normal(mean, stddev, size=(4, 10)) / 100 * np.random.randint(-1, 2, (4, 10))
      if random.uniform(0, 1) < PROB_MUTATION:
        new_genome.w2 += new_genome.w2 * np.random.normal(mean, stddev, size=(10, 20)) / 100 * np.random.randint(-1, 2, (10, 20))
      if random.uniform(0, 1) < PROB_MUTATION:
        new_genome.w3 += new_genome.w3 * np.random.normal(mean, stddev, size=(20, 10)) / 100 * np.random.randint(-1, 2, (20, 10))
      if random.uniform(0, 1) < PROB_MUTATION:
        new_genome.w4 += new_genome.w4 * np.random.normal(mean, stddev, size=(10, 6)) / 100 * np.random.randint(-1, 2, (10, 6))

      if random.uniform(0, 1) < PROB_MUTATION:
        new_genome.b1 += new_genome.b1 * np.random.normal(mean, stddev, size=(10)) / 100 * np.random.randint(-1, 2, (10))
      if random.uniform(0, 1) < PROB_MUTATION:
        new_genome.b2 += new_genome.b2 * np.random.normal(mean, stddev, size=(20)) / 100 * np.random.randint(-1, 2, (20))
      if random.uniform(0, 1) < PROB_MUTATION:
        new_genome.b3 += new_genome.b3 * np.random.normal(mean, stddev, size=(10)) / 100 * np.random.randint(-1, 2, (10))
      if random.uniform(0, 1) < PROB_MUTATION:
        new_genome.b4 += new_genome.b4 * np.random.normal(mean, stddev, size=(6)) / 100 * np.random.randint(-1, 2, (6))

      genomes.append(new_genome)
