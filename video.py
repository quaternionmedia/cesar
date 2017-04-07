import numpy as np
import cv2
import time
from sys import stdout
from math import ceil
import PIL.Image as Image
import PIL.ImageTk as ImageTk
from tkinter import Tk, Label

from multiprocessing import Pool

class Video:
	def __init__(self, path=None):
		self.path = path
		if self.path == None:
			self.video = cv2.VideoCapture(0)
			self.frameNumber = 0
			self.frames = 100
		else:
			self.video = self.loadVideo(self.path)
			self.frameNumber = int(self.video.get(1))

			self.frames = int(self.video.get(7)*.9) # bad safety factor
		self.ratio = self.video.get(2)
		self.width = int(self.video.get(3))
		self.height = int(self.video.get(4))
		self.fps = int(100*self.video.get(5))/100
		#self.vlabel = label # must be tk label
		#self.width = self.vlabel.winfo_width()
		#self.height = self.vlabel.winfo_height()
		#self.window.overrideredirect(1)
		#self.window.geometry("%dx%d+0+0" % (self.width, self.height))
		self.playing = False
		self.startTime = time.perf_counter()
		self.frameDelay = 26

		self.delays = []
		self.buffer = [] #np.array()
		self.bufferFrames = 24
		self.lag = 0
		self.frameBuildTime = None

	def loadVideo(self, path):
		return cv2.VideoCapture(path)

	def loadImage(self, path):
		return cv2.imread(path)

	def convertImage(self, img):
		self.frameBuildTime = -time.perf_counter()
		r = cv2.resize(img, (self.width, self.height), interpolation=cv2.INTER_NEAREST)
		s = cv2.cvtColor(r, cv2.COLOR_BGR2RGBA)
		t = Image.fromarray(s)
		u = ImageTk.PhotoImage(image=t)
		self.frameBuildTime += time.perf_counter() + int(self.lag)
		return u

	def getNextFrame(self, img):
		if type(img) == cv2.VideoCapture().__class__:
			ret, frame = img.read()
			if ret:
				return frame
			else:
				return self.frame
	def timeUntilNext(self):
		self.frameDelay = int(1000*((self.frameNumber/self.fps) - (time.perf_counter() - self.startTime - self.lag)))
		if self.frameDelay < 0: self.frameDelay = 0

	def bufferFrame(self):
			ret, frame = self.video.read()
			if ret:
				self.buffer.append(self.convertImage(frame))
	def _bufferFrame(self, fNum):
			if self.frameNumber is not fNum:
				self.seek(fNum)
			ret, frame = self.video.read()
			if ret:
				return self.convertImage(frame)
	def assignWindow(self, w):
		self.label = Label(w)
		self.label.grid(row=0, column=0, sticky='nsew')

	def playNext(self):
		#print(self.frameNumber, self.frames, flush=True)
		if self.frameNumber < self.frames and self.playing:
			while len(self.buffer) <= 1:
				self.bufferFrame()
			lag = -time.perf_counter()
			self.label.configure(image=self.buffer[1])
			del self.buffer[0]
			self.frameNumber += 1
			self.lag = lag + time.perf_counter()
			self.timeUntilNext()
			self.label.after(self.frameDelay, self.playNext)
			t = self.frameDelay / 1000
			#stdout.write('\rtimeLeft/timeTakes = %.02f buffer length = %d \r' % (t/self.frameBuildTime, len(self.buffer)))
			#stdout.flush()
			if t < 0:
				if -t*self.fps > len(self.buffer) - 2:
					self.buffer = []
					skip = self.frameNumber
					self.frameNumber = int((time.perf_counter() - self.startTime) * self.fps) + 10
					self.video.set(1, self.frameNumber)
					#self.frameNumber += skip
					print('skipping %d frames to %d' % (skip, self.frameNumber))
				else:
					self.buffer = self.buffer[int(-t/self.fps):]
					self.frameNumber += int(-t/self.fps)
			while t/self.frameBuildTime > 1 and len(self.buffer) < self.bufferFrames:
				self.bufferFrame()
				t -= self.frameBuildTime
		else:
			self.playing = False
	def play(self):
		if not self.playing:
			self.playing = not self.playing
			self.bufferFrame()
			self.startTime = time.perf_counter()
			self.playNext()

	def pause(self):
		self.playing = not self.playing
		if self.playing:
			self.startTime = time.perf_counter() - (self.frameNumber/self.fps)
			self.playNext()
	def seek(self, f):
		self.video.set(1, f)
		self.frameNumber = f
		self.buffer = []
		self.startTime = time.perf_counter() - self.frameNumber / self.fps
		self.bufferFrame
		#return g
