from __future__ import print_function
import networkx as nx
from tkinter import Tk, Frame, Label, Canvas, Entry, Button
import matplotlib
matplotlib.use("TkAgg") # Extremely important. Don't know why. Do not move.
from matplotlib import pyplot as plt
from multiprocessing import Process, Queue#, Lock
from threading import Thread, Lock, Event#, Queue
import time
from sys import stderr
from IPython.core.magic import (Magics, magics_class, line_magic, cell_magic, line_cell_magic)
import ast

import osc

import kerbal

class StoppableThread(Thread):
	"""Thread class with a stop() method. The thread itself has to check
	regularly for the stopped() condition."""

	def __init__(self, l=None):
		print( "base init", file=stderr )
		super(StoppableThread, self).__init__()
		self._stopper = Event()
		self.logic = l

	def stopit(self):
		print( "base stop()", file=stderr )
		self._stopper.set()

	def stopped(self):
		return self._stopper.is_set()

class Ion(StoppableThread):
	def __init__(self, logic=None, *args):
		StoppableThread.__init__(self, logic)
		self.ion = nx.MultiDiGraph()
		self.ion.add_node('parents')
		self.ion.add_node('children')

	def runIon(self,*args):
		print('thread running', file=stderr)
		while not self.stopped():
			# print('running',file=stderr)
			pass
		print('thread running', file=stderr)



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


class Gui():
	def __init__(self, _w, _h, _x, _y):
		global win, ions, can
		ions = []
		win = Tk()
		win.geometry(str(_w)+'x'+str(_h)+'+'+str(_x)+'+'+str(_y))
		can = Canvas(win)
		can.place(relheight=1,relwidth=1)
		can.bind('<Key>', lambda e: self.cli)

	def cli():
		pass





def resize(event):
	w,h = event.width, event.height
	#show.config(width=w, height=h)
	v.width, v.height = w, h
	v.buffer = []
	print('resizing to ', w, h)


def task(thing, *args):
	t = Process(target=thing, args=args)
	return t

def background(func,*args):


	def do(qu,ars):
		#f = compile(ast.parse(fn), '~/a','eval')
		while True:
			func(qu,ars)
			#exec(f, globals())
			time.sleep(.01)
	def get(qu):
		while True:
			mes = qu.get()
			if mes is not None:
				# print(mes)
				pass

	queue = Queue()

	# thread = Thread(target=do, args=[queue, args])
	# thread.start()
	# results = Thread(target=get, args=[queue])
	# results.start()

	thread = Ion(Thread(target=do, args=[queue, args]))
	results = Ion(Thread(target=get, args=[queue]))
	return thread, queue, results







	p = Thread(target=do, args=[queue])#, daemon=True)
	p.start()

	m = Thread(target=get, args=[queue])
	m.start()

	return m,p,queue


def activateSoundBoard():

	def do(qu):
		while True:
			mes = q.server._get_message(qu)
			#qu.put(mes)
	def get(qu):
		lock = Lock()
		while True:
			with lock:
				mes = qu.get()
			if mes is not None:
				try:
					with lock:
						exec(osc.oscParse(mes), globals())
				except Exception as ex:
					print('osc exec error: ', ex, mes)
					m = osc.oscParse(mes)
					print('oscParse: ', m)

	queue = Queue()

	p = Thread(target=do, args=[queue])#, daemon=True)
	p.start()

	e = Thread(target=get, args=[queue])
	e.start()
	#return p
def board():
	background()



	#m = queue.get()



# def

# The class MUST call this class decorator at creation time
@magics_class
class George(Magics):

	@line_magic
	def gcore(self, line):
		global gui
		gui = Gui(800,600,2550,1230)

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
		#v = Video('/Users/peterkagstrom/Media/TV & Movies/Futurama - Seasons 1-7/Futurama - Season 1')
		#v = Video('/Users/peterkagstrom/Dropbox/Cesar and Rubin/Audio & Video/Cesar and Ruben Qlab Oct-2011/video/shot3_v11_H264.mov')
		#v = Video(0)
		try:
			s = Sound()
		except:
			print('no sound module available')
		# try:
		# 	l = Lights()
		# except:
		# 	print('WARNING - NOT CONNECTED TO LIGHTING BOARD')

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

			global k, v, ap, ki
			k = kerbal
			k.pilot()
			v = kerbal.vessel
			ap = v.auto_pilot
			ki = Ion()



			return line
		else:
			kerbal.controlpanel()
			return line, cell

	@line_magic
	def tentry(self, line):


		master = Tk()

		e = Entry(master)
		e.pack()

		e.focus_set()

		def callback():
			print(e.get())

		b = Button(master, text="get", width=10, command=callback)
		b.pack()

		mainloop()
		e = Entry(master, width=50)
		e.pack()

		text = e.get()
		def makeentry(parent, caption, width=None, **options):
			Label(parent, text=caption).pack(side=LEFT)
			entry = Entry(parent, **options)
			if width:
				entry.config(width=width)
			entry.pack(side=LEFT)
			return entry

		user = makeentry(parent, "User name:", 10)
		password = makeentry(parent, "Password:", 10, show="*")
		content = StringVar()
		entry = Entry(parent, text=caption, textvariable=content)

		text = content.get()
		content.set(text)
		return line


# In order to actually use these magics, you must register them with a
# running IPython.  This code must be placed in a file that is loaded once
# IPython is up and running:
ip = get_ipython()
# You can register the class itself without instantiating it.  IPython will
# call the default constructor on it.
ip.register_magics(George)
