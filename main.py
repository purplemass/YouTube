# ------------------------------------------------------------------------------

import sys
import youtube

# ------------------------------------------------------------------------------

parameters = {
	'email':		'bob_ak@hotmail.com',
	'password':		'beats4me',
	'username':		'eaglerocktv', #default
	'application':	'my-example-application',
	'dev_key':		'AI39si7d7xVRmwtUXlhRXWtDs5NQhBNbq7xfLW4ZtIx74yU9Azs0XLCrPTKr60uN-X8juceJpjThVpoVeal-1FT-INJwm7OccQ',
	'client_id':	'purplemass'
}

youtube_feed = 'http://gdata.youtube.com/feeds/api/users/%s/uploads' % parameters['username']
		
# ------------------------------------------------------------------------------
# START HERE

print '=========================================================================='

youtube = youtube.YouTube(parameters);

#youtube.Login();
#youtube.GetAndPrintVideoFeed(youtube_feed)

youtube.GetAndPrintSingleVideo('Glny4jSciVI')

print '=========================================================================='

# ------------------------------------------------------------------------------

# reference:

#http://code.google.com/apis/youtube/1.0/developers_guide_python.html
#http://code.google.com/apis/youtube/2.0/developers_guide_protocol_video_feeds.html
#http://gdata-python-client.googlecode.com/svn/trunk/pydocs/gdata.youtube.html

# ------------------------------------------------------------------------------
