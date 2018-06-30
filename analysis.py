# IIQ 3763 Project - 2018-1
# Staircases and Mechanical Staircases, TASEP
# Post simulation script fpr parameter dependence
# Pablo Bravo   ptbravo@uc.cl

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter

# Generate empty variables to fill
n = [0]*11
N_start = []
for i in range(11):
    N_start.append(n)
N_end = N_start
M_start = N_start
M_end = N_start
n_f10 = np.zeros([11,11])
m_f10 = np.zeros([11,11])
n_all = np.zeros([11,11])
m_all = np.zeros([11,11])
n_l10 = np.zeros([11,11])
m_l10 = np.zeros([11,11])
T = np.zeros([11,11])

# Load data from .npz
for file_name in os.listdir('./data'):
    data = np.load('./data/'+file_name) # Load .npz
    l = data['arr_0'][0]
    w = data['arr_0'][1]
    i = int((l/10) - 1)                 # index 1
    j = int(10*w)                       # index 2

    # Temporal arrays before sorting
    n_start = data['arr_1'][0]
    n_end = data['arr_1'][1]
    m_start = data['arr_2'][0]
    m_end = data['arr_2'][1]

    # Sorting
    idx = n_start.argsort()
    idy = m_start.argsort()
    n_start = n_start[idx]
    n_end = n_end[idx]
    m_start = m_start[idy]
    m_end = m_end[idy]
    n_travel = (n_end-n_start)#/l
    m_travel = (m_end-m_start)#/l

    # Add to matrices
    n_all[i,j] = np.mean(n_travel)
    m_all[i,j] = np.mean(m_travel)


# Plotting
fig = plt.figure()
ax = fig.gca(projection='3d')
plt.title('N = 100')
ax.set_ylabel('Length')
ax.set_xlabel('w')
ax.set_zlabel('Average travel time')
ypos = np.arange(10,120,10)
xpos = np.arange(0,1.1,0.1)
xpos, ypos = np.meshgrid(xpos,ypos)
surf1 = ax.plot_surface(xpos, ypos, m_all, alpha = 0.7,
                       linewidth=0, antialiased=False)
surf2 = ax.plot_surface(xpos, ypos, n_all, alpha = 0.7,
                       linewidth=0, antialiased=False)
fake2Dline1 = mpl.lines.Line2D([0],[0], c='blue')   # For legend
fake2Dline2 = mpl.lines.Line2D([0],[0], c='orange') # For legend
ax.legend([fake2Dline1, fake2Dline2], ['Mechanical', 'Normal'], numpoints = 1)
plt.show()
