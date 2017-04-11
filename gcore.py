from __future__ import print_function
import networkx as nx
from tkinter import Tk, Frame, Label, Canvas, Entry, Button
import matplotlib
matplotlib.use("TkAgg") # Extremely important. Don't know why. Do not move.
from matplotlib import pyplot as plt
from multiprocessing import Manager
from multiprocessing.managers import SyncManager, BaseManager
from threading import Thread, Lock, Event
from queue import Queue
import time
from sys import stderr
from IPython.core.magic import (Magics, magics_class, line_magic, cell_magic, line_cell_magic)
import ast
import editor
import tktest

import osc

import kerbal
icons = []

ions = []

class Ion():
	def __init__(self, logic, *args):
		#StoppableThread.__init__(self, logic)
		self.ion = nx.MultiDiGraph()
		self.ion.add_node('parents')
		self.ion.add_node('children')

		self._stopper = Event()
		self.logic = logic
		self.args = args
		#self.thread = Thread(target=self.run, daemon=True)
		#self.thread.start()
		ions.append(self)

	def stopit(self):
		print( "base stop()", file=stderr )
		self._stopper.set()

	def stopped(self):
		return self._stopper.is_set()

	def run(self):
		#pass
		if self.logic.__class__ == str:
			return exec((self.logic + '()'), globals())
		elif len(self.args) == 0:
			return self.logic()
		else:
			return self.logic(self.args)

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

def buf(qu, *args):
	for i in range(v.getLength()):
		with v.lock:
			qu.put(v.bufferFrame(i))
def showFrame(frame):
	print('displaying frame', frame)
	v.buffer.append(frame)

def background(func, *args):# aft, *args):
	def do(qu,ars):
		while True:
			qu.put(func(qu,ars))
			#time.sleep(.01)
	def get(qu):
		while True:
			mes = qu.get()
			if mes is not None:
				print(mes)
				aft(mes)


	queue = Queue()

	thread = Thread(target=do, args=[queue, args], daemon=True)
	#thread.start()
	results = Thread(target=get, args=[queue], daemon=True)
	#results.start()

	#thread = Ion(Thread(target=do, args=[queue, args]))
	#results = Ion(Thread(target=get, args=[queue]))
	return thread, results, queue





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
						exec('s.' + osc.oscParse(mes), globals())
				except Exception as ex:
					print('osc exec error: ', ex, mes)
					m = osc.oscParse(mes)
					print('oscParse: ', m)

	queue = Queue()

	p = Thread(target=do, args=[queue], daemon=True)
	p.start()

	e = Thread(target=get, args=[queue], daemon=True)
	e.start()
	#return p
def board():
	background()




