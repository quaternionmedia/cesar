import cv2
import tkinter
import numpy
import time
#python2 version (original) -> 120fps
#full physical file io and new image each cycle -> 130fps
#reuse PIL Image instead of create new each time -> 160fps
#and... direct image into tkinter using ppm byte array -> 240 fps

v = cv2.VideoCapture('/Users/harpo/Movies/CRfirst.mp4')
w = int(v.get(3))
h = int(v.get(4))
global data
n = numpy.zeros((w,h))

class mainWindow():
	times=1
	timestart=time.clock()
	data=numpy.array(numpy.random.random((w,h))*900,dtype=numpy.uint16)

	def __init__(self):
		self.root = tkinter.Tk()
		#self.frame = tkinter.Frame(self.root, width=w, height=h)
		#self.frame.pack()
		#self.canvas = tkinter.Canvas(self.root, width=w,height=h)
		#self.canvas.place()
		self.label = tkinter.Label(self.root, width=w, height=h)
		#xdata = b'P5 500 400 255 ' + self.data.tobytes()
		#self.photo = tkinter.PhotoImage(width=w, height=h, data=xdata, format='PPM')
		#self.imid = self.canvas.create_image(0,0,image=self.photo,anchor=tkinter.NW)
		#self.root.after(100,self.start) # INCREASE THE 0 TO SLOW IT DOWN
		#self.root.mainloop()
	def start(self):

		ret, data = v.read()

		if ret:
			d = numpy.array(cv2.cvtColor(data, cv2.COLOR_BGR2RGB))

			x = 'P6 \n%s %s\n255\n' % (w, h)
			y = bytes(x, 'UTF-8')
			xdata = y + d.tobytes()
			self.photo = tkinter.PhotoImage(width=w, height=h, data=xdata, format='PPM')
			if True:
				self.label.configure(image = self.photo)
			#else:
			#	self.canvas.delete(self.imid)
			#	self.imid = self.canvas.create_image(0,0,image=self.photo,anchor=tkinter.NW)
			self.times+=1
			if self.times%33==0:
				print("	%.02f FPS"%(self.times/(time.clock()-self.timestart)))
			self.root.update()
			self.root.after(100,self.start)
			#self.data=numpy.roll(self.data,-1,1)

x = mainWindow()
if __name__ == '__main__':
	x = mainWindow()

#!/usr/bin/python

# use a Tkinter label as a panel/frame with a background image
# note that Tkinter only reads gif and ppm images
# use the Python Image Library (PIL) for other image formats
# free from [url]http://www.pythonware.com/products/pil/index.htm[/url]
# give Tkinter a namespace to avoid conflicts with PIL
# (they both have a class named Image)
#
# import tkinter as tk
# from PIL import Image, ImageTk
# from tkinter.ttk import Frame, Button, Style
# import time
#
# class Example():
# 	def __init__(self):
# 		self.root = tk.Tk()
# 		self.root.title('My Pictures')
#
# 		# pick an image file you have .bmp  .jpg  .gif.  .png
# 		# load the file and covert it to a Tkinter image object
# 		imageFile = "/Users/harpo/Downloads/art4.jpg"
# 		self.image1 = ImageTk.PhotoImage(Image.open(imageFile))
# 		self.image2 = ImageTk.PhotoImage(Image.open("/Users/harpo/Downloads/art22.jpg"))
#
# 		# get the image size
# 		#w = self.image1.width()
# 		#h = self.image1.height()
# 		w = 1920
# 		h = 1080
#
# 		# position coordinates of root 'upper left corner'
# 		x = 0
# 		y = 0
#
# 		# make the root window the size of the image
# 		self.root.geometry("%dx%d+%d+%d" % (w, h, x, y))
#
# 		# root has no image argument, so use a label as a panel
# 		self.panel1 = tk.Label(self.root, image=self.image1)
# 		self.display = self.image1
# 		self.panel1.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.YES)
# 		print( "Display image1")
# 		self.root.after(3000, self.update_image)
# 		self.root.mainloop()
#
# 	def update_image(self):
# 		if self.display == self.image1:
# 			self.panel1.configure(image=self.image2)
# 			print( "Display image2")
# 			self.display = self.image2
# 		else:
# 			self.panel1.configure(image=self.image1)
# 			print("Display image1")
# 			self.display = self.image1
# 		self.root.after(3000, self.update_image)       # Set to call again in 30 seconds
#
# def main():
# 	app = Example()
#
# if __name__ == '__main__':
# 	main()


# import tkinter
# import numpy
# import time
# #python2 version (original) -> 120fps
# #full physical file io and new image each cycle -> 130fps
# #reuse PIL Image instead of create new each time -> 160fps
# #and... direct image into tkinter using ppm byte array -> 240 fps
#
# class mainWindow():
#     times=1
#     timestart=time.clock()
#     data=numpy.array(numpy.random.random((400,500))*900,dtype=numpy.uint16)
#
#     def __init__(self):
#         self.root = tkinter.Tk()
#         self.frame = tkinter.Frame(self.root, width=500, height=400)
#         self.frame.pack()
#         self.canvas = tkinter.Canvas(self.frame, width=500,height=400)
#         self.canvas.place(x=-2,y=-2)
#         xdata = b'P5 500 400 255 ' + self.data.tobytes()
#         self.photo = tkinter.PhotoImage(width=500, height=400, data=xdata, format='PPM')
#         self.imid = self.canvas.create_image(0,0,image=self.photo,anchor=tkinter.NW)
#         self.root.after(1,self.start) # INCREASE THE 0 TO SLOW IT DOWN
#         self.root.mainloop()
#
#     def start(self):
#         global data
#         xdata = b'P5 500 400 255 ' + numpy.clip(self.data,0,255).tobytes()
#         self.photo = tkinter.PhotoImage(width=500, height=400, data=xdata, format='PPM')
#         if True:
#             self.canvas.itemconfig(self.imid, image = self.photo)
#         else:
#             self.canvas.delete(self.imid)
#             self.imid = self.canvas.create_image(0,0,image=self.photo,anchor=tkinter.NW)
#         self.times+=1
#         if self.times%33==0:
#             print("%.02f FPS"%(self.times/(time.clock()-self.timestart)))
#         self.root.update()
#         self.root.after(0,self.start)
#         self.data=numpy.roll(self.data,-1,1)
#
# if __name__ == '__main__':
#     x=mainWindow()
#import sys
#if sys.version_info[0] == 2:  # Just checking your Python version to import Tkinter properly.
#    from Tkinter import *
#else:
# from tkinter import *
#
#
# class Fullscreen_Window:
#
#     def __init__(self):
#         self.tk = Tk()
#         #self.tk.attributes('-zoomed', True)  # This just maximizes it so we can see the window. It's nothing to do with fullscreen.
#         self.frame = Frame(self.tk)
#
#         self.frame.pack()
#         self.state = False
#         self.tk.bind("<f>", self.toggle_fullscreen)
#         self.tk.bind("<Escape>", self.end_fullscreen)
#
#     def toggle_fullscreen(self, event=None):
#         self.state = not self.state  # Just toggling the boolean
#         self.tk.attributes("-fullscreen", self.state)
#         return "break"
#
#     def end_fullscreen(self, event=None):
#         self.state = False
#         self.tk.attributes("-fullscreen", False)
#         return "break"
#
# if __name__ == '__main__':
#     w = Fullscreen_Window()
#     w.tk.mainloop()
