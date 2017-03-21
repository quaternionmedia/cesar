from __future__ import print_function
import networkx as nx
from tkinter import Tk, Frame, Label, Canvas
import matplotlib
matplotlib.use("TkAgg") # Extremely important. Don't know why. Do not move.
from matplotlib import pyplot as plt
from multiprocessing import Process

import kerbal

class Ion():
	def __init__(self):
		self.ion = nx.MultiDiGraph()

	def printIon(self):
		for i in self.ion.nodes():
			print(i)

	def showIon(self, window):
		global ionp, ionch, iong, ionf, canvas
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
		ionp = Label(control, bg='plum')
		ionp.place(relx=0.5, rely=0, relheight=0.1, relwidth=0.1)
		ionp.bind('<Enter>', lambda e: ionp.config(bg='orchid'))
		ionp.bind('<Leave>', lambda e: ionp.config(bg='plum'))
		#children canvas
		ionch = Canvas(canvas, bg='blue')
		ionch.place(relx=0.5, rely=1, relheight=0.1, relwidth=0.1)
		ionch.bind('<Enter>', lambda e: ionch.config(bg='lightblue'))
		ionch.bind('<Leave>', lambda e: ionch.config(bg='blue'))
		#generator canvas
		iong = Canvas(canvas, bg='lightgreen')
		iong.place(relx=0, rely=.5, relheight=0.1, relwidth=0.1)
		iong.bind('<Enter>', lambda e: iong.config(bg='green'))
		iong.bind('<Leave>', lambda e: iong.config(bg='lightgreen'))
		#function canvas
		ionf = Canvas(canvas, bg='lavender')
		ionf.place(relx=1, rely=.5, relheight=0.1, relwidth=0.1)
		ionf.bind('<Enter>', lambda e: ionf.config(bg='brown'))
		ionf.bind('<Leave>', lambda e: ionf.config(bg='lavender'))

from IPython.core.magic import (Magics, magics_class, line_magic, cell_magic, line_cell_magic)

def resize(event):
	w,h = event.width, event.height
	#show.config(width=w, height=h)
	v.width, v.height = w, h
	v.buffer = []
	print('resizing to ', w, h)


def task(thing, *args):
	t = Process(target=thing, args=args)
	return t


def waitForQ():
	#t = task(q.server.wait_for_message)
	#t.start()
	#return t
	while True:
		q.server.wait_for_message()
		#(clientsocket, address) = q.server.sock.accept()
		#print('socket connected', clientsocket, address)
		if q.server.messages[-1] is not None:
			try:
				exec(q.server.oscParse(q.server.messages[-1]), globals())
			except Exception as e:
				print('osc exec error: ', e, q.server.oscParse(q.server.messages[-1]))


# def

# The class MUST call this class decorator at creation time
@magics_class
class George(Magics):

	@line_magic
	def cesar(self, line):
		global g, show, control, q, v, s, l
		g = Ion()
		from video import Video
		from cr import Qlab, Sound, Lights
		#import osc
		show = Tk()
		#label = Label(show)
		#label.place(x=0,y=5,relheight=1,relwidth=1)
		q = Qlab()
		q.send('/version')
		v = Video('/Users/harpo/Movies/Proclaim2016 Tom edit.mp4')
		try:
			s = Sound()
		except:
			print('no sound module available')

		#l = Lights()

		c = Canvas(show)
		c.place(x=0,y=5,relheight=1,relwidth=1)
		v.assignWindow(c)

		c.bind('<Configure>', resize)

		#g.addGenerator(show)
		# show.overrideredirect(1) #windowless
		# show.bind("<Escape>", lambda e: e.widget.quit())
		show.geometry('600x400+0+0')
		# show.config(bg='black')
		show.title('Show')
		# show.state('zoomed')
		sdatas = Label(show, text='x:%s, y:%s' %( show.winfo_screenwidth(), show.winfo_screenheight()))
		#g.addChild(sdatas)


		control = Tk()
		#g.addGenerator(show)

		control.geometry('320x240+0+0')
		control.config(bg='darkgrey')
		control.title('Control')
		def action(event):
			print('firing thing')
			q.go()
		control.bind('<space>', action)
		cdatas = Label(control, text='x:%s, y:%s' %( control.winfo_screenwidth(), control.winfo_screenheight()))
		#g.addChild(cdatas)

		sdatas.place(rely=.9,relx=.1)

		g.showIon(control)
		v.play()


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

	@line_cell_magic
	def ksp(self, line, cell=None):
		if cell is None:
			kerbal.pilot()

			return line
		else:
			kerbal.controlpanel()
			return line, cell


# In order to actually use these magics, you must register them with a
# running IPython.  This code must be placed in a file that is loaded once
# IPython is up and running:
ip = get_ipython()
# You can register the class itself without instantiating it.  IPython will
# call the default constructor on it.
ip.register_magics(George)
