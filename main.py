# ------------------------------------------------------------------------------

import sys

import fileops
import youtube
import yaml

# ------------------------------------------------------------------------------
# FUNCTIONS
# ------------------------------------------------------------------------------

def print_line(double=False):
	if (double):
		print '=========================================================================='
	else:
		print '--------------------------------------------------------------------------'

# ------------------------------------------------------------------------------

def log(priority, msg):
	if priority == 3:
		error = 'ERROR '
	else:
		error = ''
	
	print '%s%s' % (error, msg)
	
# ------------------------------------------------------------------------------
# START HERE
# ------------------------------------------------------------------------------

# get settings

error = False
settings_file = 'settings.yaml'

try:
	f = open(settings_file)
except:
	log(3, 'Cannot open %s' % settings_file)
	error = True

try:
	settings = yaml.load(f)
except:
	log(3, 'Cannot load YAML')
	error = True

try:
	f.close()
except:
	log(3, 'Cannot close file %s' % settings_file)
	error = True

if (not error):
	credentials = settings['credentials']
	youtube_feed = settings['youtube_feed'] % credentials['username']
	server_path = settings['server_path']
else:
	sys.exit('Existing program')

# ------------------------------------------------------------------------------
# Main program

print_line(True)

if (__name__ == '__main__'):
	fileops = fileops.FileOps(server_path)
	fileops.scanFolder()
	
	youtube = youtube.YouTube(credentials)
	youtube.Login()
	
	#youtube.UploadVideo('%s%s' % (server_path, 'jumps.mov'))
	
	youtube.GetAndPrintVideoFeed(youtube_feed)
	#youtube.GetAndPrintSingleVideo('Glny4jSciVI')

print_line(True)

# ------------------------------------------------------------------------------
# reference:
# ------------------------------------------------------------------------------

"""
http://code.google.com/apis/youtube/1.0/developers_guide_python.html
http://code.google.com/apis/youtube/2.0/developers_guide_protocol_video_feeds.html
http://gdata-python-client.googlecode.com/svn/trunk/pydocs/gdata.youtube.html


PyYaml:
http://mikkel.elmholdt.dk/?p=4

# write file
f = open('newtree.yaml', "w")
yaml.dump(settings, f)
f.close()

"""
# ------------------------------------------------------------------------------
