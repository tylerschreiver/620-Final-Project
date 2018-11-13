import random
import math
import matplotlib.pyplot as plt

class Grid:
  size = 0
  cities = []
  edges = []
  def __init__(self, n, numCities):
    self.size = n
    for i in range(0, numCities):
      self.cities = addCity(self.cities, self.size, i)
    
    #there shouldn't be any repeat edges with shortenInnerLoop
    shortenInnerLoop = 0
    for j in range(0, numCities):
      k = numCities-1
      while k is not shortenInnerLoop:
        if j is not k:
          self.edges.append(Edge(self.cities[j], self.cities[k]))
        k -= 1
      shortenInnerLoop += 1
    

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

# will be used to hold pheremone levels
class Edge:
  city1 = None
  city2 = None
  pheremone = 0
  def __init__(self, c1, c2):
    self.city1 = c1
    self.city2 = c2
  def distance(self):
    return distance(self.city1, self.city2)
  def __str__(self):
    return "[ " + str(self.city1) + ", " + str(self.city2) + " ]"

def distance(city1, city2):
  return math.sqrt( math.pow((city2.x-city1.x), 2) + math.pow((city2.y-city1.y), 2) )

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

def plotGraph(grid):
  x = []
  y = []
  for city in grid.cities:
    x.append(city.x)
    y.append(city.y)
  plt.scatter(x,y)

  for edge in grid.edges:
    x = []
    x.append(edge.city1.x)
    x.append(edge.city2.x)
    y = []
    y.append(edge.city1.y)
    y.append(edge.city2.y)
    plt.plot(x,y)
  plt.show()

  
# Initialize 100 x 100 Grid with 10 cities
grid = Grid(100, 5)
plotGraph(grid)