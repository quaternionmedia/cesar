import json
from socket import socket
from pythonosc import osc_message_builder
#from pythonosc import udp_client

from multiprocessing import Process

END = b'\xc0'
ESC = b'\xdb'
ESC_END = b'\xdc'
ESC_ESC = b'\xdd'
NULL = b'\x00'

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
		print('data = ', data, address)
		if data == None:
			self.messages.append(None)
		else:
			data = data.replace(b'\xc0', b'')
			#data = data.replace(b'\xd7', b'')
			#data = data.replace(b'\x85', b'')
			#data = data.replace(b'\x80', b'')
			print('recieved message: ', data)
			raw = data.decode('utf8')
			parts = list(filter(bool, raw.split('\x00')))
			json_message = parts[1]
			try:
				self.last_message = json.loads(json_message)
				self.messages.append(self.last_message)
			except json.decoder.JSONDecodeError as e:
				print('Error. server raw response:', repr(raw))
				print('parts', parts)
				print(e)
				self.last_message = None

	def get_message(self):
		#self.last_message = None
		t = threading.Thread(target=self._get_message, daemon=True)
		t.start()
		t.join(timeout=.1)
		return self.messages[-1]
