# ------------------------------------------------------------------------------

import sys
import gdata.youtube
import gdata.youtube.service

# ------------------------------------------------------------------------------


class YouTube():
	
	mainmodule = sys.modules['__main__']
	
	credentials = ''
	
	# ------------------------------------------------------------------------------
	
	def __init__(self, credentials):
		print 'YouTube initialsed'
		
		self.credentials = credentials
		self.yt_service = gdata.youtube.service.YouTubeService()
		self.yt_service.ssl = False # The YouTube API does not currently support HTTPS/SSL access.
	
	# ------------------------------------------------------------------------------
	
	def Login(self):
		try:
			self.yt_service.email = self.credentials['email']
			self.yt_service.password = self.credentials['password']
			self.yt_service.source = self.credentials['application']
			
			# dev key & id
			self.yt_service.developer_key = self.credentials['dev_key']
			self.yt_service.client_id = self.credentials['client_id']
			
			self.yt_service.ProgrammaticLogin()
			print 'Logged in!'
		
		except:
			print 'Invalid username or password'
			sys.exit(0)
	
	# ------------------------------------------------------------------------------
	
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
	
	# ------------------------------------------------------------------------------
	
	def GetAndPrintVideoFeed(self, uri):
		try:
			self.feed = self.yt_service.GetYouTubeVideoFeed(uri)
			#self.feed = self.yt_service.GetTopRatedVideoFeed()
		except gdata.service.RequestError, e:
			print 'Error reading feed: %s' % (e[0]['reason'])
			sys.exit(0)
		
		for entry in self.feed.entry:
			try:
				self.PrintEntryDetails(entry)
			except:
				print '--content ignored--'
	
	# ------------------------------------------------------------------------------
	
	def PrintEntryDetails(self, entry):
		self.mainmodule.print_line()
		
		print 'Title:\t\t%s' % entry.media.title.text		
		print 'Published on:\t%s ' % entry.published.text
		print 'ID:\t\t%s' % entry.id.text
		#print 'description: %s' % entry.media.description.text
		print 'Category:\t%s' % entry.media.category[0].text
		#print 'Tags:\t\t%s' % entry.media.keywords.text
		#print 'Watch page:\t%s' % entry.media.player.url
		#print 'Flash URL:\t%s' % entry.GetSwfUrl()
		print 'Duration:\t%s' % entry.media.duration.seconds
		
		# non entry.media attributes
		#print 'geo location: %s' % entry.geo.location() # mostly doesn't exist
		print 'View count:\t%s' % entry.statistics.view_count
		print 'Rating:\t\t%s' % entry.rating.average
		
		# show thumbnails
		#for thumbnail in entry.media.thumbnail:
		#	print 'Thumbnail url:\t%s' % thumbnail.url
			
		# show alternate formats (mostly doesn't exist)
		#for alternate_format in entry.media.content:
		#	if 'isDefault' not in alternate_format.extension_attributes:
		#		print 'Other format:\t%s | url: %s ' % (alternate_format.type, alternate_format.url)
