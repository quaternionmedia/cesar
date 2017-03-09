from __future__ import print_function
import networkx as nx
from tkinter import Tk, Frame, Label, Canvas

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

# The class MUST call this class decorator at creation time
@magics_class
class George(Magics):

	@line_magic
	def cesar(self, line):
		global g, show, control, v
		g = Ion()

		show = Tk()
		#l = Label(show)
		#l.place(x=0,y=5,relheight=1,relwidth=1)
		import video
		global v
		v = video.Video('/Users/harpo/Movies/Proclaim2016 Tom edit.mp4')
		c = Canvas(show)
		c.place(x=0,y=5,relheight=1,relwidth=1)
		v.assignWindow(c)
		v.play()
		#import video
		#global vi
		# label = Label(show)
		#vi = video.Video('/Users/harpo/Movies/reduced_1.mp4', l)
		#vi.play()

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
			i.client.send_message()
		control.bind('<space>', action)
		cdatas = Label(control, text='x:%s, y:%s' %( control.winfo_screenwidth(), control.winfo_screenheight()))
		#g.addChild(cdatas)

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

	@line_cell_magic
	def osc(self, line):
		import osc
		global q
		q = osc.Qlab()
		q.send('/workspaces')
		q.send('/go')
		q.send('/version')
		return line

	@line_magic
	def video(self, line):
		import video
		global window, v
		window = Tk()
		v = video.Video('/Users/harpo/Movies/Proclaim2016 Tom edit.mp4')
		v.assignWindow(show)
		v.play()

	@line_magic
	def sound(self, line):
		import osc
		import mido
		global r, s
		s = osc.Sound()

	@line_cell_magic
	def ksp(self, line, cell=None):
		if cell is None:
			import krpc
			print(krpc.__version__)
			conn = krpc.connect(name='Hello World')
			print(conn.krpc.get_status().version)
			vessel = conn.space_center.active_vessel
			print(vessel.name)
			return line
		else:
			return line, cell


# In order to actually use these magics, you must register them with a
# running IPython.  This code must be placed in a file that is loaded once
# IPython is up and running:
ip = get_ipython()
# You can register the class itself without instantiating it.  IPython will
# call the default constructor on it.
ip.register_magics(George)
