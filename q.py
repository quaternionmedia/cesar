import csv
import networkx as nx

f = open('CR.csv', 'r').readlines()
l = list(csv.reader(f, delimiter=','))
q = nx.MultiDiGraph()
s = nx.MultiDiGraph()


active = []
qnum = 0
for n in l:
	if n[1].startswith('/'):
		if not s.has_node(n[1]):
			s.add_node(n[1])
		q.add_node(s.node[n[1]])
		active.append(n[0]+' '+n[2])
	else:
		for i in l:
			if n[1] == i[0]+' '+i[2]:
				q.add_edge(i[1], qnum)

	qnum += 1
