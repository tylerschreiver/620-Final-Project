import random
import math
import matplotlib.pyplot as plt
from aco import ACO

class Grid:
  gridSize = 0
  tourSize = 0
  cities = []
  costMatrix = [[]]
  def __init__(self, n, numCities):
    self.gridSize = n
    self.tourSize = numCities
    for i in range(0, numCities):
      self.cities = addCity(self.cities, self.gridSize, i)
    self.createCostMatrix()

  def createCostMatrix(self):
    self.costMatrix = [[0 for i in range(self.tourSize)] for x in range(self.tourSize)]
    for i in range(self.tourSize):
      for j in range(self.tourSize):
        self.costMatrix[i][j] = distance(self.cities[i], self.cities[j])

class City:
  x = 0
  y = 0
  index = 0
  def __init__(self, row, col, i):
    self.x = row
    self.y = col
    self.index = i
  def __str__(self):
    return "(" + str(self.x) + ", " + str(self.y) + ")"

def distance(city1, city2):
  return math.sqrt( math.pow((city2.x-city1.x), 2) + math.pow((city2.y-city1.y), 2) )

# no repeat cities....just in case
def checkValidCoords(x, y, cities):
  isValid = True
  for city in cities:
    if city.x is x and city.y is y:
      isValid = False
      print("This check wasn't worthless")
  return isValid

def addCity(cities,size, index):
  isValid = False
  # prevents 2 cities from having same x and y coord
  while isValid is False:
    x = random.randint(0, size-1)
    y = random.randint(0, size-1)
    isValid = checkValidCoords(x, y, cities)
  cities.append(City(x, y, index))
  return cities

# currently plots a rando path
def plotGraph(grid, path):
  x = []
  y = []
  for city in grid.cities:
    x.append(city.x)
    y.append(city.y)
  plt.scatter(x,y)

  for i in range(len(path)-1):
    x = []
    x.append(path[i].x)
    x.append(path[i+1].x)
    y = []
    y.append(path[i].y)
    y.append(path[i+1].y)
    plt.plot(x,y)
  plt.show()

 
# Initialize 100 x 100 Grid with 15 cities
grid = Grid(100, 15)

# ACO (grid, numGenerations, numAnts, alpha, beta, rho)
aco = ACO(grid, 10, 5, .5, .5, .5)
#aco = ACO(grid, 1, 1, .5, .5, .5)
path = aco.getBestPath()


plotGraph(grid, path)
