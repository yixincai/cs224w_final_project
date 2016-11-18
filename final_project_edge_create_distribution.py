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

monthly_transaction = collections.defaultdict(int)
f = open('txtime.txt', 'r')
start_time = 1230768000
year_seconds = 31536000
year_seconds_2012 = 31622400

monthly_seconds = [2678400, 2419200, 2678400, 2592000, 2678400, 2592000, 2678400, 2678400, 2592000, 2678400, 2592000, 2678400]
monthly_seconds_2012 = [2678400, 2505600, 2678400, 2592000, 2678400, 2592000, 2678400, 2678400, 2592000, 2678400, 2592000, 2678400]
average_month_seconds = 2628000

count = 0
for line in f:
	count += 1
	if count % 100000 == 0: print count
	
	row = line.split()
	time = int(row[1])
	month = (time - start_time) / 2628000
	monthly_transaction[month] += 1
	
keylist = monthly_transaction.keys()
keylist.sort()
months = [x for x in keylist]
values = [monthly_transaction[x] for x in keylist]
plt.plot(months, values, 'b')
plt.title('Monthly transaction')
plt.xlabel('Month')
plt.ylabel('Monthly Transactions')
plt.show()

plt.plot(months, values, 'b')
plt.yscale('log')
plt.title('Monthly transaction log scale')
plt.xlabel('Month')
plt.ylabel('Monthly Transactions')
plt.show()

input = [x for x in keylist]
y = [log(monthly_transaction[x]) for x in keylist]
A = np.vstack([input, np.ones(len(input))]).T

print np.linalg.lstsq(A, y)