import mido
import time

HEADER = b'\xF0\x00\x00\x1A\x50\x11\x01\x00\x7F\x10\x00\xF7'


r = mido.Backend('mido.backends.rtmidi')
m = mido.Message('sysex', data=bytearray(HEADER))
print(m)
#o = r.open_output()

def mute(channel):
	m = mido.Message.from_hex('')


#with r.open_input() as i:
#	for msg in i:
#		start = time.perf_counter()
#		print(i)