def resize(event):
	w,h = event.width, event.height
	#show.config(width=w, height=h)
	v.width, v.height = w, h
	v.buffer = []
	print('resizing to ', w, h)


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
		try:

			q = Qlab()
			q.send('/version')
		except:
			print('Warning - Not connected to QLab!!!')
		v = Video('/Users/harpo/Movies/Proclaim2016 Tom edit.mp4')
		#v = Video('/Users/peterkagstrom/Media/TV & Movies/Futurama - Seasons 1-7/Futurama - Season 1')
		#v = Video('/Users/peterkagstrom/Dropbox/Cesar and Rubin/Audio & Video/Cesar and Ruben Qlab Oct-2011/video/shot3_v11_H264.mov')
		#v = Video(0)
		try:
			s = Sound()
		except:
			print('WARNING - No sound module available')

		try:
			l = Lights()
		except:
			print('Not connected to lighting board')

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
			ki = Ion('ki')



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


	@line_magic
	def timeline(self, line):
		global v, show, control, g, t, c
		#g = Ion()
		#v = editor.Timeline('/Users/harpo/Movies/Proclaim2016 Tom edit.mp4')
		#v = editor.Timeline('/Users/peterkagstrom/Downloads/Captain.America.Civil.WAR.2016.1080p.HD.TC.AC3.x264-ETRG.mkv')
		v = editor.Timeline('/Users/peterkagstrom/Dropbox/Cesar and Rubin/Audio & Video/Cesar and Ruben Qlab Oct-2011/video/shot3_v11_H264.mov')
		show = Tk()
		show.geometry('1280x720+100+100')
		c = Canvas(show)
		c.place(x=0,y=5,relheight=1,relwidth=1)
		v.assignWindow(c)

		#c.bind('<Configure>', resize)
		control = Tk()
		con = tktest.Tester(control)
		control.geometry('1320x240+0+240')
		control.config(bg='darkgrey')
		control.title('Control')
		control.bind('<space>', v.play)
		show.bind('<space>', v.play)
		x = 0
		icons = []
		count = 0
		for i in v.timeline:
			l = i[2]-i[1]
			icons.append(tktest.Icon(i))
			icons[-1].attach(con.canvas, x, 10)
			x += l

		t = background(buf)#, showFrame)

		v.play()

		return line

	@line_magic
	def ggui(self, line):
		global control, loadin, reloadin, gui, reflow
		_w = 800
		_h = 1000
		_x = 0
		_y = 0
		control = Tk()
		gui = tktest.Tester(control)
		gui.top.geometry('%sx%s+%s+%s' %(_w,_h,_x,_y))

		def wcha(e):
			# _w = e.x
			# _h = e.y
			#reloadin(locals())
			print('wcha', e)
			# reflow()
			#icons = []
			#loadin(globals())
			# print(e)
			# gui.top.geometry('%sx%s+%s+%s' %(e.x,e.y,_x,_y))

		control.title('gGui')
		# control.bind('<Configure>', lambda e: print('wcha', e))
		gui.top.bind('<ButtonPress>', lambda e: print('Pressed', e))
		gui.top.bind('<Configure>', wcha)
		gui.top.bind('<ButtonRelease>', lambda e: print('Let go',e))
		gui.top.bind()

		def loadin(_i):
			#icons = []
			__y = 0
			__x = 10
			for i in _i:# if i not in icons:
				icons.append(tktest.Icon(i))
				icons[-1].attach(gui.canvas, __x, __y)
				print(i, gui.top.winfo_height())
				if(__y > gui.top.winfo_height()):
					__x += 100
					__y = 0
				else: __y += 20

		def reloadin(_i):
			# icons = []
			__x = icons[-1].label.winfo_x()
			__y = icons[-1].label.winfo_y()
			labels = []
			xy = {}
			for i in icons:
				labels.append(i.name)
				xy[i.name] = (i.label.winfo_x(), i.label.winfo_y())
			for i in [x for x in _i if x not in labels]:
				if i is not None:
					icons.append(tktest.Icon(i))

					if(__y > gui.top.winfo_height()):
						__x += 100
						__y = 0
					else: __y += 20
					icons[-1].attach(gui.canvas, __x, __y)
					xy[i] = (icons[-1].label.winfo_x(), icons[-1].label.winfo_y())
			print(xy)

		def reflow():
			__y = 0
			__x = 10
			for i in icons:
				if(__y > gui.top.winfo_height()):
					__x += 100
					__y = 0
				else: __y += 20
				i.attach(gui.canvas, __x, __y)
				print(i, __x, __y)

		#loadin(globals())

		# icons = []
		# __y = 0
		# __x = 10
		#
		# for l in globals():
		# 	icons.append(tktest.Icon(Ion(l).logic))
		# 	icons[-1].attach(gui.canvas, __x, __y)
		# 	if(__y > _h):
		# 		__x += 100
		# 		__y = 0
		# 	else: __y += 20

		#redraw(icons, gui)





	@line_magic
	def cgcore(self, line):

		return line

	@line_magic
	def mana(self,line):
		global man
		man = Ion(manag)
		return line

	@line_magic
	def ger(self,line):
		global m1, m2
		m1 = make_server_manager(51365,authkey=51365)
		m1.start()
		m2 = make_client_manager('127.0.0.1',53165,authkey=51365)
def manag():
	queue = Queue()
	class QueueManager(BaseManager): pass
	QueueManager.register('get_queue', callable=lambda:queue)
	m = QueueManager(address=('', 50000), authkey=b'abracadabra')
	s = m.get_server()
	s.serve_forever()

def make_server_manager(port, authkey):
	""" Create a manager for the server, listening on the given port.
		Return a manager object with get_job_q and get_result_q methods.
	"""
	job_q = Queue()
	result_q = Queue()

	# This is based on the examples in the official docs of multiprocessing.
	# get_{job|result}_q return synchronized proxies for the actual Queue
	# objects.
	class JobQueueManager(SyncManager):
		pass

	JobQueueManager.register('get_job_q', callable=lambda: job_q)
	JobQueueManager.register('get_result_q', callable=lambda: result_q)

	manager = JobQueueManager(address=('', port), authkey=authkey)
	manager.start()
	print('Server started at port %s' % port)
	return manager

def make_client_manager(ip, port, authkey):
	""" Create a manager for a client. This manager connects to a server on the
		given address and exposes the get_job_q and get_result_q methods for
		accessing the shared queues from the server.
		Return a manager object.
	"""
	class ServerQueueManager(SyncManager):
		pass

	ServerQueueManager.register('get_job_q')
	ServerQueueManager.register('get_result_q')

	manager = ServerQueueManager(address=(ip, port), authkey=authkey)
	manager.connect()

	print('Client connected to %s:%s' % (ip, port))
	return manager



# In order to actually use these magics, you must register them with a
# running IPython.  This code must be placed in a file that is loaded once
# IPython is up and running:
ip = get_ipython()
# You can register the class itself without instantiating it.  IPython will
# call the default constructor on it.
ip.register_magics(George)
