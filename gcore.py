from __future__ import print_function
import networkx as nx
from tkinter import Tk, Frame, Label, Canvas

class Ion():
	def __init__(self):
		self.parents = nx.MultiDiGraph()
		self.generators = nx.MultiDiGraph()
		self.children = nx.MultiDiGraph()
		self.functions = nx.MultiDiGraph()

	def printIon(self):
		for p in self.parents.nodes():
			print('Parent: ', p)
			for pn in p.nodes():
				print('nodes: ', pn)
		for g in self.generators.nodes():
			print(g)
			for gn in g.nodes():
				print('nodes: ', gn)
		for c in self.children.nodes():
			print(c)
			for cn in c.nodes():
				print('nodes: ', cn)
		for f in self.functions.nodes():
			print(f)
			for fn in f.nodes():
				print('nodes: ', fn)

	#
	# def showIon(self, window):
	#
	# 	canvas = Canvas(window, bg='black')
	# 	canvas.pack(fill='both')
	#
	# 	#ion frame
	# 	ionf = Frame(canvas, bg='grey', borderwidth=2, takefocus=True)
	# 	ionf.pack()
	# 	#parent frame
	# 	ionp = Frame(ionf, bg='red', borderwidth=1)
	# 	for p in self.parents:
	# 		pl = Label(ionp, text='p')
	# 		for pn in p.nodes():
	# 			pnl = Label(ionp, text='pn')
	# 	#generator frame
	# 	iong = Frame(ionf, bg='green', borderwidth=1)
	# 	#children frame
	# 	iong = Frame(ionf, bg='blue', borderwidth=1)
	# 	#function frame
	# 	ionf = Frame(ionf, bg='white', borderwidth=1)
	#
	# 	canvas.pack()

	def addParent(self, name, *args, **kwargs):
		i = nx.MultiDiGraph()
		i.add_node(name)
		i.add_nodes_from(args)
		i.add_edges_from(kwargs)
		self.parents.add_node(i)

	def addGenerator(self, name, *args, **kwargs):
		i = nx.MultiDiGraph()
		i.add_node(name)
		i.add_nodes_from(args)
		i.add_edges_from(kwargs)
		self.generators.add_node(i)

	def addChild(self, name, *args, **kwargs):
		i = nx.MultiDiGraph()
		i.add_node(name)
		i.add_nodes_from(args)
		i.add_edges_from(kwargs)
		self.children.add_node(i)

	def addFunction(self, name, *args, **kwargs):
		i = nx.MultiDiGraph()
		i.add_node(name)
		i.add_nodes_from(args)
		i.add_edges_from(kwargs)
		self.functions.add_node(i)

	def test(self):
		self.addParent('Parent')
		self.addGenerator('Generator')
		self.addChild('Child')
		self.addFunction('Function')
		self.printIon()




from IPython.core.magic import (Magics, magics_class, line_magic, cell_magic, line_cell_magic)

# The class MUST call this class decorator at creation time
@magics_class
class George(Magics):

	@line_magic
	def guitest(self, line):
		ion = Ion()
		w = Tk()
		ion.showIon(w)
		return line

	@line_magic
	def lmagic(self, line):
		"my line magic"
		print("Full access to the main IPython object:", self.shell)
		print("Variables in the user namespace:", list(self.shell.user_ns.keys()))
		return line

	@cell_magic
	def cmagic(self, line, cell):
		"my cell magic"
		return line, cell

	@line_cell_magic
	def lcmagic(self, line, cell=None):
		"Magic that works both as %lcmagic and as %%lcmagic"
		if cell is None:
			print("Called as line magic")
			return line
		else:
			print("Called as cell magic")
			return line, cell


# In order to actually use these magics, you must register them with a
# running IPython.  This code must be placed in a file that is loaded once
# IPython is up and running:
ip = get_ipython()
# You can register the class itself without instantiating it.  IPython will
# call the default constructor on it.
ip.register_magics(George)
