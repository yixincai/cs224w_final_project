from snap import *
from copy import deepcopy
import numpy as np
import matplotlib.pyplot as plt
import json

def edge_deg_dist(fname, start=1372455959, step=2635200, max_iter=5, is_in=True):
	# 1372455959 06/28/2013
	# 1388267159 12/28/2013
	# start = 1385675159
	# step = 2635200
	G = TNGraph().New()
	G_old = None
	count = 0
	deg_count = {}
	edge_deg_count = {}
	with open(fname, 'r') as f:

		end = start + step
		for line in f:
			[txID, addrin, addrout, txtime] = [int(x) for x in line.split()]
			if txtime < start:
					continue
			if txtime > end:
				print 'iteration', 5-max_iter
				if G_old:
					if is_in:
						compute_deg_dist(G_old, G, deg_count, edge_deg_count)
					else:
						compute_out_deg_dist(G_old, G, deg_count, edge_deg_count)
				end += step
				max_iter -= 1
				if max_iter <= 0: # finished
					break
				G_old = copy_graph(G)


			user1 = addrin
			user2 = addrout
			if user1 == user2:
				continue
			if user1 and not G.IsNode(user1):
				G.AddNode(user1)
			if user2 and not G.IsNode(user2):
				G.AddNode(user2)
			if not G.IsEdge(user1, user2):
				G.AddEdge(user1, user2)

			count += 1
			if count % 10000 == 0:
				print "Parsing edges at ", count, " line"

	deg_plot(deg_count, edge_deg_count)

def compute_deg_dist(G_old, G_new, deg_count, edge_deg_count):
	size = 1000
	for node in G_old.Nodes():
		nid = node.GetId()
		deg = node.GetInDeg()
		deg_new = G_new.GetNI(nid).GetInDeg()
		if deg < size and deg > 0:
			deg_count[deg] = deg_count[deg] + 1 if deg_count.has_key(deg) else 1
			if edge_deg_count.has_key(deg):
				edge_deg_count[deg] += deg_new - deg
			else:
				edge_deg_count[deg] = deg_new - deg


def compute_out_deg_dist(G_old, G_new, deg_count, edge_deg_count):
	size = 1000
	for node in G_old.Nodes():
		nid = node.GetId()
		deg = node.GetOutDeg()
		deg_new = G_new.GetNI(nid).GetOutDeg()
		if deg < size and deg > 0:
			deg_count[deg] = deg_count[deg] + 1 if deg_count.has_key(deg) else 1
			if edge_deg_count.has_key(deg):
				edge_deg_count[deg] += deg_new - deg
			else:
				edge_deg_count[deg] = deg_new - deg

def copy_graph(G_old):
	G = TNGraph().New()
	for node in G_old.Nodes():
		G.AddNode(node.GetId())

	for edge in G_old.Edges():
		src, dest = edge.GetId()
		G.AddEdge(src, dest)

	return G

def deg_plot(deg_count, edge_deg_count):
	with open('out.json', 'wb') as f:
		f.write(json.dumps(deg_count)+'\n')
		f.write(json.dumps(edge_deg_count)+'\n')

	X = []
	nom = []
	denom = []
	for key in edge_deg_count:
		X.append(key)
		nom.append(edge_deg_count[key])
		denom.append(deg_count[key])

	X = np.array(X)
	Y = np.divide(np.array(nom), np.array(denom)*1.0)
	mask = np.nonzero(Y)[0]

	if len(mask) <= 0:
		print 'Failed! All degrees have 0 counts'
		return
	plt.plot(X[mask], Y[mask], 'o', color='r')
	plt.xscale("log")
	plt.yscale("log")
	plt.title('Bitcoin network')
	plt.xlabel('Destination node degree, d')
	plt.ylabel('Edge probability, p(d)')
	plt.show()

def plot_json():
	with open('out1.json', 'rb') as f:
		lines = [line for line in f]
	deg_count = json.loads(lines[0])
	edge_deg_count = json.loads(lines[1])

	X = []
	nom = []
	denom = []
	for key in edge_deg_count:
		X.append(int(key))
		nom.append(int(edge_deg_count[key]))
		denom.append(int(deg_count[key]))

	print 'Start plotting..'
	X = np.array(X)
	Y = np.divide(np.array(nom), np.array(denom)*1.0)
	Y = np.divide(Y, np.sum(Y))

	mask = np.nonzero(Y)[0]
	if len(mask) <= 0:
		print 'Failed! All degrees have 0 counts'
		return
	print denom
	plt.plot(X[mask], Y[mask], 'o', color='r')
	plt.xscale("log")
	plt.yscale("log")
	plt.title('Bitcoin Network')
	plt.xlabel('Destination node degree, d')
	plt.ylabel('Edge probability, p(d)')
	plt.show()

if __name__ == '__main__':
	# edge_deg_dist("txedge_10000_sorted.txt", start=1372377601, step=(1376517848-1372377601)/5, max_iter=5)
	edge_deg_dist("txedge_6m_sorted.txt")
	# plot_json()
	









