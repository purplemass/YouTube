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
	paths = settings['paths']
	movie_extension = settings['movie_extension']
	
	pause_time = settings['pause_time']
	
	credentials = settings['credentials']
	tags = settings['tags']
	test_mode = settings['test_mode']
	youtube_feed = settings['youtube_feed'] % credentials['username']
	
	#youtube_feed = 'http://gdata.youtube.com/feeds/api/users/FocusCamTest/uploads/mgOKxPAOg2g'
	#youtube_feed = 'http://gdata.youtube.com/feeds/api/users/default/uploads/Pu43mzXcw9Q' #mgOKxPAOg2g
	#youtube_feed = '%s/Pu43mzXcw9Q' % youtube_feed
		
else:
	sys.exit('Existing program')

# ------------------------------------------------------------------------------
# Main program
# ------------------------------------------------------------------------------

if (__name__ == '__main__'):

	fileops = fileops.FileOps(paths, movie_extension)
	youtube = youtube.YouTube(credentials, tags, test_mode)
	
	youtube.Login()
	
	# show tagged videos for testing:	
	youtube.GetDeveloperTagList(tags['developer'][0])
	
	# get all videos
	#youtube.GetAndPrintVideoFeed(youtube_feed)
	#sys.exit()
	
	# get a single video
	#youtube.GetAndPrintSingleVideo('Glny4jSciVI')

	while common.running:
		
		common.PrintLine(True)
				
		file_name = fileops.ProcessFolder()	
		if (file_name == False):
			time.sleep(pause_time)
		else:
			ret = youtube.UploadVideo(paths['incoming'] + file_name)
			if (ret):
				ret = fileops.DeleteFile(paths['server'] + file_name)
				if (ret):
					ret = fileops.ArchiveFile(file_name)
		
		time.sleep(1)

# ------------------------------------------------------------------------------
# reference:
# ------------------------------------------------------------------------------

"""
http://code.google.com/apis/youtube/1.0/developers_guide_python.html
http://code.google.com/apis/youtube/2.0/developers_guide_protocol_video_feeds.html
http://gdata-python-client.googlecode.com/svn/trunk/pydocs/gdata.youtube.html

Dev Tag Issue?:
http://markmail.org/thread/ekb6zmuwrnlk2tvd
http://groups.jonzu.com/z_apis_adding-developer-tags.html#comments
http://stackoverflow.com/questions/3677453/youtube-api-php-retrieving-a-private-video-under-my-account
http://gdata.youtube.com/demo/

Quota
http://apiblog.youtube.com/2010/02/best-practices-for-avoiding-quota.html

PyYaml:
http://mikkel.elmholdt.dk/?p=4

# write file
f = open('newtree.yaml', "w")
yaml.dump(settings, f)
f.close()

"""
# ------------------------------------------------------------------------------
