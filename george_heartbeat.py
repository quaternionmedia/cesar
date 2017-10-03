import os
import logging
import datetime
import shutil

home = '//Users/peterkagstrom/Dropbox/george'

def touchDirectory(path):
	if not os.path.isdir(path):
		os.mkdir(path)

def traverseDirectory(rootDir='//'):
	logging.info('Starting directory traverse on ' + rootDir)
	for dirpath, dirnames, filenames in os.walk(rootDir):
		logging.debug('Found directory: %s' % dirpath + ', and it consumes ' + str(sum(os.path.getsize(os.path.join(dirpath, name)) for name in filenames)) + ' bytes in ' + str(len(filenames)) + ' non-directory files')
		for fname in filenames:
			logging.debug('\t%s' % fname)

def copyFile(src,dest):
	shutil.copyfile(src,dest)

if __name__ == '__main__':
	#run system and network discovery
	#
	#System Discovery
	touchDirectory(home)
	#setup logging (logging.debug, info, warning, error, critical)

	logpath = home + '/glogs'
	touchDirectory(logpath)
	logname = logpath + '/' + str(datetime.datetime.now()) + '.glog'

	logging.basicConfig(filename=logname, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)


	traverseDirectory(home)

	#establish connection with george heartbeat

	#if no connection, start internal heartbeat Server

	#register functions with active heartbeat Server
