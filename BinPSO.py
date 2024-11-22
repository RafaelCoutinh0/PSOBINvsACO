
# importando módulos
import sys
import numpy as np
import matplotlib.pyplot as plt
import random

# importando PySwarms
import pyswarms as ps

#[2] Geração do Grafo e Função de Custo

# função graphTSP(numCities, minDist, maxDist)
# parâmetros:
#   numCities: número de cities
#   minDist: menor valor de distância
#   maxDist: maior valor de distância
# retorno:
#   roads: lista de estradas - arestas: (cidade1, cidade2, distância). As distâncias
#   entre duas cidades são determinadas aleatoriamente entre minDist e maxDist
def graphTSP(numCities, minDist, maxDist):
  roads = []
  for i in range(numCities):
    for j in range(i+1, numCities):
      roads.append((i, j, random.randint(minDist, maxDist)))
  return roads

numCities = 5     #  Número de cidade inicial

while(True):
  numCities = int(input('Digite o número de cidades [>4]: '))
  if (numCities > 4):
    break
  else:
    print('O número de cidades deve ser maior que 4!')

roads = graphTSP(numCities, 10, 100)


# Função evalRoutes(particles)
# parâmetros:
#   particles: array (numpy.ndarray) de posições das partículas (rotas)
# retorno:
#   costs: lista de custos para cada partícula.
def evalRoutes(particles):
  costs = []
  for individual in particles:
    cost = 0;

    validArcs = np.where(individual == 1)[0]

    for arc in validArcs:
      cost = cost + roads[arc][2]

    for i in range(numCities):
      count = 0
      for arc in validArcs:
        if (roads[arc][0]==i or roads[arc][1]==i):
          count = count + 1
      if(count!=2):
        cost = cost + 10000

    if(sum(individual)!=numCities):
      cost = cost + 10000
    else:
      # identificar a ocorrência de ciclos
      validArcs = list(validArcs)
      current = validArcs[0]
      visited = [roads[current][0]]
      while(len(validArcs)>1):
        node = roads[current][1]
        if (not roads[current][0] in visited):
          node = roads[current][0]
        elif (roads[current][1] in visited):
          cost = cost + 10000
          break
        visited.append(node)
        validArcs.remove(current)
        for arc in validArcs:
          if (node == roads[arc][0] or node == roads[arc][1]):
            current = arc
            break

    costs.append(cost)

  return costs

print('Grafo:')
for road in roads:
  print(road)

# [3] Hiperparâmetros e Otimização

numParticles = 100

while (True):
    numParticles = 200
    #   int(input('Digite o número de partículas [>=10]: '))
    if (numParticles >= 10):
        break
    else:
        print('O número de partículas deve ser maior ou igual a 10!')

numIters = 10

while (True):
    numIters = 1000
    # int(input('Digite o número de iterações do algoritmo [>=10]: '))
    if (numIters >= 10):
        break
    else:
        print('Use no mínimo 10 iterações!')

# hiperparâmetros
options = {'c1': 0.7, 'c2': 0.3, 'w': 1, 'k': (numParticles - 1), 'p': 1}

# instanciação de objeto da classe BinaryPSO
optimizer = ps.discrete.binary.BinaryPSO(n_particles=numParticles, dimensions=len(roads), options=options,
                                         velocity_clamp=(-3, 3))

# execução da otimização
cost, pos = optimizer.optimize(evalRoutes, iters=numIters)

print('Custo = ', cost)

validArcs = np.where(pos == 1)[0]
print('Arcos: ')
for arc in validArcs:
    print(roads[arc])