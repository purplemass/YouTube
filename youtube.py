# ------------------------------------------------------------------------------

import sys
import gdata.youtube
import gdata.youtube.service

# ------------------------------------------------------------------------------


class YouTube():
	
	common = sys.modules['__main__'].common
	
	credentials = []
	tags = []
	test_mode = ''
	
	# ------------------------------------------------------------------------------
	
	def __init__(self, credentials, tags, test_mode):
		self.common.log(1, 'YouTube initialised')
		
		self.credentials = credentials
		self.tags = tags
		self.test_mode = test_mode
		
		self.yt_service = gdata.youtube.service.YouTubeService()
		self.yt_service.ssl = False # The YouTube API does not currently support HTTPS/SSL access.
	
	# ------------------------------------------------------------------------------
	
	def Login(self):
		try:
			self.yt_service.email = self.credentials['username']
			self.yt_service.password = self.credentials['password']
			self.yt_service.source = self.credentials['application']
			
			# dev key
			self.yt_service.developer_key = self.credentials['dev_key']
			
			# no longer required!!
			self.yt_service.client_id = self.credentials['client_id']
			
			self.yt_service.ProgrammaticLogin()
			self.common.log(2, 'Logged into YouTube')
		
		except:
			self.common.log(3, 'Invalid username or password')
			sys.exit(0)


	# ------------------------------------------------------------------------------
	
	def UploadVideo(self, video_file_location):
		self.common.PrintLine()
		self.common.log(2, 'Uploading file:[T][T]%s' % video_file_location)

		# prepare a media group object to hold our video's meta-data
		my_media_group = gdata.media.Group(
			title=gdata.media.Title(text=self.tags['title']),
			description=gdata.media.Description(description_type='plain', text=self.tags['description']),
			keywords=gdata.media.Keywords(text=self.tags['keywords']),
			category=[
					gdata.media.Category(
						text=self.tags['category'],
						scheme='http://gdata.youtube.com/schemas/2007/categories.cat',
						label=self.tags['category']
					)
				],
				player=None
		)
		
		# create the gdata.youtube.YouTubeVideoEntry to be uploaded
		video_entry = gdata.youtube.YouTubeVideoEntry(media=my_media_group)
		
		# developer's tags
		developer_tags = self.tags['developer']
		video_entry.AddDeveloperTags(developer_tags)
		
		# upload				
		try:
			if (not self.test_mode):
				new_entry = self.yt_service.InsertVideoEntry(video_entry, video_file_location)
			
				# should we do this?!!
				upload_status0 = ''
				while True:
					upload_status = self.yt_service.CheckUploadStatus(new_entry) 
					if upload_status is not None:
						video_upload_state = upload_status[0]
						detailed_message = upload_status[1]
						if (upload_status <> upload_status0):
							print video_upload_state, detailed_message
							upload_status0 = upload_status
					time.sleep(1)
					
			
			#self.common.log(2, 'File uploaded:[T][T]%s' % video_file_location)
			self.common.log(2, 'File uploaded')
			ret = True
			
		except gdata.youtube.service.YouTubeError, e:
			self.common.log(3, 'Could not upload file: %s (%s)' % (video_file_location, e[0]['reason']))
			ret = False

		return ret
	
	# ------------------------------------------------------------------------------
	
	def GetDeveloperTagList(self, developer_tag):
		self.common.PrintLine()
		self.common.log(1, 'Looking for developer tag: %s' % developer_tag)
		
		uri = 'http://gdata.youtube.com/feeds/api/videos?category=%7Bhttp%3A%2F%2Fgdata.youtube.com%2Fschemas%2F2007%2Fdevelopertags.cat%7D' + developer_tag
		
		try:
			feed = self.yt_service.GetYouTubeVideoFeed(uri)		
			entry_num = feed.total_results.text
		except gdata.service.RequestError, e:
			self.common.log(3, 'Error reading feed: %s' % (e[0]['reason']))
			entry_num = 0
		
		self.common.log(1, 'Found %s entries with developer tag: %s' % (entry_num, developer_tag))
		
		if (entry_num > 0):
			for entry in feed.entry:
				try:
					self.PrintEntryDetails(entry)
				except:
					self.common.log(1, '--content ignored--')
	
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
		
		print self.feed
		
		for entry in self.feed.entry:
			try:
				self.PrintEntryDetails(entry)
			except:
				self.common.log(1, '--content ignored--')
	
	# ------------------------------------------------------------------------------
	
	def PrintEntryDetails(self, entry):
		self.common.PrintLine()

		self.common.log(1, 'Title:\t%s' % entry.media.title.text)
		self.common.log(1, 'Published on:\t%s ' % entry.published.text)
		self.common.log(1, 'ID:\t\t%s' % entry.id.text)
		self.common.log(1, 'Description:\t%s' % entry.media.description.text)
		self.common.log(1, 'Keywords\t%s' % entry.media.keywords.text)
		self.common.log(1, 'Category:\t%s' % entry.media.category[0].text)
		
		c = 1
		for category in entry.media.category:
			if (c > 1):
				self.common.log(1, 'Dev Tag:\t%s' % category.text)
			c += 1

		self.common.log(1, 'Duration:\t%s' % entry.media.duration.seconds)

	# ------------------------------------------------------------------------------
	# IGNORE BELOW - EXTRA CODE
	# ------------------------------------------------------------------------------
	
		#self.common.log(1, 'Watch page:\t%s' % entry.media.player.url)
		#self.common.log(1, 'Flash URL:\t%s' % entry.GetSwfUrl())
		
		# non entry.media attributes
		# normally not set:
		#self.common.log(1, 'geo location: %s' % entry.geo.location()) # mostly doesn't exist
		#self.common.log(1, 'View count:\t%s' % entry.statistics.view_count)
		#self.common.log(1, 'Rating:\t\t%s' % entry.rating.average)
		
		# show thumbnails
		#for thumbnail in entry.media.thumbnail:
		#	self.common.log(1, 'Thumbnail url:\t%s' % thumbnail.url)
			
		# show alternate formats (mostly doesn't exist)
		#for alternate_format in entry.media.content:
		#	if 'isDefault' not in alternate_format.extension_attributes:
		#		self.common.log(1, 'Other format:\t%s | url: %s ' % (alternate_format.type, alternate_format.url))

