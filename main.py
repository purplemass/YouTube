# ------------------------------------------------------------------------------

#http://code.google.com/apis/youtube/1.0/developers_guide_python.html
#http://code.google.com/apis/youtube/2.0/developers_guide_protocol_video_feeds.html
#http://gdata-python-client.googlecode.com/svn/trunk/pydocs/gdata.youtube.html

# ------------------------------------------------------------------------------

import sys
import gdata.youtube
import gdata.youtube.service

# ------------------------------------------------------------------------------

email = 'bob_ak@hotmail.com'
pw = 'beats4me'

username = 'eaglerocktv' #default

application = 'my-example-application'

dev_key = 'AI39si7d7xVRmwtUXlhRXWtDs5NQhBNbq7xfLW4ZtIx74yU9Azs0XLCrPTKr60uN-X8juceJpjThVpoVeal-1FT-INJwm7OccQ'
client_id = 'purplemass'

youtube_feed = 'http://gdata.youtube.com/feeds/api/users/%s/uploads' % username

# ------------------------------------------------------------------------------

class YouTube():

	def __init__(self):
		self.yt_service = gdata.youtube.service.YouTubeService()
		self.yt_service.ssl = False # The YouTube API does not currently support HTTPS/SSL access.
		self.yt_service.email = email
		self.yt_service.password = pw
		self.yt_service.source = application
		
		# dev key & id
		self.yt_service.developer_key = dev_key
		self.yt_service.client_id = client_id

		print 'YouTube initialsed'
		pass
	
	def Login(self):
		try:
			self.yt_service.ProgrammaticLogin()
			print 'Logged in!'
		
		except:
			print 'Invalid username or password'
			sys.exit(0)

	def GetAndPrintSingleVideo(self, my_video_id):
		try:
			self.feed = self.yt_service.GetYouTubeVideoEntry(video_id=my_video_id)
		except gdata.service.RequestError, e:
			print 'Error reading feed: %s' % (e[0]['reason'])
			sys.exit(0)
		
		#print self.feed.author[0].name.text
		
		try:
			self.PrintEntryDetails(self.feed)
		except:
			print '--content ignored--'
		
	def GetAndPrintVideoFeed(self, uri):
		try:
			self.feed = self.yt_service.GetYouTubeVideoFeed(uri)
			#self.feed = self.yt_service.GetTopRatedVideoFeed()
		except gdata.service.RequestError, e:
			print 'Error reading feed: %s' % (e[0]['reason'])
			sys.exit(0)
		
		for entry in self.feed.entry:
			try:
				self.PrintEntryDetails(self.entry)
			except:
				print '--content ignored--'

	def PrintEntryDetails(self, entry):
		print '--------------------------------------------------------------------------'
		#print entry
		print 'Title:\t\t%s' % entry.media.title.text
		
		print 'ID:\t\t%s' % entry.id.text
# 		print 'Author:\t %s' % entry.uri
		
		print 'Published on:\t%s ' % entry.published.text
		#print 'description: %s' % entry.media.description.text
		print 'Category:\t%s' % entry.media.category[0].text
		print 'Tags:\t\t%s' % entry.media.keywords.text
		print 'Watch page:\t%s' % entry.media.player.url
		print 'Flash URL:\t%s' % entry.GetSwfUrl()
		print 'Duration:\t%s' % entry.media.duration.seconds
		
		# non entry.media attributes
		#print 'geo location: %s' % entry.geo.location() # mostly doesn't exist
		print 'View count:\t%s' % entry.statistics.view_count
		print 'Rating:\t\t%s' % entry.rating.average
		
		# show thumbnails
		for thumbnail in entry.media.thumbnail:
			print 'Thumbnail url:\t%s' % thumbnail.url

		
		# show alternate formats (mostly doesn't exist)
		for alternate_format in entry.media.content:
			if 'isDefault' not in alternate_format.extension_attributes:
				print 'Other format:\t%s | url: %s ' % (alternate_format.type,
		                                         alternate_format.url)
		
# ------------------------------------------------------------------------------
# START HERE

print '==============================='

youtube = YouTube();
#youtube.Login();
#youtube.GetAndPrintVideoFeed(youtube_feed)
youtube.GetAndPrintSingleVideo('Glny4jSciVI')

print '==============================='

# ------------------------------------------------------------------------------