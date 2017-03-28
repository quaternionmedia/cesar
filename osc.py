import json
from codecs import encode
from socket import socket, AF_INET, SOCK_DGRAM, SOCK_STREAM, create_connection
from pythonosc import osc_message_builder
#from pythonosc import udp_client
from threading import Thread
from multiprocessing import Process, Queue

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

def build(message, value=None):
	msg = osc_message_builder.OscMessageBuilder(address=message)
	if value:
		msg.add_arg(value)
	return(slip(msg.build().address))

def oscParse(thing):
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
				if len(thing[-1]) > 1:
					total = 0
					for h in thing[-1]:
						total = ord(h)
						print(h, total)
					cmd += str(total)
				else:
					cmd += str(ord(thing[-1]))
				break
		cmd = cmd + ')'
		#print('Parsed! ', cmd)
		return cmd
	#try:
	#	j = json.loads(address[2])


class Osc:
	def _get_message(self, queue):
		data, address = self.conn.recvfrom(8192)
		#print('data = ', data, address)
		data = data.replace(b'\xc0', b'')
		raw = data.decode('utf8')
		parts = list(filter(bool, raw.split('\x00')))
		self.messages.append(parts)
		queue.put(parts)


class Client(Osc): # TCP SLIP osc connection
	def __init__(self, addr, port):
		#self.client = udp_client.UDPClient('127.0.0.1', port) # for udp
		#self.client = socket()
		#self.client.connect((addr, port))
		self.conn = create_connection((addr, port))
		self.queue = Queue()
		self.last_message = None
		self.messages = [None]
		#self.get_message()

	def send_message(self, message, value=None):
		encoded = build(message, value)
		print('sending: ', encoded)
		self.conn.send(encoded)
		#self.get_message()


class Server(Osc):
	def __init__(self, addr, port):
		self.conn = socket(AF_INET, SOCK_DGRAM)
		self.conn.bind((addr, port))
		#self.conn.listen(5)
		self.messages = [None]
		self.queue = Queue()
