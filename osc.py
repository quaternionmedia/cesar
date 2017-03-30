import json
from codecs import encode
from socket import socket, AF_INET, SOCK_DGRAM, SOCK_STREAM, create_connection
from pythonosc import osc_message_builder
#from pythonosc import udp_client
from threading import Thread, Lock
from multiprocessing import Process, Queue
from struct import unpack

END = b'\xc0'
ESC = b'\xdb'
ESC_END = b'\xdc'
ESC_ESC = b'\xdd'
NULL = b'\x00'

commands = ['mix', 'mute', 'unmute', 'z']

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
	print('parsing thing: ', thing)
	args = thing.partition(b',')
	address = list(filter(bool, args[0].split(b'/')))
	#print('address: ', address)
	# dec = address[0]#.decode('utf8')
	# print('first = ', dec)
	# l = len(address)
	cmd = address[0].decode('utf8')
	#print('cmd = ', cmd)

	#args = list(filter(bool, address[-1].split(b',', maxsplit = 1 )))
	#args = address[-1].partition(b',')
	#print('args = ', args)

	if cmd in commands:
		cmd = 's.' + cmd + '('
		#i = 0
		cmd += '\'' + unPadBack(address[1]).decode('utf8') + '\'' + ','
		print('address = ', address, cmd)
		if args[2].find(b'i') == 0:
			#a = args[2].replace(b'i', b'', 1)
			a = unPadFront(args[2][1:])
			print('working with ', a)
			if a == b'':
				cmd += str(0)

			elif len(a) > 1:
				total = 0
				i = len(a) - 1
				for h in a:
					total += h * 256 ** i
					print(h, total)
					i -= 1
				cmd += str(total)
			else:
				cmd += str(ord(a))

		elif args[2].find(b'f') == 0:
			#a = args[2].replace(b'f', b'', 1)
			a = unPadFront(args[2][1:])
			#a = a.replace(b'\x00', b'', 1)

			if len(a) > 4:
				a = b'\x00' * (len(a) % 4) + a
			#print('a = ', a)
			if a == b'':
				b = str(0)
			else:
				b = unpack('>%s' % ('f' * int(len(a) / 4) ), a)[0]
			#print('b = ', b)
			cmd += str(b)


			#cmd += str(ord(a))
		cmd += ')'
		print('Parsed! ', cmd)
		return cmd

def tcpParse(thing):
	#print('stripping SLIP from: ', thing)
	if thing.find(b'\xc0\xc0') >= 0:
		things = list(filter(bool, thing.split(b'\xc0\xc0')))
		parsed = []
		for t in things:
			raw = unSlip(t)
			parsed.append(list(filter(bool, raw.split(b'\x00'))))
		return parsed
	else:
		return unSlip(thing)

def unSlip(thing):
	if thing[1] == b'\xc0':
		thing = thing[1:]
	if thing[-1] == b'\xc0':
		thing = thing[:-1]
	return thing

def unPadFront(thing):
	while thing.find(b'\x00') == 0:
		thing = thing[1:]
	return thing
def unPadBack(thing):
	while thing[-1] == 0:
		thing = thing[:-1]
	return thing

# def unCode(thing):
# 	try:
# 		raw = thing.decode('utf8')
# 	except Exception as e:
# 		print(e)
# 		raw = data.decode()
# 	return raw

class Osc:

	def _get_message(self, queue): # get message and add it to queue
		self.lock = Lock()

		data, address = self.conn.recvfrom(8192)
		parts = tcpParse(data)
		with self.lock:
			queue.put(parts)
		# for part in parts:
		# 	try:
		# 		self.last_message = json.loads(part)
		# 	except json.decoder.JSONDecodeError:
		# 		print(part)
		# 		self.last_message = part
		# 	self.messages.append(self.last_message)
	def get_message(self): # returns one message. Joins  until message is gotten.
		data, address = self.conn.recvfrom(8192)
		return tcpParse(data)

	#
	# def get_message(self):
	# 	#self.last_message = None
	# 	t = Thread(target=self._get_message, args=[self.queue], daemon=True) # properly returns stuff
	# 	#t = Process(target=self._get_message, daemon=True) # returns none for some resason
	# 	t.start()
	# 	t.join()#timeout=.1)
	# 	try:
	# 		results = self.queue.get(False, 1)
	# 	except Exception as e:
	# 		print(e)
	# 		results = None
	# 	if results is not None:
	# 		return results
	# 	#return self.messages[-1]


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
