# ------------------------------------------------------------------------------

import sys
import time
from datetime import datetime
import gdata.youtube
import gdata.youtube.service

# ------------------------------------------------------------------------------

class YouTube():
	
	# ------------------------------------------------------------------------------
	
	def __init__(self, credentials, application, tags):
		self.common = sys.modules['__main__'].common
		
		self.pause_time_status = 5
		
		self.credentials = credentials
		self.tags = tags
		self.check_status = application['check_status']
		self.dev_tag_to_key = application['dev_tag_to_key']
		self.test_mode = application['test_mode']
		self.pattern_in_file = application['pattern_in_file']
		
		self.yt_service = gdata.youtube.service.YouTubeService()
		self.yt_service.ssl = False # The YouTube API does not currently support HTTPS/SSL access.

		self.common.log(1, 'YouTube initialised')
	
	# ------------------------------------------------------------------------------
	
	def Login(self):
		try:
			self.yt_service.email = self.credentials['username']
			self.yt_service.password = self.credentials['password']
			self.yt_service.source = self.credentials['application']
			
			# dev key
			self.yt_service.developer_key = self.credentials['dev_key']
			
			# this is no no longer required!!
			self.yt_service.client_id = self.credentials['client_id']
			
			self.yt_service.ProgrammaticLogin()
			self.common.log(2, 'Logged in as %s' % self.credentials['username'])
		
		except:
			self.common.log(3, 'Invalid username or password')
			sys.exit(0)

	# ------------------------------------------------------------------------------
	
	def Get_Date_Time(self, filename):
		# find pattern in filename
		n = filename.find(self.pattern_in_file)
		
		if (n > -1):
			# based on filename: FocusCam_02052011_1720
			n = n + len(self.pattern_in_file)
			
			date = filename[n:n+8]
			my_date = date[4:8] + date[2:4] + date[0:2]
			my_date_dashes = date[0:2] + '-' + date[2:4] + '-' + date[4:8]
			my_time = filename[n+9:n+13]
			my_time_dashed = filename[n+9:n+11] + ':' + filename[n+11:n+13]
		else:
			# based on current time
			now = datetime.now()
			my_date = now.strftime("%Y%m%d")
			my_date_dashes = now.strftime("%d-%m-%Y")
			my_time = now.strftime("%H%M")
			my_time_dashed = now.strftime("%H:%M")
		
		hours = my_time[0:2]
		minutes = my_time[2:4]
		if int(minutes) < 30:
			minutes = '00'
		else:
			minutes = '30'
		
		my_time_slot = '%s%s' % (hours, minutes)
		
		return (my_date, my_date_dashes, my_time, my_time_dashed, my_time_slot)
	
	# ------------------------------------------------------------------------------
	
	def UploadVideo(self, video_file_location):
		#
		# return: uploaded, rejected, error
		#
		self.common.PrintLine()
		self.common.log(2, 'Uploading file:[T][T]%s' % video_file_location)
		
		(my_date, my_date_dashes, my_time, my_time_dashed, my_time_slot) = self.Get_Date_Time(video_file_location)
		
		video_title = self.tags['title']
		video_title = video_title.replace('yyyymmdd', my_date_dashes)
		video_title = video_title.replace('hhmm', my_time_dashed)

		# prepare developer's tags
		developer_tags = self.tags['developer']
		new_dev_tags = []
		for dtag in developer_tags:
			dtag = dtag.replace('date=yyyymmdd', 'date=' + my_date)
			dtag = dtag.replace('videotime=hhmm', 'videotime=' + my_time)
			dtag = dtag.replace('videoslot=hhmm', 'videoslot=' + my_time_slot)
			new_dev_tags.append(dtag)	
		
		# prepare keywords and include dev tags in keywords if required
		keywords = self.tags['keywords']
		if self.dev_tag_to_key:
				for dev_tag in new_dev_tags:
					keywords = '%s, %s' % (keywords, dev_tag)
		
		# prepare a media group object to hold our video's meta-data
		my_media_group = gdata.media.Group(
			title=gdata.media.Title(text=video_title),
			description=gdata.media.Description(description_type='plain', text=self.tags['description']),
			keywords=gdata.media.Keywords(text=keywords),
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
		
		# add dev tags
		video_entry.AddDeveloperTags(new_dev_tags)
		
		for dev_tag in video_entry.GetDeveloperTags():
			self.common.log(1, '- with Dev tag:[T][T]%s' % (dev_tag.text))
		
		# upload
		video_uploaded = ''
		
		try:
			self.common.log(1, '... this may take a few minutes ...')
			if (not self.test_mode):
				video_uploaded = self.yt_service.InsertVideoEntry(video_entry, video_file_location)
			
			#self.common.log(2, 'File uploaded:[T][T]%s' % video_file_location)
			self.common.log(2, 'File uploaded')
			ret = 'uploaded'
		
		except gdata.youtube.service.YouTubeError, e:
			print 'YouTubeError:'
			print e
			self.common.log(3, 'Could not upload file: %s (%s)' % (video_file_location, e[0]['reason']))
			video_uploaded = ''
			ret = 'error'
		
		# to test uncomment these:
		#ret = 'rejected'
		#ret = 'too_many_recent_calls'
		#return ret
		
		# check status of uploaded video
		if (self.check_status == False or self.test_mode):
			return ret
		
		self.common.PrintLine()
		self.common.log(2, 'Checking upload status on YouTube')
		
		try:
			video_id = video_uploaded.id.text
			n = video_id.rfind('/')
			video_id = video_id[n+1:len(video_id)]
		except:
			video_id = ''
		
		upload_status_rem = 'error'
		
		if (video_id <> ''):
			while True:
				try:
					upload_status = self.yt_service.CheckUploadStatus(video_id=video_id)
				except:
					self.common.log(3, 'Could not get status on uploaded file.')
					break
				
				if upload_status is not None:
					my_state = upload_status[0]
					my_message = upload_status[1]
					if my_state == 'rejected':
						upload_status_rem = 'rejected (%s)' % my_message
						# MUST DEAL WITH THIS!!
						ret = my_state
						break;		
					else:
						print my_state, my_message
						#self.common.log(1, '[T][T][T]%s' % (my_state, my_message))
					
				else:
					upload_status_rem = 'uploaded'
					ret = upload_status_rem
					break
				
				time.sleep(self.pause_time_status)
		
		self.common.log(2, 'Uploaded file status:[T]%s' % upload_status_rem)
		
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
		self.yt_service.developer_key = self.credentials['dev_key']
		try:
			self.feed = self.yt_service.GetYouTubeVideoFeed(uri)
			#self.feed = self.yt_service.GetTopRatedVideoFeed()
		except gdata.service.RequestError, e:
			self.common.log(3, 'Error reading feed: %s' % (e[0]['reason']))
			sys.exit(0)
		
		num = 0
		for entry in self.feed.entry:
			try:
				self.PrintEntryDetails(entry)
			except:
				self.common.log(1, '--content ignored--')
			num += 1
			
		self.common.PrintLine()
		self.common.log(1, 'Total videos:[T]%s' % num)	
		self.common.PrintLine()
	
	# ------------------------------------------------------------------------------
	
	def PrintEntryDetails(self, entry):
		self.common.PrintLine()

		self.common.log(1, 'Title:\t\t%s' % entry.media.title.text)
		self.common.log(1, 'Published on:\t%s ' % entry.published.text)
		self.common.log(1, 'ID:\t\t%s' % entry.id.text)
		self.common.log(1, 'Description:\t%s' % entry.media.description.text)
		self.common.log(1, 'Keywords:\t%s' % entry.media.keywords.text)
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
