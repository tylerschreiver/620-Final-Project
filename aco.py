import random
import math

class ACO:
  grid = None
  alpha = 0
  beta = 0
  rho = 0
  pheremones = [[]]
  genCurrent = 0
  genTotal = 0
  ants = []
  def __init__(self, graph, generations, numAnts, a, b, r):
    self.grid = graph
    self.genTotal = generations
    self.alpha = a
    self.beta = b
    self.rho = r
    self.pheremones = [[1 for i in range(graph.tourSize)] for j in range(graph.tourSize)]
    for i in range(numAnts): self.ants.append(Ant(i, self))
    for j in range(generations):
      print(j)
      self.dispatchAnts()
      self.updatePheremones()

  def dispatchAnts(self):
    for ant in self.ants:
      ant.path = []
      ant.pathLength = 0
      for i in range(self.grid.tourSize):
        ant.selectCity()
        ant.findProbabilities()
      ant.goHome()

  def updatePheremones(self):
    newPheremones = [[0 for i in range(self.grid.tourSize)] for j in range(self.grid.tourSize)]
    for i in range(self.grid.tourSize):
      for j in range(self.grid.tourSize):
        totalFitnessOfAntsUsingThisEdge = 0
        for ant in self.ants:
          totalFitnessOfAntsUsingThisEdge += ant.fitnessForAntForEdge(i, j)
        newPheremones[i][j] = (1-self.rho) * self.pheremones[i][j] + totalFitnessOfAntsUsingThisEdge
    self.pheremones = newPheremones

  def getBestPath(self):
    bestAnt = self.ants[0]
    for i in range(1, len(self.ants)):
      if (self.ants[i].pathLength < bestAnt.pathLength): bestAnt = self.ants[i]
    return bestAnt.path


class Ant:
  index = 0
  path = []
  pathLength = 0
  aco = None
  currentCity = None
  probability = [[]]
  def __init__(self, i, antColony): 
    self.index = i
    self.aco = antColony
    # ant starts at a random home
    self.currentCity = self.aco.grid.cities[random.randint(0, len(self.aco.grid.cities) - 1)]
    self.path.append(self.currentCity)
    self.probability = [[(1/self.aco.grid.tourSize) for i in range(self.aco.grid.tourSize)] for j in range(self.aco.grid.tourSize)]

  def selectCity(self):
    # availableCities = cities - self.path
    availableCities = [x for x in self.aco.grid.cities if x not in self.path]
    prob = self.probability[self.currentCity.index]
    odds = [0 for i in range(len(availableCities))]
    odds.append(prob[0])
    for i in range(1, len(availableCities) - 1):
      odds[i] = odds[i-1] + prob[availableCities[i].index]


    
    randVal = random.random()
    index = -1
    for i in range(len(odds) - 1): 
      if odds[i] > randVal:
        index = availableCities[i].index
        break
    if index == -1: index = availableCities[len(availableCities) - 1].index
    
    print(index)
    self.currentCity = self.aco.grid.cities[index] #availableCities[random.randint(0, len(availableCities) - 1)] 
    self.path.append(self.currentCity)
    self.pathLength += self.aco.grid.costMatrix[self.path[len(self.path) - 1].index][self.path[len(self.path) - 2].index]

  def findProbabilities(self):
    availableCities = [x for x in self.aco.grid.cities if x not in self.path]
    for i in range(self.aco.grid.tourSize):
      denominator = 0
      for l in range(len(availableCities)):
        if availableCities[l].index is not i:
          denominator += math.pow(self.aco.pheremones[i][availableCities[l].index], self.aco.alpha) * math.pow(1 / self.aco.grid.costMatrix[i][availableCities[l].index], self.aco.beta) 
      if denominator is not 0:
        for j in range(self.aco.grid.tourSize):
          if i is not j:
            numerator = math.pow(self.aco.pheremones[i][j], self.aco.alpha) * math.pow(1 / self.aco.grid.costMatrix[i][j], self.aco.beta)
            self.probability[i][j] = (numerator / denominator)

  def goHome(self):
    self.path.append(self.path[0])

  def fitnessForAntForEdge(self, i, j):
    hasEdge = False
    for i in range(len(self.path)-1):
      if ((self.path[i].index == i and self.path[i+1].index == j) or
          (self.path[i].index == j and self.path[i+1].index == i)): hasEdge = True
    if hasEdge and self.pathLength != 0: return 1 / self.pathLength
    else: return 0

