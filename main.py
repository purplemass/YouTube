# ------------------------------------------------------------------------------
# import
# ------------------------------------------------------------------------------

import sys
import time

import commonops
common = commonops.CommonOps()

import fileops
import youtube
import yaml

# ------------------------------------------------------------------------------
# get settings
# ------------------------------------------------------------------------------

error = False
settings_file = 'settings.yaml'

try:
	f = open(settings_file)
except:
	common.log(3, 'Cannot open %s' % settings_file)
	error = True

try:
	settings = yaml.load(f)
except:
	common.log(3, 'Cannot load YAML')
	error = True

try:
	f.close()
except:
	common.log(3, 'Cannot close file %s' % settings_file)
	error = True

# ------------------------------------------------------------------------------
# process settings
# ------------------------------------------------------------------------------

if (not error):
	pause_time = settings['pause_time']
	credentials = settings['credentials']
	youtube_feed = settings['youtube_feed'] % credentials['username']
	server_path = settings['server_path']
	movie_extension = settings['movie_extension']
else:
	sys.exit('Existing program')

# ------------------------------------------------------------------------------
# Main program
# ------------------------------------------------------------------------------

if (__name__ == '__main__'):

	fileops = fileops.FileOps(server_path)
	youtube = youtube.YouTube(credentials)
	
	while common.running:
		
		common.PrintLine(True)
		
		fileops.ProcessFolder()
		
		#youtube.Login()
		
		#youtube.UploadVideo('%s%s' % (server_path, 'jumps.mov'))
		
		#youtube.GetAndPrintVideoFeed(youtube_feed)
		#youtube.GetAndPrintSingleVideo('Glny4jSciVI')

		time.sleep(pause_time)

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
