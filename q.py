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

#qcount = 0
qnum = 0
qname = None
for n in l:
	if n[0]:
		q.add_edge(qnum, n[0])
		qname = n[0]
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

#	qcount += 1

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

def get_neighbors(thing):
	if thing.__class__ == list:
		for i in thing:
			print(get_neighbors(i))
	else:
		print(thing)

#nx.write_gml(q, 'CR.gml')
#window = tk.Tk()



def draw(graph):
	#viz = graphviz_layout(graph)
	nx.draw_networkx(graph, font_size=9)
	#nx.draw_spring(viz)
	#fig = Figure()
	#sub = fig.add_subplot(111)
	#sub.plot(viz)
	#canvas = FigureCanvasTkAgg(fig, master=window)
	#canvas.get_tk_widget().pack()
	#canvas.draw()
#draw(q)

#if __name__ == '__main__':
	#window.mainloop()
