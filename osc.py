# import asyncio
import json
import socket
import sys
import time
from pythonosc import osc_message_builder
from pythonosc import udp_client
import slip

import threading


class Client:
	def __init__(self, addr, port):
		#self.client = udp_client.UDPClient('127.0.0.1', port) # for udp
		self.client = socket.socket()
		self.client.connect((addr, port))
		self.last_message = None
		self.messages = [None]

	def send_message(self, message, value=None):
		msg = osc_message_builder.OscMessageBuilder(address=message)
		if value:
			msg.add_arg(value)
		#self.client.send(msg.build()) # for udp
		encoded = slip.encode(msg.build().address)
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
			data = data.replace(b'\xd7', b'')
			data = data.replace(b'\x85', b'')
			data = data.replace(b'\x80', b'')
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
		#time.sleep(.3)
		return self.messages[-1]


class Qlab:
	def __init__(self):
		self.client = Client('127.0.0.1', 53000)

	def send(self, message='/go'):
		self.client.send_message(message)
		self.client.messages.append(None)
		return self.client.get_message()
	def cue(self, cue):
		self.send('/cue/%s/start' % cue)
	def select(self, select):
		self.send('/select/%s' % select)
	def get_cue_text(self, cue_no):
		return self.get_cue_property(cue_no, 'text')

	def get_cue_property(self, cue_no, name):
		self.client.send_message('/cue/{cue_no}/{name}'.format(**locals()))
		response = self.client.get_message()
		if response:
			return response.get('data')

	def set_cue_property(self, cue_no, name, value):
		self.client.send_message('/cue/{cue_no}/{name}'.format(**locals()), value=value)

	def select_next_cue(self):
		old = self.get_cue_property('selected', 'number')
		self.client.send_message('/select/next')

		cue_no = self.get_cue_property('selected', 'number')
		print(old, cue_no)
		return cue_no

import mido

class Sound:
	def __init__(self):
		self.backend = mido.Backend('mido.backends.rtmidi')
		#self.input = self.backend.open_input('QU-32 MIDI Out')
		self.output = self.backend.open_output('QU-32 MIDI In')
		self.last_message = None
		self.messages = [None]
	def mute(self, channel):
		m = mido.Message('note_on', note=31+channel, velocity=127)
		self.output.send(m)
	def unmute(self, channel):
		m = mido.Message('note_on', note=31+channel, velocity=1)
		self.output.send(m)
	def fader(self, channel, value):
		m1 = mido.Message('control_change', channel=0, control=0x63, value=31+channel)
		m2 = mido.Message('control_change', channel=0, control=0x62, value=0x17)
		m3 = mido.Message('control_change', channel=0, control=0x6, value=value)
		m4 = mido.Message('control_change', channel=0, control=0x26, value=0x7)
		message = [m1, m2, m3, m4]
		for m in message:
			self.output.send(m)
			#ime.sleep(.01)


	def scene(self, scene):
		m = mido.Message('control_change', channel=0, control=0, value=0)
		n = mido.Message('program_change', channel=0, program=scene)
		self.output.send(m)
		#time.sleep(.1)
		self.output.send(n)

	def _get_message(self):
		with self.backend.open_input('QU-32 MIDI Out') as inp:
			for msg in inp:
				print(msg)
				self.messages.append(msg)
	def get_message(self):
		t = threading.Thread(target=self._get_message, daemon=True)
		t.start()
		t.join(timeout=.1)
		#time.sleep(.3)
		return self.messages[-1]

class Lights:
	def __init__(self):
		self.client = Client('192.168.1.38', 3032)
	def cue(self, cue):
		self.client.send_message('/eos/cue/%s/fire' % cue)
