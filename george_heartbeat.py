import os
import logging
import datetime

home = '//Users/peterkagstrom/Dropbox/george'

def touchDirectory(path):
	if not os.path.isdir(path):
		os.mkdir(path)

def traverseDirectory(rootDir='//'):
	logging.debug('Starting directory traverse on ' + rootDir)
	for dirpath, dirnames, filenames in os.walk(rootDir):
		logging.debug('Found directory: %s' % dirpath)
		logging.debug(str(dirpath) + " consumes ")
		logging.debug(str(sum(os.path.getsize(os.path.join(dirpath, name)) for name in filenames)))
		logging.debug('bytes in ' + str(len(filenames)) +
		' non-directory files')
		for fname in filenames:
			logging.debug('\t%s' % fname)

if __name__ == '__main__':
	#run system and network discovery
	#
	#System Discovery
	touchDirectory(home)
	#setup logging

	logpath = home + '/glogs'
	touchDirectory(logpath)
	logname = logpath + '/' + str(datetime.datetime.now())

	logging.basicConfig(filename=logname, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)


	traverseDirectory(home)

	#establish connection with george heartbeat

	#if no connection, start internal heartbeat Server

	#register functions with active heartbeat Server
