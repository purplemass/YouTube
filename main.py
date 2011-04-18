# ------------------------------------------------------------------------------

import sys

import fileops
import youtube
import yaml

# ------------------------------------------------------------------------------
# get settings

f = open('settings.yaml')
settings = yaml.load(f)
f.close()

credentials = settings['credentials']
youtube_feed = settings['youtube_feed'] % credentials['username']
server_path = settings['server_path']

# ------------------------------------------------------------------------------

def print_line(double=False):
	if (double):
		print '=========================================================================='
	else:
		print '--------------------------------------------------------------------------'

# ------------------------------------------------------------------------------
# START HERE

print_line(True)

if (__name__ == '__main__'):
	fileops = fileops.FileOps(server_path)
	fileops.scanFolder()
	#youtube = youtube.YouTube(credentials);
	
	#youtube.Login();
	#youtube.GetAndPrintVideoFeed(youtube_feed)
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
