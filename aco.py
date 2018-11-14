'''
http://staff.washington.edu/paymana/swarm/stutzle99-eaecs.pdf
equations broken down from this research paper

α = how much we favor pheremone values
β = how much we favor hueristic values

τ = pheremone value thingy
η = hueristic value = 1 / (distance(i,j))
N = set of cities ant has not visited

p(k)(i,j) = probability ant k will leave city i and go to city j (assuming j is in N)

  ((τ(i,j) ^ α) * ((η(i,j) ^ β))  # numerator
= ------------------------------------------ # division line
  SUM all cities l in N ((τ(i,l) ^ α) * ((η(i,l) ^ β))   # denominator

basically the denominator is the sum of all numerators if that makes sense
This shit is used for constructing the tour and guiding our ants

Onto the pheremone stuff

t = current generation
ρ = pheremone trail evaportation rate   0 < ρ <= 1
L(k) = length of ant k's tour

τ(i,j)(t+1) = (1 - ρ) * τ(i,j)(t) + SUM all ants k ( Δτ(k)(i,j)(t)  )

where
Δτ(k)(i,j)(t) = 1 / L(k)(t)  (Each ants pheremone strength is determined by the fitness of their tour)
if ant k took path (i,j)
and
Δτ(k)(i,j)(t) = 0
if ant k did not take path (i,j)

Basically, the pheremone strength for the next generation is equal to 
  (modifier*curr pheremone strength) + (sum of fitness of all ants who took path (i,j))

'''
import random

class ACO:
  grid = None
  pheremones = [[]]
  genCurrent = 0
  genTotal = 0
  ants = []
  def __init__(self, graph, generations, numAnts):
    self.grid = graph
    self.genTotal = generations
    for i in range(numAnts): self.ants.append(Ant(i))
    self.dispatchAnts()

  def dispatchAnts(self):
    for ant in self.ants:
      for i in range(self.grid.tourSize):
        ant.selectCity(self.grid.cities)
      ant.goHome()

  def ant1Tour(self):
    return self.ants[0].path

class Ant:
  index = 0
  path = []
  currentCity = None
  def __init__(self, i): 
    self.index = i

  def selectCity(self, cities):
    # availableCities = cities - self.path
    availableCities = [x for x in cities if x not in self.path]
    self.path.append(availableCities[random.randint(0, len(availableCities) - 1)])
  
  def goHome(self):
    self.path.append(self.path[0])
