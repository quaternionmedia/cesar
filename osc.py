import json
from codecs import encode
from socket import socket, AF_INET, SOCK_DGRAM
from pythonosc import osc_message_builder
#from pythonosc import udp_client
from threading import Thread
from multiprocessing import Process

END = b'\xc0'
ESC = b'\xdb'
ESC_END = b'\xdc'
ESC_ESC = b'\xdd'
NULL = b'\x00'

commands = ['mix', 'mute', 'unmute']

def slip(packet):
	encoded = END
	for char in packet:
		if char == END:
			encoded +=  ESC + ESC_END
		elif char == ESC:
			encoded += ESC + ESC_ESC
		else:
			encoded += char.encode()
	encoded += NULL * ((len(encoded) % 4 )+ 3) # padding magic
	encoded += END
	return encoded


class Client: # TCP SLIP client
	def __init__(self, addr, port):
		#self.client = udp_client.UDPClient('127.0.0.1', port) # for udp
		self.client = socket()
		self.client.connect((addr, port))
		self.last_message = None
		self.messages = [None]
		self.get_message()

	def send_message(self, message, value=None):
		msg = osc_message_builder.OscMessageBuilder(address=message)
		if value:
			msg.add_arg(value)
		#self.client.send(msg.build()) # for udp
		encoded = slip(msg.build().address)
		print('sending: ', encoded)
		self.client.send(encoded)
		#self.get_message()

	def _get_message(self):
		data, address = self.client.recvfrom(8192)
		#print('data = ', data, address)
		#if data == None:
		#	self.messages.append(None)
		#else:
		data = data.replace(b'\xc0', b'')
		#data = data.replace(b'\xd7', b'')
		#data = data.replace(b'\x85', b'')
		#data = data.replace(b'\x80', b'')
		#print('recieved message: ', data)
		raw = data.decode('utf8')
		parts = list(filter(bool, raw.split('\x00')))
		self.messages.append(parts)
		for part in parts:
			try:
				self.last_message = json.loads(part)
			except json.decoder.JSONDecodeError as e:
				print(part)
				self.last_message = part
			self.messages.append(self.last_message)

	def get_message(self):
		#self.last_message = None
		t = Thread(target=self._get_message, daemon=True) # properly returns stuff
		#t = Process(target=self._get_message, daemon=True) # returns none for some resason
		t.start()
		t.join(timeout=.1)
		return self.messages[-1]

class Server:
	def __init__(self, addr, port):
		self.sock = socket(AF_INET, SOCK_DGRAM)
		self.sock.bind((addr, port))
		self.messages = [None]
		#self.get_message()

	def _get_message(self):
		data, address = self.sock.recvfrom(8192)
		print('data = ', data, address)
		if data is not None:
			data = data.replace(b'\xc0', b'')
			#data = data.replace(b'\xd7', b'')
			#data = data.replace(b'\x85', b'')
			#data = data.replace(b'\x80', b'')
			#print('recieved message: ', data)
			#raw = data.decode('utf8')
			parts = list(filter(bool, data.split(b'\x00')))
			#self.messages.append(parts)
			message = []
			for part in parts:
				if part == b',':
					continue
				try:
					self.last_message = json.loads(part)
				except json.decoder.JSONDecodeError as e:
					#print('json error', part)
					#self.last_message = part
					pass
				except Exception as e:
					print(e, part)
				try:
					self.last_message = part.decode('utf8')
				except Exception as e:
					print('decode error', e, part)
				if self.last_message is not None:
					message.append(self.last_message)
				self.last_message = None
			self.messages.append(message)
			return

	def get_message(self):
		#self.last_message = None
		t = Thread(target=self._get_message, daemon=True) # properly returns stuff
		#t = Process(target=self._get_message, daemon=True) # returns none for some resason
		t.start()
		t.join(timeout=.1)
		return self.messages[-1]
		self.get_message()
	def wait_for_message(self):
		t = Thread(target=self._get_message, daemon=True)
		t.start()
		t.join()
		# try:
		# 	exec(self.oscParse(self.messages[-1]), globals())
		# except Exception as e:
		# 	print('osc exec error: ', e, self.oscParse(self.messages[-1]))
		# self.wait_for_message()
	def oscParse(self, thing):
		cmd = ''
		#print('parsing thing: ', thing)
		address = list(filter(bool, thing[0].split('/')))
		#print('address: ', address)
		l = len(address)
		cmd = address[0]
		if cmd in commands:
			cmd = 's.' + cmd + '('
			i = 0
			for m in address:
				if m == address[0]:
					continue
				elif m.__class__ is str:
					cmd += '\'' + m + '\'' + ','
				i += 1
			for t in thing:
				if t == thing[0]:
					continue
				elif t == ',i':
					cmd += str(ord(thing[-1]))
					break
			cmd = cmd + ')'
			#print('Parsed! ', cmd)
			return cmd
