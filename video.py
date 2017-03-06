import numpy as np
import cv2
import time
import PIL.Image as Image
import PIL.ImageTk as ImageTk

class Video:
	def __init__(self, path, label):
		self.path = path
		self.video = self.loadVideo(self.path)

		self.vlabel = label # must be tk label
		self.width = self.vlabel.winfo_width()
		self.height = self.vlabel.winfo_height()
		#self.window.overrideredirect(1)
		#self.window.geometry("%dx%d+0+0" % (self.width, self.height))
		self.frameDelay = 26
		self.frameNumber = self.video.get(1)
		self.ratio = self.video.get(2)
		#self.width = self.video.get(3)
		#self.height = self.video.get(4)
		self.fps = int(100*self.video.get(5))/100
		self.frames = self.video.get(7)
		self.playing = True
		self.fading = False
		self.fadeDuration = 0
		self.startTime = time.perf_counter()
		self.currentTime = 0
		#self.img = None
		self.res = 0
		self.delays = []

	def loadVideo(self, path):
		return cv2.VideoCapture(path)

	def play(self):
		if self.playing:
			self.ret, self.frame = self.video.read()
			if self.ret:
				self.resized = cv2.resize(self.frame, (self.width, self.height))
				self.cv2image = cv2.cvtColor(self.resized, cv2.COLOR_BGR2RGBA)
				#self.resized = Image.fromarray(self.cv2image).resize((self.w, self.h))
				if self.fading:
					self.bret, self.bframe = self.b.read()
					if self.bret:
						self.bresized = cv2.resize(self.bframe, (self.width, self.height))
						self.bimage = cv2.cvtColor(self.bresized, cv2.COLOR_BGR2RGBA)
						#self.bresized = Image.fromarray(self.bimage).resize((self.w, self.h))
						self.alpha = self.alpha*self.fadeDuration/(self.fadeDuration+1)
						self.cv2image = cv2.addWeighted(self.cv2image, self.alpha, self.bimage, 1-self.alpha, 0)
						#self.cv2image = Image.blend(self.resized, self.bresized, self.alpha)
						if self.fadeDuration == 0:
							self.fading = False
							self.video = self.b
							#self.b.release()
							self.frameNumber = self.video.get(1)
							self.startTime = time.perf_counter() - (self.frameNumber/self.fps)
						else:
							self.fadeDuration -= 1
				#self.cv2image = cv2.resize(self.cv2image, (self.width, self.height), interpolation=cv2.INTER_LANCZOS4)
				#self.img = Image.fromarray(self.cv2image)#.resize((self.width, self.height), resample=Image.NEAREST)
				#self.big = np.zeros((self.width*self.res, self.height*self.res, 4), dtype = np.uint8)
				#self.big = cv2.pyrUp(self.cv2image)
				#for i in range(self.res):
				#	self.big = cv2.pyrUp(self.big)
				self.img = Image.fromarray(self.cv2image)
				#self.fullscreen.putdata('RGBA', self.img)
				self.imgtk = ImageTk.PhotoImage(image=self.img)
				#self.pimgtk = tk.PhotoImage(self.imgtk)#.zoom(2)
				#self.lmain.imgtk = self.imgtk
				self.vlabel.configure(image=self.imgtk)
				# figure out next time
				self.frameNumber += 1
				self.frameDelay = int(1000*((self.frameNumber/self.fps) - (time.perf_counter() - self.startTime)))
				# self.meta.configure(text='frame: %s frameDelay: %s fps: %s perf: %.3f startTime %s' %(self.frameNumber, self.frameDelay, self.fps, time.perf_counter(), self.startTime))
				self.delays.append(self.frameDelay)
				#print('setting delay', self.frameDelay)
				if self.frameDelay < 0:
					s = -((self.frameNumber/self.fps) - (time.perf_counter() - self.startTime))
					print('video is behind schedule by %.2f ms' % (s*1000))
					if s > .2:
						self.video.set(1, self.frameNumber + int(s*self.fps) + 10 )
						self.frameNumber += int(s*self.fps) + 10
						print('seeking forward ', int(s*self.fps) + 10 )
					elif s > .01:
						self.video.read()
						self.frameNumber += 1
						if self.fading:
							self.b.read()
					self.frameDelay = 1

			else:
				print('no image')
				self.seek(0)
				#self.playing = False
				#self.fading = False
			self.vlabel.after(self.frameDelay, self.play)

	def seek(self, f):
		self.video.set(1, f)
		self.frameNumber = f
		self.startTime = time.perf_counter() - self.frameNumber / self.fps

	def space(self, event):
		print('pausing', event)
		self.pause()

	def pause(self):
		self.playing = not self.playing
		if self.playing:
			self.startTime = time.perf_counter() - (self.frameNumber/self.fps)
			self.play()

	def upRes(self, event):
		self.res = self.res +1

	def downRes(self, event):
		if self.res > 0:
			self.res = self.res - 1

	def fade(self, new, length):
		#if self.playing:
		#self.playing = False
		self.fading = True
		self.b = cv2.VideoCapture(new)
		self.alpha = 1
		self.fadeDuration = length
	def stats(self):
		return stats.describe(self.delays)
