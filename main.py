# ------------------------------------------------------------------------------
# import
# ------------------------------------------------------------------------------

import sys
import time
from datetime import datetime

import yaml

# ------------------------------------------------------------------------------
# get settings
# ------------------------------------------------------------------------------

date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

error = False
running = True
settings_file = 'settings.yaml'

try:
	f = open(settings_file)
except:
	print 'ERROR: Cannot open %s' % settings_file
	error = True

try:
	settings = yaml.load(f)
except:
	print 'ERROR: Cannot load YAML file'
	error = True

try:
	f.close()
except:
	print 'ERROR: Cannot close %s' % settings_file
	error = True

# ------------------------------------------------------------------------------
# process settings
# ------------------------------------------------------------------------------

if (not error):
	# main vars
	paths = settings['paths']
	application = settings['application']
	credentials = settings['credentials']
	tags = settings['tags']
	gmail = settings['gmail']
	
	pause_time = application['pause_time']
	pause_time_quota = application['pause_time_quota']
	test_mode = application['test_mode']
	
	youtube_feed = settings['youtube_feed'] % credentials['username']
	
else:
	sys.exit('Existing program')

# ------------------------------------------------------------------------------
# import our classes
# ------------------------------------------------------------------------------

import commonops
common = commonops.CommonOps(application, gmail)

import fileops
import youtube

# ------------------------------------------------------------------------------
# Main program
# ------------------------------------------------------------------------------

#common.Mail('Test email', settings['gmail'])
#sys.exit(0)

if (__name__ == '__main__'):
	youtube = youtube.YouTube(credentials, application, tags)	

	# if arg is list then list all videos for our 
	# YouTube account - then exit
	#
	try:
		arg = sys.argv[1]		
	except:
		arg = ''
	
	if arg == 'list':
		#youtube.GetDeveloperTagList('imag_dev')
		youtube.GetAndPrintVideoFeed(youtube_feed)
		sys.exit('Exiting program')
	
 	youtube.Login()
	fileops = fileops.FileOps(paths, application)
	
	while running:
		common.PrintLine(True)
		
		# write date/time
		date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		common.log(1, 'Date/Time:[T][T]%s' % date_time)
				
		file_name = fileops.ProcessFolder()	
		
		if (file_name == False):
			time.sleep(pause_time)
		else:
			ret = youtube.UploadVideo(paths['local_incoming'] + file_name)
			if (ret != 'uploaded'):
				common.log(3, 'Error (%s) when uploading video %s' % (ret, file_name))
						
			if (ret == 'uploaded'):
				ret = fileops.ArchiveFile(file_name, False)
			
			elif (ret == 'rejected'):
				ret = fileops.ArchiveFile(file_name, True)
				body = gmail['rejected_body'] % (file_name)
				common.Mail('%s' % body)
			
			elif (ret == 'too_many_recent_calls'):
				body = gmail['quota_body'] % (file_name, (pause_time_quota/60))
				common.Mail('%s' % body)
				common.log(2, '... waiting for %s minutes to reset YouTube quota ...' % (pause_time_quota/60))
				time.sleep(pause_time_quota)
			
			else:
				ret = fileops.ArchiveFile(file_name, False)
			
		time.sleep(2)

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
# code may be used later:
# ------------------------------------------------------------------------------

	#youtube_feed = 'http://gdata.youtube.com/feeds/api/users/FocusCamTest/uploads/mgOKxPAOg2g'
	#youtube_feed = 'http://gdata.youtube.com/feeds/api/users/default/uploads/Pu43mzXcw9Q' #mgOKxPAOg2g
	#youtube_feed = '%s/Pu43mzXcw9Q' % youtube_feed		

	# show tagged videos for testing:	
	#youtube.GetDeveloperTagList(tags['developer'][0])
	
	# get all videos
	#youtube.GetAndPrintVideoFeed(youtube_feed)
	#sys.exit()
	
	# get a single video
	#youtube.GetAndPrintSingleVideo('Glny4jSciVI')


# ------------------------------------------------------------------------------
