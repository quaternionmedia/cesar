from __future__ import print_function
import networkx as nx
from tkinter import Tk, Frame, Label, Canvas
from IPython.core.magic import (Magics, magics_class, line_magic, cell_magic, line_cell_magic)

class Ion():
	def __init__(self):
		self.ion = nx.MultiDiGraph()
		self.ion.add_nodes_from(['parents', 'children', 'generators', 'children'])

	def printIon(self):
		for i in self.ion.nodes():
			print('Nodes: ', i)

	def showIon(self, window):
		global ionp, ionch, iong, ionf
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
		ionp.place(relx=0, rely=0, relheight=0.25, relwidth=1)
		ionp.bind('<Enter>', lambda e: ionp.config(bg='orchid'))
		ionp.bind('<Leave>', lambda e: ionp.config(bg='plum'))
		#parents
		# for pi, pe in enumerate(self.parents.nodes()):
		# 	pl = Label(ionp, text=pe, font=("Helvetica", 16))
		# 	plen = len(self.parents)
		# 	pl.place(relx=.5, rely=pi/plen)
		# 	print(pi,plen)

		#children canvas
		ionch = Canvas(canvas, bg='blue')
		ionch.place(relx=0, rely=0.25, relheight=0.25, relwidth=1)
		ionch.bind('<Enter>', lambda e: ionch.config(bg='blue'))
		ionch.bind('<Leave>', lambda e: ionch.config(bg='lightblue'))
		#children
		# for ci, ce in enumerate(self.children.nodes()):
		# 	cl = Label(ionch, text=ce, font=("Helvetica", 16))
		# 	clen = len(self.children)
		# 	cl.place(relx=.5, rely=ci/clen)
		# 	print(ci,clen)

		#generator canvas
		iong = Canvas(canvas, bg='lightgreen')
		iong.place(relx=0, rely=0.5, relheight=0.25, relwidth=1)
		iong.bind('<Enter>', lambda e: iong.config(bg='green'))
		iong.bind('<Leave>', lambda e: iong.config(bg='lightgreen'))
		#generators
		# for gi, ge in enumerate(self.generators.nodes()):
		# 	gl = Label(iong, text=ge, font=("Helvetica", 16))
		# 	glen = len(self.generators)
		# 	gl.place(relx=.5, rely=gi/glen)
		# 	print(gi,glen)

		#function canvas
		ionf = Canvas(canvas, bg='lavender')
		ionf.place(relx=0, rely=0.75, relheight=0.25, relwidth=1)
		ionf.bind('<Enter>', lambda e: ionf.config(bg='lavender'))
		ionf.bind('<Leave>', lambda e: ionf.config(bg='brown'))
		#functions
		# for fi, pe in enumerate(self.functions.nodes()):
		# 	fl = Label(ionf, text=pe, font=("Helvetica", 16))
		# 	flen = len(self.functions)
		# 	fl.place(relx=.5, rely=fi/flen)
		# 	print(fi,flen)

# The class MUST call this class decorator at creation time
@magics_class
class George(Magics):
	@line_magic
	def cesar(self, line):
		global g, show, control
		g = Ion()
		show = Tk()
		# g.addGenerator(show)
		# show.overrideredirect(1) #windowless
		# show.bind("<Escape>", lambda e: e.widget.quit())
		show.geometry('1280x650+0+0')
		show.config(bg='black')
		show.title('Show')
		show.state('zoomed')
		sdatas = Label(show, text='x:%s, y:%s' %( show.winfo_screenwidth(), show.winfo_screenheight()))
		# g.addChild(sdatas)
		control = Tk()
		# g.addGenerator(show)
		control.geometry('1280x720+0+720')
		control.config(bg='darkgrey')
		control.title('Control')
		def action(event):
			print('firing thing')
			i.client.send_message()
		control.bind('<space>', action)
		cdatas = Label(control, text='x:%s, y:%s' %( control.winfo_screenwidth(), control.winfo_screenheight()))
		# g.addChild(cdatas)
		sdatas.place(rely=.9,relx=.1)
		g.showIon(control)
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

	@line_magic
	def osc(self, line):
		import osc
		global i
		i = osc.Interface()
		#i.client.send_message('/go')
		return line

ip = get_ipython()
ip.register_magics(George)
