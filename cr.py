from osc import Client


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
	def select_previous_cue(self):
		old = self.get_cue_property('selected', 'number')
		self.client.send_message('/select/previous')
		cue_no = self.get_cue_property('selected', 'number')
		print(old, cue_no)
		return cue_no

import mido

class Sound:
	def __init__(self):
		self.backend = mido.Backend('mido.backends.rtmidi')
		#self.input = self.backend.open_input('QU-32 MIDI Out')
		#self.output = self.backend.open_output('QU-32 MIDI In')
		self.header = b'\xF0\x00\x00\x1A\x50\x11\x01\x00\x00'
		self.parser = mido.Parser()
		self.last_message = None
		self.messages = [None]
	def mute(self, channel):
		m = mido.Message('note_on', note=31+channel, velocity=127)
		self.output.send(m)
	def unmute(self, channel):
		m = mido.Message('note_on', note=31+channel, velocity=1)
		self.output.send(m)
	def nrpn(self, parameter, channel, value=0):
		m1 = mido.Message('control_change', channel=0, control=0x63, value=31+channel)
		m2 = mido.Message('control_change', channel=0, control=0x62, value=parameter)
		m3 = mido.Message('control_change', channel=0, control=0x6, value=value)
		m4 = mido.Message('control_change', channel=0, control=0x26, value=0x7)
		message = [m1, m2, m3, m4]
		for m in message:
			self.output.send(m)
			#ime.sleep(.01)
	def fade(self, channel, value):
		self.nrpn(0x17, channel, value)
	def pan(self, channel, value):
		self.nrpn(0x16, channel, value)
	#def mixAssign(self, channel, value):
	#	self.nrpn(0x55, channel, value)

	def scene(self, scene):
		m = mido.Message('control_change', channel=0, control=0, value=0)
		n = mido.Message('program_change', channel=0, program=scene)
		self.output.send(m)
		#time.sleep(.1)
		self.output.send(n)

	def meters(self):
		self.parser.feed(self.header+b'\x10\x00\xF7')
		return self.parser.get_message()

	def name(self, channel, name=None):
		if name: # set name
			self.parser.feed(self.header + b'\x03' + channel.encode() + name.encode() + b'\xF7')
		else: # get name
			self.parser.feed(self.header + b'\x03' + channel.encode() + name.encode() + b'\xF7')
			self.output.send(self.parser.get_message())
			self.get_message()

	def _get_message(self):
		with self.backend.open_input('QU-32 MIDI Out') as inp:
			for msg in inp:
				print(msg)
				self.messages.append(msg)
	def get_message(self):

		t = Process(target=self._get_message, daemon=True)
		t.start()
		t.join(timeout=.1)
		#time.sleep(.3)
		return self.messages[-1]

class Lights:
	def __init__(self):
		self.client = Client('192.168.1.38', 3032)
	def cue(self, cue):
		self.client.send_message('/eos/cue/%s/fire' % cue)
