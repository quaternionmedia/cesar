from __future__ import print_function
import serial, sys
import logging

START_VAL = 0x7E
END_VAL = 0xE7

COM_BAUD = 57600
COM_TIMEOUT = 1
COM_PORT = 7
DMX_SIZE = 512

LABELS = {
    'GET_WIDGET_PARAMETERS': 3,  # unused
    'SET_WIDGET_PARAMETERS': 4,  # unused
    'RX_DMX_PACKET': 5,  # unused
    'TX_DMX_PACKET': 6,
    'TX_RDM_PACKET_REQUEST': 7,  # unused
    'RX_DMX_ON_CHANGE': 8,  # unused
}


class DMXConnection( object ):
    auto_render = False

    def __init__( self, comport=None, autorender=False ):
        '''
        On Windows, the only argument is the port number. On *nix, it's the path to the serial device.
        For example:
            DMXConnection(4)              # Windows
            DMXConnection('/dev/tty2')    # Linux
            DMXConnection("/dev/ttyUSB0") # Linux
        '''
        self.dmx_frame = [ 0 ] * DMX_SIZE
        self.auto_render = autorender
        try:
            self.com = serial.Serial( comport, baudrate=COM_BAUD, timeout=COM_TIMEOUT )
        except:
            com_name = 'COM%s' % (comport + 1) if type( comport ) == int else comport
            logging.error( "Could not open device %s. Quitting application." % com_name )
            # sys.exit(0)

        logging.info( "Opened %s." % (self.com.portstr) )

    def setChannel( self, chan, val, autorender=False ):
        '''
        Takes channel and value arguments to set a channel level in the local
        DMX frame, to be rendered the next time the render() method is called.
        '''
        if chan < 1 or chan > DMX_SIZE:
            logging.error( 'Invalid channel specified: ',  chan )
            return
        # clamp value
        val = max( 0, min( val, 255 ) )
        self.dmx_frame[ chan - 1 ] = val
        if autorender or self.auto_render:
            self.render( )

    def clear( self, chan=0 ):
        '''
        Clears all channels to zero. blackout.
        With optional channel argument, clears only one channel.
        '''
        if chan == 0:
            self.dmx_frame = [ 0 ] * DMX_SIZE
        else:
            self.dmx_frame[ chan - 1 ] = 0

    def render( self ):
        ''''
        Updates the DMX output from the USB DMX Pro with the values from self.dmx_frame.
        '''
        packet = [ START_VAL, LABELS[ 'TX_DMX_PACKET' ], len( self.dmx_frame ) & 0xFF,
                                                         (len( self.dmx_frame ) >> 8) & 0xFF, ]
        packet += self.dmx_frame
        packet.append( END_VAL )

        data = bytearray(packet)

        logging.debug( packet )
        logging.debug( data )
        self.com.write( data )

    def close( self ):
        self.com.close( )

# import serial, sys, time
#
#
# DMXOPEN = chr(126)
# DMXCLOSE = chr(231)
# DMXINTENSITY=chr(6)+chr(1)+chr(2)
# DMXINIT1= chr(03)+chr(02)+chr(0)+chr(0)+chr(0)
# DMXINIT2= chr(10)+chr(02)+chr(0)+chr(0)+chr(0)
#
# class DmxPy:
# 	def __init__(self, serialPort):
# 		try:
# 			self.serial=serial.Serial(serialPort, baudrate=57600)
# 		except:
# 			print "Error: could not open Serial Port"
# 			sys.exit(0)
# 		self.serial.write( DMXOPEN+DMXINIT1+DMXCLOSE)
# 		self.serial.write( DMXOPEN+DMXINIT2+DMXCLOSE)
#
# 		self.dmxData=[chr(0)]*513   #128 plus "spacer".
#
# 	def setChannel(self, chan, intensity):
# 		if chan > 512 : chan = 512
# 		if chan < 0 : chan = 0
# 		if intensity > 255 : intensity = 255
# 		if intensity < 0 : intensity = 0
# 		self.dmxData[chan] = chr(intensity)
#
# 	def blackout(self):
# 		for i in xrange (1, 512, 1):
# 			self.dmxData[i] = chr(0)
#
# 	def render(self):
# 		sdata=''.join(self.dmxData)
# 		self.serial.write(DMXOPEN+DMXINTENSITY+sdata+DMXCLOSE)
