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
			# for pn in p.nodes():
			# 	print('nodes: ', pn)
		for g in self.generators.nodes():
			print(g)
			# for gn in g.nodes():
			# 	print('nodes: ', gn)
		for c in self.children.nodes():
			print(c)
			# for cn in c.nodes():
			# 	print('nodes: ', cn)
		for f in self.functions.nodes():
			print(f)
			# for fn in f.nodes():
			# 	print('nodes: ', fn)






	def addParent(self, name, *args, **kwargs):
		i = self.parents
		i.add_node(name)
		i.add_nodes_from(args)
		i.add_edges_from(kwargs)
		self.parents.add_node(i)

	def addGenerator(self, name, *args, **kwargs):
		i = self.generators
		i.add_node(name)
		i.add_nodes_from(args)
		i.add_edges_from(kwargs)
		self.generators.add_node(i)

	def addChild(self, name, *args, **kwargs):
		i = self.children
		i.add_node(name)
		i.add_nodes_from(args)
		i.add_edges_from(kwargs)
		self.children.add_node(i)

	def addFunction(self, name, *args, **kwargs):
		i = self.functions
		i.add_node(name)
		i.add_nodes_from(args)
		i.add_edges_from(kwargs)
		self.functions.add_node(i)


	def showIon(self, window):
		#ion canvas
		canvas = Canvas(window, bg='grey', takefocus=True)
		def drag(event):
			newx = event.x/2
			newy = event.y/2
			canvas.place(x=newx,y=newy)#, anchor='center')
			print(event, newx, newy)



		canvas.bind('<Enter>', lambda e: canvas.config(bg='dimgrey'))
		canvas.bind('<Leave>', lambda e: canvas.config(bg='grey'))
		canvas.bind('<B1-Motion>', drag)
		canvas.place(relx=0.5, rely=0.5, relheight=1, relwidth=1, anchor='center')

		#parent canvas
		ionp = Canvas(canvas, bg='plum')
		ionp.place(relx=0.5, rely=.25, relheight=0.1, relwidth=0.25, anchor='n')
		ionp.bind('<Enter>', lambda e: ionp.config(bg='orchid'))
		ionp.bind('<Leave>', lambda e: ionp.config(bg='plum'))
		#parents
		for pi, pe in enumerate(self.parents.nodes()):
			pl = Label(ionp, text=pe, font=("Helvetica", 6))
			plen = len(self.parents)
			pl.place(relx=.5, rely=pi/plen)
			print(pi,plen)


		#children canvas
		ionch = Canvas(canvas, bg='blue')
		ionch.place(relx=0.5, rely=.75, relheight=0.1, relwidth=0.25, anchor='s')
		ionch.bind('<Enter>', lambda e: ionch.config(bg='lightblue'))
		ionch.bind('<Leave>', lambda e: ionch.config(bg='blue'))
		#children
		for ci, ce in enumerate(self.children.nodes()):
			cl = Label(ionch, text=ce, font=("Helvetica", 6))
			clen = len(self.children)
			cl.place(relx=.5, rely=ci/clen)
			print(ci,clen)



		#generator canvas
		iong = Canvas(canvas, bg='lightgreen')
		iong.place(relx=.25, rely=.5, relheight=0.25, relwidth=0.1, anchor='w')
		iong.bind('<Enter>', lambda e: iong.config(bg='green'))
		iong.bind('<Leave>', lambda e: iong.config(bg='lightgreen'))
		#generators
		for gi, ge in enumerate(self.generators.nodes()):
			gl = Label(iong, text=ge, font=("Helvetica", 6))
			glen = len(self.generators)
			gl.place(relx=.5, rely=gi/glen)
			print(gi,glen)

		#function canvas
		ionf = Canvas(canvas, bg='lavender')
		ionf.place(relx=.75, rely=.5, relheight=0.25, relwidth=0.1, anchor='e')
		ionf.bind('<Enter>', lambda e: ionf.config(bg='brown'))
		ionf.bind('<Leave>', lambda e: ionf.config(bg='lavender'))
		#functions
		for fi, pe in enumerate(self.functions.nodes()):
			fl = Label(ionf, text=pe, font=("Helvetica", 6))
			flen = len(self.functions)
			fl.place(relx=.5, rely=fi/flen)
			print(fi,flen)


	def test(self, window):
		# self.addParent('Parent')
		# self.addGenerator('Generator')
		# self.addChild('Child')
		# self.addFunction('Function')
		self.printIon()
		self.showIon(window)




from IPython.core.magic import (Magics, magics_class, line_magic, cell_magic, line_cell_magic)

# The class MUST call this class decorator at creation time
@magics_class
class George(Magics):

	@line_magic
	def cesar(self, line):
		global g, show, control
		g = Ion()



		show = Tk()
		g.addGenerator(show)
		# show.overrideredirect(1) #windowless
		# show.bind("<Escape>", lambda e: e.widget.quit())
		show.geometry('920x600+-1875+50')
		show.config(bg='black')
		show.title('Show')
		show.state('zoomed')
		sdatas = Label(show, text='x:%s, y:%s' %( show.winfo_screenwidth(), show.winfo_screenheight()))
		g.addChild(sdatas)


		control = Tk()
		g.addGenerator(show)

		control.geometry('800x600+0+0')
		control.config(bg='darkgrey')
		control.title('Control')
		cdatas = Label(control, text='x:%s, y:%s' %( control.winfo_screenwidth(), control.winfo_screenheight()))
		g.addChild(cdatas)

		sdatas.place(rely=.9,relx=.1)

		g.test(control)

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
