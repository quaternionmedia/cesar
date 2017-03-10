import csv
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout
import json

#import tkinter as tk
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure


PATH = '/Users/harpo/Desktop/Cesar and Rubin/Audio & Video/Cesar and Ruben Qlab Oct-2011/'
f = open('CR.csv', 'r').readlines()
l = list(csv.reader(f, delimiter=','))

s = nx.MultiDiGraph()# sources
q = nx.MultiDiGraph()# queue graph

Q = 0

qnum = 0
qname = None
for n in l: # for every item in list
	if n[0]: # if it has a q number
		q.add_edge(qnum, n[0]) # connect qnum to qname
		qname = n[0] # needed to connect the next lines to this cue
		qnum += 1
	#if n[6] == 'auto-follow':

	if n[1].startswith('/'): # if it's a file
		n[1] = n[1].strip(PATH)
		if not s.has_node(n[1]): # if it's not in sources
			#print('adding node to source graph: ', n[1])
			s.add_node(n[1])
		#print('adding q: ', n[1]) # add source to q graph
		#q.add_node(n[1])
		q.add_edge(qname, n[2])
		q.add_edge(n[2], n[1])
	else: # if it's not a file, it's a pointer
		for i in l: # for each thing in list of sources
			if n[1] == i[0]+' '+i[2]: # if target == qnum + qname
				q.add_edge(qname, n[2]) # add an edge from the current q to it
				q.add_edge(n[2], i[1]) # add an edge from the name to the source
				break


qcount = 0
for i in range(111):
	q.add_edge(qcount, qcount+1)
	qcount += 1
#
# for i in range(100):
# 	n = get_neighbors(i)
# 	if n.
# 		for j in n:
# 			print(q.neig)
# 	else:
# 		print(n)

#nx.write_gml(q, 'CR.gml')
#window = tk.Tk()

def walk(graph):
	for i in nx.strongly_connected_components(q.q):
		print(i)

def cue(n):
	c, next = q.neighbors(n)
	graph = get_edges(c)

def get_edges(source, thing):
	graph = nx.MultiDiGraph()
	if thing.__class__ == int:
		graph.add_edge(thing, thing+1)
		graph.add_edge(thing, source.neighbors(thing)[0])
		graph = nx.compose(graph, get_edges(source, source.neighbors(thing)[0]))
	elif thing.__class__ == list:
		for i in thing:
			subthing = get_edges(source.out_edges(i), i)
			graph = nx.compose(graph, subthing)
			print('adding subthing: ', subthing)
	elif thing.__class__ == tuple:
		print('copying edge', thing)
		graph.add_edge(thing)
	elif thing.__class__ == str:
		for i in source.neighbors(thing):
			graph.add_edge(thing, i)
			print('adding edge from string', i)
		if source.neighbors(thing):
			for j in l: # for each thing in list of sources
				if i == j[0]+' '+j[2]: # if target == qnum + qname
					#graph = nx.compose(graph, get_edges(source, i))
					graph.add_edge(i, j[1])
					print('adding neighbors', source.edges(i))
					break
	print('adding thing: ', thing)
	return graph


def draw(graph):
	plt.clf()
	#viz = graphviz_layout(graph)
	labels = nx.draw_networkx_labels(graph, pos=nx.spring_layout(graph))
	nx.draw_networkx(graph, labels=labels, font_size=9)
	plt.draw()
	#nx.draw_spring(viz)
	#fig = Figure()
	#sub = fig.add_subplot(111)
	#sub.plot(viz)
	#canvas = FigureCanvasTkAgg(fig, master=window)
	#canvas.get_tk_widget().pack()
	#canvas.draw()

def show(num):
	cue = get_edges(q, num)
	draw(cue)
	#Q += 1
