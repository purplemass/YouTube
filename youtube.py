# ------------------------------------------------------------------------------

import sys
import gdata.youtube
import gdata.youtube.service

# ------------------------------------------------------------------------------


class YouTube():
	
	common = sys.modules['__main__'].common
	
	credentials = []
	tags = []
	
	# ------------------------------------------------------------------------------
	
	def __init__(self, credentials, tags):
		self.common.log(1, 'YouTube initialised')
		
		self.credentials = credentials
		self.tags = tags
		
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
			#self.yt_service.client_id = self.credentials['client_id']
			
			self.yt_service.ProgrammaticLogin()
			self.common.log(2, 'Logged in!')
		
		except:
			self.common.log(3, 'Invalid username or password')
			sys.exit(0)


	# ------------------------------------------------------------------------------
	
	def UploadVideo(self, my_file_name):
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
					),
					gdata.media.Category(
						text='jacqui0',
						label='jacqui0',
						scheme='http://gdata.youtube.com/schemas/2007/developertags.cat'
					),
					gdata.media.Category(
						text='jacqui1',
						label='jacqui1',
						scheme='http://gdata.youtube.com/schemas/2007/developertags.cat'
					)
				],
				player=None
		)
		
		# prepare a geo.where object to hold the geographical location
		# of where the video was recorded
		#where = gdata.geo.Where()
		#where.set_location((37.0,-122.0))
		
		# create the gdata.youtube.YouTubeVideoEntry to be uploaded
		video_entry = gdata.youtube.YouTubeVideoEntry(media=my_media_group) #, geo=where
		
		# set the path for the video file binary
		video_file_location = my_file_name
		
		# developer's tags
# 		print 'DEV TAGS: %s' % video_entry.GetDeveloperTags()
		
		developer_tags = self.tags['developer'] #[self.tags['developer'][0]] #
		video_entry.AddDeveloperTags(developer_tags)
		
# 		print 'DEV TAGS: %s' % video_entry.GetDeveloperTags()
# 		print '+++++++++++++++++++++++++++++++++++++++++++++++++++'
# 		print video_entry
# 		print '+++++++++++++++++++++++++++++++++++++++++++++++++++'
		
		# upload
		self.common.log(2, 'Uploading file: %s' % video_file_location)
		
		new_entry = self.yt_service.InsertVideoEntry(video_entry, video_file_location)
# 		while True: 
# 			upload_status = self.yt_service.CheckUploadStatus(new_entry) 
# 			if upload_status is not None:
# 				video_upload_state = upload_status[0]
# 				detailed_message = upload_status[1]
# 				print video_upload_state, detailed_message
		
 		sys.exit()
		
		try:
			new_entry = self.yt_service.InsertVideoEntry(video_entry, video_file_location)
			self.common.log(2, 'File uploaded: %s' % video_file_location)
			ret = True
		except gdata.youtube.service.YouTubeError, e:
			self.common.log(3, 'Could not upload file: %s (%s)' % (video_file_location, e[0]['reason']))
			ret = False

		return ret
	
	# ------------------------------------------------------------------------------
	
	def GetDeveloperTagList(self, developer_tag):
		self.common.log(1, 'Looking for developer tag: %s' % developer_tag)
		
		self.yt_service.source = self.credentials['application']
		self.yt_service.client_id = self.credentials['client_id']
		self.yt_service.developer_key = self.credentials['dev_key']
		
		developer_tag = 'jacqui123'
		
		# ALL
		#uri = 'http://gdata.youtube.com/feeds/api/videos/-/' + developer_tag + '?v=2'
		
		# OLDER
		uri = 'http://gdata.youtube.com/feeds/videos/-/%7Bhttp%3A%2F%2Fgdata.youtube.com%2Fschemas%2F2007%2Fdevelopertags.cat%7D' + developer_tag
		
		# NEW
		#uri = 'http://gdata.youtube.com/feeds/api/videos/-/%7Bhttp%3A%2F%2Fgdata.youtube.com%2Fschemas%2F2007%2Fdevelopertags.cat%7D' + developer_tag + '?v=2'
		#uri = 'http://gdata.youtube.com/feeds/api/videos?category=%7Bhttp%3A%2F%2Fgdata.youtube.com%2Fschemas%2F2007%2Fdevelopertags.cat%7D' + developer_tag
		#uri = 'http://gdata.youtube.com/feeds/api/videos?category={http://gdata.youtube.com/schemas/2007/developertags.cat}' + developer_tag + '?v=2'		        
		
		# WRONG
		#uri = 'http://gdata.youtube.com/feeds/api/videos/-/%7Bhttp://gdata.youtube.com/schemas/2007/developertags.cat%7D' + developer_tag + '?v=2'
		#uri = 'http://gdata.youtube.com/feeds/api/videos/-/{http://gdata.youtube.com/schemas/2007/developertags.cat}' + developer_tag + '?v=2'

						
		#print self.yt_service.GetYouTubeVideoFeed(uri)
	
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
	
# 		entry = self.yt_service.GetYouTubeVideoEntry(uri)
# 		upload_status = self.yt_service.CheckUploadStatus(None, 'Pu43mzXcw9Q')
# 		print upload_status
# 		if upload_status is not None:
# 			video_upload_state = upload_status[0]
# 			detailed_message = upload_status[1]
# 		else:
# 			return False
# 		
		
		try:
			self.feed = self.yt_service.GetYouTubeVideoFeed(uri)
			#self.feed = self.yt_service.GetTopRatedVideoFeed()
		except gdata.service.RequestError, e:
			self.common.log(3, 'Error reading feed: %s' % (e[0]['reason']))
			sys.exit(0)
		
		print self.feed
		
		for entry in self.feed.entry:
			print entry
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