from codecs import encode
from socket import socket, AF_INET, SOCK_DGRAM, SOCK_STREAM, create_connection
from pythonosc import osc_message_builder
#from pythonosc import udp_client
from threading import Thread, Lock
from queue import Queue
from struct import unpack

END = b'\xc0'
ESC = b'\xdb'
ESC_END = b'\xdc'
ESC_ESC = b'\xdd'
NULL = b'\x00'

def oscParse(thing): # turn osc message into python command
	#print('parsing thing: ', thing)
	args = thing.partition(b',') # split message into address and values
	address = list(filter(bool, args[0].split(b'/'))) # seperate address into parts
	#print('address: ', address, 'args = ', args)
	cmd = address[0].decode('utf8') + '(' # assume first address is a function
	address = address[1:] # remove cmd from address
	for i in address: # add rest of address
		cmd += '\'' + unPadBack(i).decode('utf8') + '\'' + ','
	for j in parseNumbers(args[2]): # add all numbers as strings to cmd
		if j is not b'':
			cmd += str(j) + ','
			# print('adding number ', j)
	cmd += ')'
	print('Parsed! ', cmd)
	return cmd

def tcpParse(thing):
	#print('stripping SLIP from: ', thing)
	if thing.find(END + END) >= 0: # there's more than one message here
		things = list(filter(bool, thing.split(END + END)))
		parsed = []
		for t in things:
			raw = unSlip(t)
			parsed.append(raw)
		return parsed
	else: # there's only one message here
		return unSlip(thing)

def slip(packet): # RFC 1055
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

def unSlip(thing):
	if thing[1] == END:
		thing = thing[1:]
	if thing[-1] == END:
		thing = thing[:-1]
	while thing.find(ESC + ESC_END) > -1:
		thing.replace(ESC + ESC_END, END)
	while thing.find(ESC + ESC_ESC) > -1:
		thing.replace(ESC + ESC_END, ESC)
	return thing

def unPadFront(thing):
	while thing.find(NULL) == 0:
		thing = thing[1:]
	return thing

def unPadBack(thing):
	while thing[-1] == 0: # NULL evaluates to 0
		thing = thing[:-1]
	return thing

def parseNumbers(thing): # Qlab sends a 3 byte 'header' for type, then the number(s)
	kind = thing[:2]
	thing = thing[3:]
	return unpack(b'>' + kind, thing)

def build(message, value=None): # assemble and SLIP message
	msg = osc_message_builder.OscMessageBuilder(address=message)
	if value:
		msg.add_arg(value)
	return(slip(msg.build().address))


class Osc:

	def _get_message(self, queue): # get message and add it to queue
		parts = self.get_message()
		with self.lock:
			queue.put(parts)

	def get_message(self): # returns one message. Joins  until message is gotten.
		data, address = self.conn.recvfrom(8192)
		return tcpParse(data)


class Client(Osc): # TCP SLIP osc 1.1 connection
	def __init__(self, addr, port):
		#self.client = udp_client.UDPClient(addr, port) # for udp
		self.conn = create_connection((addr, port))
		self.lock = Lock()

	def send_message(self, message, value=None):
		encoded = build(message, value)
		print('sending: ', encoded)
		self.conn.send(encoded)


class Server(Osc):
	def __init__(self, addr, port):
		self.conn = socket(AF_INET, SOCK_DGRAM)
		self.conn.bind((addr, port))
		self.lock = Lock()
		#self.conn.listen(5)
