
END = b'\xc0'
ESC = b'\xdb'
ESC_END = b'\xdc'
ESC_ESC = b'\xdd'
NULL = b'\x00'


def encode(packet):
	encoded = END
	for char in packet:
		if char == END:
			encoded +=  ESC + ESC_END
		elif char == ESC:
			encoded += ESC + ESC_ESC
		else:
			encoded += char.encode()
	#print('encoding: ', encoded, (len(encoded)-1) % 4)
	#encoded += NULL * (4 - (len(encoded)+1) % 4)
	#encoded += NULL * ((len(encoded)+1)%4)
	encoded += NULL * ((len(encoded) % 4 )+ 3)
	encoded += END
	#print('encoded! ', encoded, len(encoded) % 4)
	return encoded
