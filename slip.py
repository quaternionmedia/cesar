
END = b'\xc0'
ESC = b'\xdb'
ESC_END = b'\xdc'
ESC_ESC = b'\xdd'

#
# def encode(msg):
# 	"""encode(msg) -> SLIP-encoded message.
# 	"""
# 	print('encoding: ', msg)
# 	msg = bytes(msg, 'UTF-8')
# 	encoded = END + msg.replace(ESC, ESC+ESC_ESC).replace(END, ESC+ESC_END) + END
# 	print(encoded)

def encode(packet):
	# Encode an initial END character to flush out any data that
	# may have accumulated in the receiver due to line noise
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
			encoded += bytes(char, 'UTF-8')	
	encoded += END
	return encoded
