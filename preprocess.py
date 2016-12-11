
def extract_graph(f_in, f_out, , end):
	with open(f_out, 'wb') as f:
		with open(f_in, 'rb') as fin:
			count = 0
			for line in fin:
				count += 1
				time = int(line.split()[-1])
				if time >= start and time <= end:
					f.write(line)

				if count % 10000 == 0:
					print "Line ", count

def sort_file(f_in, f_out):
	edges = []
	times = []
	with open(f_in, 'rb') as f:
		print "Start parsing..."
		for line in f:
			edges.append(line)
			times.append(int(line.split()[-1]))
		print "Start sorting..."
		idx = np.argsort(np.array(times))

	print 'Start writing....' 
	with open(f_out, 'wb') as fout:
		for i in idx:
			fout.write(edges[i])

if __name__ == '__main__':
	# start - 1369777559 - Tue, 28 May 2013 21:45:59 GMT
	# simulation start - 1385675159 - Thu, 28 Nov 2013 21:45:59 GMT
	# end - 1388267159 - Sat, 28 Dec 2013 21:45:59 GMT
	extract_graph('txedge.txt', 'txedge_6m.txt', 1369777559, 1385675159)
	sort_file('txedge_6m.txt', 'txedge_6m_sorted.txt')