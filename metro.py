# IIQ 3763 Project - 2018-1
# Staircases and Mechanical Staircases, TASEP
# Pablo Bravo   ptbravo@uc.cl

import numpy as np
import argparse
import matplotlib.pyplot as plt
from scipy.stats import truncnorm

#Classes
class person():
    # 'Particles' that move on staircases
    # They can have different speeds
    def __init__(self, id, av_speed):
        self.speed = 0
        self.av_speed = av_speed
        self.set = 0    # Set of staircases
        self.lane = 0   # Lane on set
        self.type = 0   # Normal or mechanical walker
        self.pos = 0    # Position on lane
        self.id = id
        self.start = 0  # timestep in which they joined staircase
        self.end = 0    # timestep in which they finished staircase
        self.type = np.random.choice(['A', 'B'])

    def to_reserve(self, reserve, t):
        self.end = t
        reserve.current.append(self.id)

    def roll_speed(self):
        delta = self.av_speed - 1
        roll = np.random.rand()
        if delta <= 0:
            if roll <= np.abs(delta):
                self.speed = 0
            else:
                self.speed = 1
        if delta > 0:
            if roll <= np.abs(delta):
                self.speed = 2
            else:
                self.speed = 1

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


    def update(self, t):
        temporal = []
        for index in self.current:
            self.positions[index - 1] -= P[index - 1].speed
        for index in self.current:
            if self.positions[index - 1] <= 0:
                temporal.append(index)
                self.current.remove(index)
                self.positions[index - 1] = 0
        self.flux += len(temporal)
        self.OUT.feed(temporal, t)

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
    def __init__(self, length = 40, id = 1, mspeed = [1,1,0,0,0,0]):
        self.length = length
        self.mspeed = np.asarray(mspeed)    # Mechanical staircase speed
        self.matrix = np.zeros([len(self.mspeed), self.length], int)
        self.id = id
        self.wait_line = []


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
                    P[value - 1].to_reserve(r_out, t)
                    self.matrix[l, self.length - 1] = 0

            # Update middle
            for i in reversed(range(0, self.length - 1)):  #Middle of stair
                pmov = self.max_mov(l, i, self.matrix[l,i])
                if np.random.rand() <= p_move:
                    if pmov != 0:
                        self.matrix[l, i + pmov] = self.matrix[l, i]
                        self.matrix[l,i] = 0

    def walkers(self):
        # Types of walkers in staircase_set()
        n = 0
        m = 0
        for i in range(len(self.mspeed)):
            for j in range(self.length):
                if self.mspeed[i] == 1:
                    if self.matrix[i,j] != 0:
                        m += 1
                if self.mspeed[i] == 0:
                    if self.matrix[i,j] != 0:
                        n += 1
        return n,m

    def feed(self, lista, t):
        # Fills the beginning positions, waitlist is only for mechanical stairs
        # The persons in the lista roll for waitlist or normal stairs.
        for index in lista:
            P[index-1].start = t

        # Fill Mechanical stairs
        for f in range(len(self.mspeed)):
            if (self.matrix[f,0] == 0) and (self.mspeed[f] == 1):
                if self.wait_line != []:
                    self.matrix[f,0] = self.wait_line.pop(0)
                    P[self.matrix[f,0] - 1].lane = f
                    P[self.matrix[f,0] - 1].type = 'M'

                if (lista != []) and (self.matrix[f,0] == 0):
                    self.matrix[f,0] = lista.pop(0)
                    P[self.matrix[f,0] - 1].lane = f
                    P[self.matrix[f,0] - 1].lane = 'M'

        while lista != []:      # Iterate until we clear it
            roll = np.random.rand()
            if roll > w:
                cont = 1
                for l in range(len(self.mspeed)):
                    if cont == 1:
                        if (self.matrix[l,0] == 0) and (self.mspeed[l] == 0):
                            self.matrix[l,0] = lista.pop(0)
                            P[self.matrix[l,0] - 1].lane = l
                            P[self.matrix[l,0] - 1].type = 'N'
                            cont = 0
                if cont == 1:
                    v = lista.pop(0)
                    self.wait_line.append(v)
            else:
                v = lista.pop(0)
                self.wait_line.append(v)

""" MAIN MAIN MAIN MAIN """
# Argparse variables
parser = argparse.ArgumentParser()
parser.add_argument("N", help = "Number of persons", type=int)
parser.add_argument("w", help = "Probability of going to wait_line", type=float)
#parser.add_argument("s", help = "Probability of stopper on mechanical stair")
args = parser.parse_args()

# Variables
T = 300
alpha = 1
Beta = 1
p_move = 1
w = args.w   # w = 0 is all wait
n_of_persons = args.N
stair_length = 50
iterations = 10

Starting_times = np.zeros([iterations, n_of_persons])
Ending_times = np.zeros([iterations, n_of_persons])
Mech_start = []
Mech_end = []
Norm_start = []
Norm_end = []

for iter in range(iterations):
    # Script Variables
    P = []          # List of all the people in simulation

    # Generate speed distrubution as in walking speed paper
    speed_distr = np.random.normal(1.32, 0.15, n_of_persons)

    # Add persons to person list
    for i in reversed(range(1, n_of_persons)):
        P.append(person(i, speed_distr[i]))

    # Generate staircases and Reserves
    S1 = staircase_set(stair_length)
    R0 = reserve(20, [], S1)
    R0.platform(n_of_persons,4,1)   # Generate platform in starting reserve
    R1 = reserve(20, S1, [])

    # Update in time
    for t in range(T):
        # Update simulation
        for persona in P:
            persona.roll_speed()
        S1.update(R0, R1, t)
        R0.update(t)

    # Get starting and finishing times
    for p in P:
        Starting_times[iter, p.id-1] = p.start
        Ending_times[iter, p.id-1] = p.end
        if p.type == 'N':
            Norm_start.append(p.start)
            Norm_end.append(p.end)
        if p.type == 'M':
            Mech_start.append(p.start)
            Mech_end.append(p.end)

# To arrays
Norm_start = np.asarray(Norm_start)
Norm_end = np.asarray(Norm_end)
Mech_start = np.asarray(Mech_start)
Mech_end = np.asarray(Mech_end)

plt.figure()
plt.scatter(Norm_start, Norm_end - Norm_start, label = "Normal")
plt.scatter(Mech_start, Mech_end - Mech_start, label = "Mech")
plt.legend()
plt.xlabel("Time to door")
plt.ylabel("Travel time")
plt.show()
