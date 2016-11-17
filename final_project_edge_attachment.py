from snap import *
from math import *
import numpy as np
import scipy
import scipy.stats
import random
import collections
import matplotlib.pyplot as plt
from sets import Set
import copy
import operator

transaction


f = open('degree.txt', 'r')

count = 0
previousTransactionID = -1
for line in f:
	count += 1
	if count % 100000 == 0: print count
	row = line.split()
	in_degree = int(row[1])
	out_degree = int(row[2])
	indegree_dis[in_degree] += 1
	outdegree_dis[out_degree] += 1
	
keylist = indegree_dis.keys()
keylist.sort()
degrees = [x for x in keylist]
values = [indegree_dis[x] for x in keylist]
plt.plot(degrees, values, 'b')
ax.set_yscale('log')
plt.title('Indegree Distribution')
plt.xlabel('Node degree')
plt.ylabel('Node degree proportion')
plt.show()

keylist = outdegree_dis.keys()
keylist.sort()
degrees = [x for x in keylist]
values = [outdegree_dis[x] for x in keylist]
plt.loglog(degrees, values, 'g')
plt.title('Outdegree Distribution')
plt.xlabel('Node degree')
plt.ylabel('Node degree proportion')
plt.show()
	