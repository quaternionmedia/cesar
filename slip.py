
END = b'\xc0'
ESC = b'\xdb'
ESC_END = b'\xdc'
ESC_ESC = b'\xdd'
NULL = b'\x00'

#
# def encode(msg):
# 	"""encode(msg) -> SLIP-encoded message.
# 	"""
# 	print('encoding: ', msg)
# 	msg = bytes(msg, 'UTF-8')
# 	encoded = END + msg.replace(ESC, ESC+ESC_ESC).replace(END, ESC+ESC_END) + END
# 	print(encoded)

def encode(packet):
	encoded = END
	for char in packet:
		# SLIP_END
		if char == END:
			encoded +=  ESC + ESC_END
		# SLIP_ESC
		elif char == ESC:
			encoded += ESC + ESC_ESC
		# the rest can simply be appended
		else:
			encoded += char.encode()
	print('encoding: ', encoded, (len(encoded)-1) % 4)
	#encoded += NULL * (4 - (len(encoded)+1) % 4)
	#encoded += NULL * ((len(encoded)+1)%4)
	encoded += NULL * ((len(encoded) % 4 )+ 3)
	encoded += END
	print('encoded! ', encoded, len(encoded) % 4)
	return encoded
