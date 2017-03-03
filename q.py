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



f = open('CR.csv', 'r').readlines()
l = list(csv.reader(f, delimiter=','))

s = nx.MultiDiGraph()# sources
q = nx.MultiDiGraph()# queue graph

qcount = 0
for n in l:
	if n[1].startswith('/'): # if it's a file
		if not s.has_node(n[1]): # if it's not in sources
			print('adding node: ', n[1])
			s.add_node(n[1])
		print('adding q: ', n[1]) # add source name to q graph
		q.add_node(n[1])
	else: # if it's not a file, it's a pointer
		for i in l: # for each thing in list of sources
			if n[1] == i[0]+' '+i[2]: # if target == qnum + qname
				q.add_edge(i[1], str(qcount)) # add an edge from it to the current q number

	qcount += 1

#with open('CR.gml', 'w') as w:
#	w.writelines()

nx.write_gml(q, 'CR.gml')

#window = tk.Tk()

def draw(graph):
	#viz = graphviz_layout(graph)
	nx.draw_networkx(graph, font_size=6)
	#nx.draw_spring(viz)
	#fig = Figure()
	#sub = fig.add_subplot(111)
	#sub.plot(viz)
	#canvas = FigureCanvasTkAgg(fig, master=window)
	#canvas.get_tk_widget().pack()
	#canvas.draw()
q.add_edges_from(enumerate(range(370)))
#draw(q)

#if __name__ == '__main__':
	#window.mainloop()
