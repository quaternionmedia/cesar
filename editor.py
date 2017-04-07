from video import Video
from time import perf_counter, sleep
from tkinter import Label
from threading import Thread, Lock

class Timeline():
	def __init__(self, path):
		self.window = None # tk label for display
		self.playing = False
		self.videos = {0:path}
		self.video = [Video(self.videos[0])]
		#self.timeline = [(0,900,1000), (0,4000,4050), (0,8000,8100)]
		self.timeline = [(0,600,650), (0,0,100), (0,500,550)]#,(50,500)]
		self.fps = 24
		self.duration = 1
		self.time = 0
		self.startTime = perf_counter()
		self.buffer = []
		self.frameNumber = 0
		#self.play()
		self.lock = Lock()
		#Thread(target=self.bufMan, daemon=True).start()
		self.length = self.getLength()
	def addVido(self, v):
		self.videos[v] = Video(v)
	def loadVideo(self, v):
		self.video = self.videos[v]

	def playNextFrame(self):
		if self.playing:
			if self.frameNumber < self.length:
				if self.frameNumber < len(self.buffer):
					if perf_counter() - self.startTime >= self.frameNumber/self.fps:
						print('new frame', self.frameNumber)
						self.window.configure(image=self.buffer[self.frameNumber])
						self.frameNumber += 1
						self.window.after(int(1/self.fps*1000), self.playNextFrame)
					else:
						self.buffer.append(self.bufferFrame(len(self.buffer)- 1))
						self.playNextFrame()
				else:
					self.buffer.append(self.bufferFrame(len(self.buffer)))
					self.playNextFrame()
			else:
				self.playing = False


	def play(self, *args):
		self.playing = not self.playing
		if self.playing:
			self.startTime = perf_counter() - (self.frameNumber/self.fps)
			self.playNextFrame()

	def playClip(self):
		self.clip = getClip(perf_counter() - self.startTime)
		if self.video.path != self.videos[self.clip[0]]:
			self.loadVideo(self.videos[self.clip[0]])


	def bufferFrame(self, n):
		c, f = self.getPos(n)
		print('getting position: ', c, f)
		return self.video[c]._bufferFrame(f)



	def bufMan(self):
		for clip in self.timeline:
			for frame in range(clip[2]-clip[1]):
				self.buffer.append(self.video[clip[0]]._bufferFrame(clip[1] + frame))
				print('buffered frame', frame, self.buffer[-1])




	def assignWindow(self, w):
		self.window = Label(w)
		self.window.grid(row=0, column=0, sticky='nsew')

	def getPos(self, f): # Return (video, frame)
		#c = 0
		for clip in self.timeline:
			if f >= clip[2] - clip[1]:
				f -= clip[2] - clip[1]
			#	c += 1
			else:
				return clip[0], clip[1] + f
	def getLength(self):
		l = 0
		for clip in self.timeline:
			l += clip[2] - clip[1]
		return l

def getClip(t):
	i = 0
	for clip in self.timeline:
		if t > clip[2] - clip[1]:
			t -= clip[2] - clip[1]
			i += 1
		else:
			return clip
			break
