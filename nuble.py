# IIQ 3763 Project - 2018-1
# Staircases and Mechanical Staircases, TASEP
# L6 to L5 Transfer at Nuble Station, Metro Santiago
# Pablo Bravo   ptbravo@uc.cl

import numpy as np
import argparse
import matplotlib.pyplot as plt
from scipy.stats import truncnorm

#Classes
class person():
    # 'Particles' that move on staircases
    # They can have different speeds
    def __init__(self, id, av_speed, type):
        self.speed = 0
        self.av_speed = av_speed
        self.lane = 0   # Lane on set
        self.id = id
        self.start = 0  # timestep in which they joined staircase
        self.end = 0    # timestep in which they finished staircase
        self.type = type    # Walker or stopper
        self.stype = 0      # Normal or mechanical stair

    def __str__(self):
        id = 'id: '+ str(self.id)
        av_speed = 'av_speed: ' + str(round(self.av_speed, 2))
        p_type = 'type: ' + str(self.type)
        return (id + '\t' + av_speed + '\t' + p_type)

    def to_reserve(self, reserve, t):
        # Move to reserve and update end time
        self.end = t
        reserve.current.append(self.id)

    def roll_speed(self):
        # Speed proxy
        if (self.type == 'S') and (self.stype == 'M'):
            self.speed = 0
        else:
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
    def __init__(self, id, length, IN, OUT, reserves = []):
        self.id = id
        self.IN = IN
        self.OUT = OUT
        self.reserves = reserves
        self.current = []
        self.positions = np.zeros(n_of_persons)
        self.positions += length
        self.flux = 0


    def update(self, t):
        # Move positions of current persons
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
        # Generate initial distribution
        for p in P:
            self.current.append(p.id)
        doors = list(np.arange(8)+1)
        D = []
        for p in self.current:
            dist = np.abs(4*np.random.choice(doors) - door_pos)
            D.append(dist)
        self.positions = np.asarray(D)

class staircase_set():
    def __init__(self, length, mspeed, id):
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
        if self.id==1:
            for index in lista:
                P[index-1].start = t

        # Fill Mechanical stairs
        for f in range(len(self.mspeed)):
            if (self.matrix[f,0] == 0) and (self.mspeed[f] == 1):
                if self.wait_line != []:
                    self.matrix[f,0] = self.wait_line.pop(0)
                    P[self.matrix[f,0] - 1].lane = f
                    P[self.matrix[f,0] - 1].stype = 'M'

                if (lista != []) and (self.matrix[f,0] == 0):
                    self.matrix[f,0] = lista.pop(0)
                    P[self.matrix[f,0] - 1].lane = f
                    P[self.matrix[f,0] - 1].stype = 'M'

        while lista != []:      # Iterate until we clear it
            roll = np.random.rand()
            if roll > w:
                cont = 1
                for l in range(len(self.mspeed)):
                    if cont == 1:
                        if (self.matrix[l,0] == 0) and (self.mspeed[l] == 0):
                            self.matrix[l,0] = lista.pop(0)
                            P[self.matrix[l,0] - 1].lane = l
                            P[self.matrix[l,0] - 1].stype = 'N'
                            cont = 0
                if cont == 1:
                    v = lista.pop(0)
                    self.wait_line.append(v)
            else:
                v = lista.pop(0)
                self.wait_line.append(v)

def generate_persons(N):
    # Generate persons
    P = []          # List of all the people in simulation
    person_type = []    # List of person types
    speed_distr = np.random.normal(1, 0.15, n_of_persons)
    for i in range(n_of_persons):
        roll = np.random.rand()
        if roll <= s:
            person_type.append('S')
        else:
            person_type.append('W')
    for i in reversed(range(1, n_of_persons)):
        P.append(person(i, speed_distr[i], person_type[i]))
    return P

""" MAIN MAIN MAIN MAIN """
# Argparse variables
parser = argparse.ArgumentParser()
parser.add_argument("N", help = "Number of persons", type = int)
#parser.add_argument("stair_length", help = "Steps of stair", type=int)
parser.add_argument("w", help = "Probability of going to waitline", type=float)
#parser.add_argument("s", help = "Probability of stopper", type = float)
args = parser.parse_args()

# Variables
alpha = 1
Beta = 1
p_move = 1
w = args.w
s = 0
#s = args.s
n_of_persons = args.N
#stair_length = args.stair_length
T = 300
iterations = 10

Starting_times = []
Ending_times = []

for iter in range(iterations):
    # Generate things for simulation
    P = generate_persons(n_of_persons)      # List of Persons

    # Things from Nuble station
    S1 = staircase_set(39, [1,1,0,0,0,0,0,0], 1)
    S2 = staircase_set(39, [1,1,0,0,0,0,1,1], 2)
    S3 = staircase_set(52, [1,1,0,0,0,0,0,0], 3)
    R0 = reserve(0, 20, [], S1)
    R1 = reserve(1, 20, S1, S2)
    R2 = reserve(2, 20, S2, S3)
    R3 = reserve(3, 20, S3, [])
    R0.platform(n_of_persons,4,1)   # Generate platform in starting reserve

    # Occupation holders
    s1 = np.zeros(T)
    s2 = np.zeros(T)
    s3 = np.zeros(T)
    r0 = np.zeros(T)
    r1 = np.zeros(T)
    r2 = np.zeros(T)
    r3 = np.zeros(T)

    # Update in time
    for t in range(T):
        # Get occupation data
        r0[t] = len(R0.current)
        r1[t] = len(R1.current)
        r2[t] = len(R2.current)
        r3[t] = len(R3.current)
        s1[t] = np.add(S1.walkers()[0], S1.walkers()[1])
        s2[t] = np.add(S2.walkers()[0], S2.walkers()[1])
        s3[t] = np.add(S3.walkers()[0], S3.walkers()[1])

        # Update simulation
        for persona in P:
            persona.roll_speed()
        S3.update(R2, R3, t)
        R2.update(t)
        S2.update(R1, R2, t)
        R1.update(t)
        S1.update(R0, R1, t)
        R0.update(t)

    # Get starting and finishing times
    for p in P:
        Starting_times.append(p.start)
        Ending_times.append(p.end)

# Transform into arrays for mathemathic operations
Starting_times = np.asarray(Starting_times)
Ending_times = np.asarray(Ending_times)

# Plotting
plt.figure()
plt.subplot(211)
plt.title('w: '+str(w)+'   N: '+str(n_of_persons))
plt.plot(r0, label = 'r0')
plt.plot(r1, label = 'r1')
plt.plot(r2, label = 'r2')
plt.plot(r3, label = 'r3')
plt.plot(s1, linewidth = 3, label = 's1')
plt.plot(s2, linewidth = 3, label = 's2')
plt.plot(s3, linewidth = 3, label = 's3')
plt.ylabel('N')
plt.xlabel('Timestep')
plt.legend()
plt.subplot(212)
plt.scatter(Starting_times, Ending_times - Starting_times, alpha = 0.3)
plt.xlabel('Time to door')
plt.ylabel('Travel time')
plt.tight_layout()
plt.show()