# ------------------------------------------------------------------------------

# 					gdata.media.Category(
# 						text='jacqui0',
# 						label='jacqui0',
# 						scheme='http://gdata.youtube.com/schemas/2007/developertags.cat'
# 					),
# 					gdata.media.Category(
# 						text='jacqui1',
# 						label='jacqui1',
# 						scheme='http://gdata.youtube.com/schemas/2007/developertags.cat'
# 					)


		# prepare a geo.where object to hold the geographical location
		# of where the video was recorded
		#where = gdata.geo.Where()
		#where.set_location((37.0,-122.0))
		
		# create the gdata.youtube.YouTubeVideoEntry to be uploaded
		#video_entry = gdata.youtube.YouTubeVideoEntry(media=my_media_group, geo=where)
		
		#print 'DEV TAGS: %s' % video_entry.GetDeveloperTags()

# ------------------------------------------------------------------------------

		# OLDER
		#uri = 'http://gdata.youtube.com/feeds/videos/-/%7Bhttp%3A%2F%2Fgdata.youtube.com%2Fschemas%2F2007%2Fdevelopertags.cat%7D' + developer_tag
		
		# WRONG
		#uri = 'http://gdata.youtube.com/feeds/api/videos/-/%7Bhttp://gdata.youtube.com/schemas/2007/developertags.cat%7D' + developer_tag + '?v=2'
		#uri = 'http://gdata.youtube.com/feeds/api/videos/-/{http://gdata.youtube.com/schemas/2007/developertags.cat}' + developer_tag + '?v=2'
		
		# not sure why these are wrong
		#uri = 'http://gdata.youtube.com/feeds/api/videos/-/%7Bhttp%3A%2F%2Fgdata.youtube.com%2Fschemas%2F2007%2Fdevelopertags.cat%7D' + developer_tag + '?v=2'
		#uri = 'http://gdata.youtube.com/feeds/api/videos?category={http://gdata.youtube.com/schemas/2007/developertags.cat}' + developer_tag + '?v=2'		        
		#uri = 'http://gdata.youtube.com/feeds/api/videos/-/' + developer_tag + '?v=2'
		
# ------------------------------------------------------------------------------
