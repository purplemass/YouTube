# ------------------------------------------------------------------------------

import sys
import gdata.youtube
import gdata.youtube.service

# ------------------------------------------------------------------------------


class YouTube():
	
	common = sys.modules['__main__'].common
	
	credentials = ''
	
	# ------------------------------------------------------------------------------
	
	def __init__(self, credentials):
		self.common.log(1, 'YouTube initialised')

		self.credentials = credentials
		self.yt_service = gdata.youtube.service.YouTubeService()
		self.yt_service.ssl = False # The YouTube API does not currently support HTTPS/SSL access.
	
	# ------------------------------------------------------------------------------
	
	def Login(self):
		try:
			self.yt_service.email = self.credentials['username']
			self.yt_service.password = self.credentials['password']
			self.yt_service.source = self.credentials['application']
			
			# dev key & id
			self.yt_service.developer_key = self.credentials['dev_key']
			self.yt_service.client_id = self.credentials['client_id']
			
			self.yt_service.ProgrammaticLogin()
			self.common.log(2, 'Logged in!')
		
		except:
			self.common.log(3, 'Invalid username or password')
			sys.exit(0)


	# ------------------------------------------------------------------------------
	
	def UploadVideo(self, my_file_name):
		# prepare a media group object to hold our video's meta-data
		my_media_group = gdata.media.Group(
		title=gdata.media.Title(text='My Test Movie'),
		description=gdata.media.Description(description_type='plain', text='My description'),
		keywords=gdata.media.Keywords(text='cars, funny'),
		category=[gdata.media.Category(
			text='Autos',
			scheme='http://gdata.youtube.com/schemas/2007/categories.cat',
			label='Autos')],
			player=None
		)
		
		# prepare a geo.where object to hold the geographical location
		# of where the video was recorded
		where = gdata.geo.Where()
		where.set_location((37.0,-122.0))
		
		# create the gdata.youtube.YouTubeVideoEntry to be uploaded
		video_entry = gdata.youtube.YouTubeVideoEntry(media=my_media_group, geo=where)
		
		# set the path for the video file binary
		video_file_location = my_file_name
		
		# developer's tags
		developer_tags = ['some_tag_01', 'another_tag']
		video_entry.AddDeveloperTags(developer_tags)
		
		# upload
		new_entry = self.yt_service.InsertVideoEntry(video_entry, video_file_location)
		
	# ------------------------------------------------------------------------------
	
	def GetAndPrintSingleVideo(self, my_video_id):
		try:
			self.feed = self.yt_service.GetYouTubeVideoEntry(video_id=my_video_id)
		except gdata.service.RequestError, e:
			self.common.log(3, 'Error reading feed: %s' % (e[0]['reason']))
			sys.exit(0)
		
		#self.common.log(1, self.feed.author[0].name.text)
		
		try:
			self.PrintEntryDetails(self.feed)
		except:
			self.common.log(1, '--content ignored--')
	
	# ------------------------------------------------------------------------------
	
	def GetAndPrintVideoFeed(self, uri):
		try:
			self.feed = self.yt_service.GetYouTubeVideoFeed(uri)
			#self.feed = self.yt_service.GetTopRatedVideoFeed()
		except gdata.service.RequestError, e:
			self.common.log(3, 'Error reading feed: %s' % (e[0]['reason']))
			sys.exit(0)
		
		for entry in self.feed.entry:
			try:
				self.PrintEntryDetails(entry)
			except:
				self.common.log(1, '--content ignored--')
	
	# ------------------------------------------------------------------------------
	
	def PrintEntryDetails(self, entry):
		self.common.PrintLine()
		
		self.common.log(1, 'Title:\t\t%s' % entry.media.title.text)
		self.common.log(1, 'Published on:\t%s ' % entry.published.text)
		self.common.log(1, 'ID:\t\t%s' % entry.id.text)
		#self.common.log(1, 'description: %s' % entry.media.description.text)
		self.common.log(1, 'Category:\t%s' % entry.media.category[0].text)
		#self.common.log(1, 'Tags:\t\t%s' % entry.media.keywords.text)
		#self.common.log(1, 'Watch page:\t%s' % entry.media.player.url)
		#self.common.log(1, 'Flash URL:\t%s' % entry.GetSwfUrl())
		self.common.log(1, 'Duration:\t%s' % entry.media.duration.seconds)
		
		# non entry.media attributes
		#self.common.log(1, 'geo location: %s' % entry.geo.location()) # mostly doesn't exist
		self.common.log(1, 'View count:\t%s' % entry.statistics.view_count)
		self.common.log(1, 'Rating:\t\t%s' % entry.rating.average)
		
		# show thumbnails
		#for thumbnail in entry.media.thumbnail:
		#	self.common.log(1, 'Thumbnail url:\t%s' % thumbnail.url)
			
		# show alternate formats (mostly doesn't exist)
		#for alternate_format in entry.media.content:
		#	if 'isDefault' not in alternate_format.extension_attributes:
		#		self.common.log(1, 'Other format:\t%s | url: %s ' % (alternate_format.type, alternate_format.url))

# ------------------------------------------------------------------------------