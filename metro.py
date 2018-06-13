# IIQ 3763 Project - 2018-1
# Staircases and Mechanical Staircases, TASEP
# Pablo Bravo   ptbravo@uc.cl

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import truncnorm

#Classes
class person():
    # 'Particles' that move on staircases
    # They can have different speeds
    def __init__(self, id):
        self.speed = np.random.choice([1,2,3])
        self.set = 0    # Set of staircases
        self.lane = 0   # Lane on set
        self.pos = 0    # Position on lane
        self.id = id
        self.start = 0  # timestep in which they joined staircase
        self.end = 0    # timestep in which they finished staircase
        self.type = np.random.choice(['A', 'B'])

    def to_reserve(self, reserve):
        self.end = t
        reserve.current.append(self.id)

    def to_stair(self, reserve):
        return 0

class reserve():
    # Keeps track and sets order for incoming "waves of people"
    def __init__(self, length, IN, OUT, reserves = []):
        self.IN = IN
        self.OUT = OUT
        self.reserves = reserves
        self.current = []
        self.positions = np.zeros(n_of_persons)
        self.positions += length
        self.flux = 0


    def update(self):
        temporal = []
        F.append(len(self.current))
        for index in self.current:
            self.positions[index - 1] -= P[index - 1].speed
        for index in self.current:
            if self.positions[index - 1] <= 0:
                temporal.append(index)
                self.current.remove(index)
                self.positions[index - 1] = 0
        self.flux += len(temporal)
        #F.append(nlen(temporal))
        print(self.flux)
        #self.OUT.feed(temporal)

    def platform(self, N, train_doors, door_pos):
        for p in P:
            self.current.append(p.id)
        doors = list(np.arange(8)+1)
        D = []
        for p in self.current:
            dist = np.abs(4*np.random.choice(doors) - door_pos)
            D.append(dist)
        self.positions = np.asarray(D)

class staircase_set():
    def __init__(self, id = 1, length = 100, mspeed = [1,1,0,0,0,0]):
        self.length = length
        self.mspeed = np.asarray(mspeed)    # Mechanical staircase speed
        self.matrix = np.zeros([len(self.mspeed), self.length], int)
        self.id = id
        self.wait_line = []

    def p_att(person, l, pos):
        # Updates person attributes
        person.set = self.set
        person.lane = l
        person.pos = pos

    def max_mov(self,l, i, id):
        # Calculates the position that a particle can move without "jumping"
        if id == 0:
            tspeed = self.mspeed[l]
        else:
            tspeed = P[int(id-1)].speed + self.mspeed[l] #id[1..N],list[0,,N.1]
        mov = 0
        if tspeed != 0:
            seg = self.matrix[l][i+1: i+tspeed+1]
            for j in seg:
                if j != 0:
                    break
                else:
                    mov += 1
        return mov

    def update(self, r_in, r_out, t):
        # Updating of positions should take in account speed of walker and
        # speed of mechanical stair
        for l in range(len(self.mspeed)):    #For each lane
            # End position l
            if self.matrix[l, self.length - 1] != 0:
                if np.random.rand() <= Beta:
                    value = self.matrix[l, self.length - 1]
                    P[value - 1].to_reserve(r_out)
                    #r_out.append(value)
                    self.matrix[l, self.length - 1] = 0

            # Update middle
            for i in reversed(range(0, self.length - 1)):  #Middle of stair
                pmov = self.max_mov(l, i, self.matrix[l,i])
                if np.random.rand() <= p:
                    if pmov != 0:
                        self.matrix[l, i + pmov] = self.matrix[l, i]
                        self.matrix[l,i] = 0

    def feed(lista):
        # Fills the beginning positions, waitlist is only for mechanical stairs
        # The persons in the lista roll for waitlist or normal stairs.

        f = [] #Free mechanical stair indexes
        for f in range(len(self.mspeed)):
            if self.matrix[f,0] == 0:
                if self.wait_line != []:
                    self.matrix[f,0] = self.wait_line.pop(0)
                if (lista != 0) and (self.matrix[f,0] == 0):
                    self.matrix[f,0] lista.pop(0)

        for j in range(len(lista))
            if np.random.rand() < w:
                self.wait_line.append(per)
            else:
                for i in range(len(self.mspeed)):
                    if (self.mspeed[i] == 0) and (self.matrix[i,0] == 0):

# Variables
T = 40
alpha = 1
Beta = 1
p = 0.8
n_of_persons = 100
ts = 60

# Simulation
P = []      # List of persons
R_in = []
I = []      # Incoming people
O = []      # Outgoing people

# Add persons to person list
for i in reversed(range(1, n_of_persons)):
    P.append(person(i))
    R_in.append(i)

# Generate staircases and Reserves
S1 = staircase_set()
R0 = reserve(20, [], S1)
R0.platform(n_of_persons,4,1)   # Generate
R1 = reserve(20, S1, [])
F = []

# Update in time
for t in range(T):
    #S1.update(R_in, R1, t)
    R0.update()
    #I.append(len(R_in))
    #O.append(len(R1.current))

# Plotting
plt.figure()
plt.plot(F)
plt.title("Current starting algorithm")
plt.xlabel("Timesteps")
plt.ylabel("People in platform")
plt.show()
ST = []
E = []
C = []
Speed = []
for person in P:
    ST.append(person.start)
    E.append(person.end)
    Speed.append(person.speed)
    if S1.mspeed[person.lane] == 1:
        C.append('r')
    else:
        C.append('b')
ST = np.asarray(ST)
E = np.asarray(E)
T = E-ST

plt.close()
plt.suptitle("p ="+str(p))
plt.subplot(311)
plt.scatter(ST,T, c=C)
plt.xlabel("Time to door")
plt.ylabel("Travel time")
plt.subplot(312)
plt.plot(I, label = "In")
plt.plot(O, label = "Out")
plt.xlabel("Timestep")
plt.ylabel("Travel time")
plt.legend()
plt.subplot(313)
plt.scatter(T, Speed)
plt.xlabel("Travel Time")
plt.ylabel("Speed")
#plt.tight_layout()
plt.show()
# final-project-ptbravo
