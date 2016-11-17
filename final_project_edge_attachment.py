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

tx_dst_num_dis = collections.defaultdict(int)
tx_src_num_dis = collections.defaultdict(int)
tx_src_dst_pair_num_dis = collections.defaultdict(int)
existing_nodes = Set()

edge_count = 0
transaction_count = 0

previousTransactionID = -1
senders = Set()
receivers = Set()

old_old_edge_count = 0
old_new_edge_count = 0
new_old_edge_count = 0
new_new_edge_count = 0

f = open('txedge.txt', 'r')
for line in f:
	edge_count += 1
	if edge_count % 1000000 == 0: print edge_count
	
	row = line.split()
	txID = int(row[0])
	sender = int(row[1])
	receiver = int(row[2])
	time = int(row[3])
	
	if previousTransactionID == -1:
		transaction_count += 1
		previousTransactionID = txID
	elif txID != previousTransactionID:
		transaction_count += 1
		
		# see how many senders and receivers are involved
		tx_dst_num_dis[len(receivers)] += 1
		tx_src_num_dis[len(senders)] += 1
		tx_src_dst_pair_num_dis[(len(senders), len(receivers))] += 1
		
		# compute how many new senders and new receivers
		new_src = 0
		new_dst = 0
		for source_node in senders:
			if source_node not in existing_nodes:
				new_src += 1
		old_src = len(senders) - new_src
		for dst_node in receivers:
			if dst_node not in existing_nodes:
				new_dst += 1
		old_dst = len(receivers) - new_dst
		
		old_old_edge_count += old_src*old_dst
		old_new_edge_count += old_src*new_dst
		new_old_edge_count += new_src*old_dst
		new_new_edge_count += new_src*new_dst
		
		# add to existing nodes
		for source_node in senders:
			existing_nodes.add(source_node)
		for dst_node in receivers:
			existing_nodes.add(dst_node)
			
		# reset
		previousTransactionID = txID
		senders = Set()
		receivers = Set()
	senders.add(sender)
	receivers.add(receiver)

# see how many senders and receivers are involved
tx_dst_num_dis[len(receivers)] += 1
tx_src_num_dis[len(senders)] += 1
tx_src_dst_pair_num_dis[(len(senders), len(receivers))] += 1

# compute how many new senders and new receivers
new_src = 0
new_dst = 0
for source_node in senders:
	if source_node not in existing_nodes:
		new_src += 1
old_src = len(senders) - new_src
for dst_node in receivers:
	if dst_node not in existing_nodes:
		new_dst += 1
old_dst = len(receivers) - new_dst

old_old_edge_count += old_src*old_dst
old_new_edge_count += old_src*new_dst
new_old_edge_count += new_src*old_dst
new_new_edge_count += new_src*new_dst

print "destination number distribution", tx_dst_num_dis
print "source number distribution", tx_src_num_dis
print "source/destination number pair distribution", tx_src_dst_pair_num_dis
print "edges", edge_count
print "transactions", transaction_count

print old_old_edge_count
print old_new_edge_count
print new_old_edge_count
print new_new_edge_count


# keylist = outdegree_dis.keys()
# keylist.sort()
# degrees = [x for x in keylist]
# values = [outdegree_dis[x] for x in keylist]
# plt.loglog(degrees, values, 'g')
# plt.title('Outdegree Distribution')
# plt.xlabel('Node degree')
# plt.ylabel('Node degree proportion')
# plt.show()
	