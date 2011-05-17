# ------------------------------------------------------------------------------

import sys, os
from datetime import datetime
from time import mktime
import dircache
import shutil

# ------------------------------------------------------------------------------

class FileOps():

	# ------------------------------------------------------------------------------
	
	def __init__(self, paths, application):
		self.mainmodule = sys.modules['__main__']
		self.common = sys.modules['__main__'].common
		
		self.server_incoming = paths['server_incoming']
		self.server_archive = paths['server_archive']
		self.server_rejected = paths['server_rejected']
		self.local_incoming = paths['local_incoming']
		self.local_archive = paths['local_archive']
		self.local_rejected = paths['local_rejected']
		
		self.local_log = paths['local_log']
		
		self.path_separator = application['separator']
		self.movie_extension = application['movie_extension']
		
		self.difference_in_mt = application['difference_in_mt']
		
		self.file_list_by_name = []
		self.file_list_by_mt = {}
		self.file_list_by_mt_sorted_keys = []
		
		# create all necessary folders
		for folder in (paths):
			if ( folder.find('server') > -1 or folder.find('local') > -1 ):
				ret = self.CreateFolder(paths[folder])
				if (ret == False):
					sys.exit('Exiting application')
		
		self.common.log(1, 'FileOps initialised')
	
	# ------------------------------------------------------------------------------
	
	def ProcessFolder(self):
		self.ScanFolder()
		
		file_to_process = self.GetOldestFileByName()
		num = len(self.file_list_by_name) # !! watch this if you go back to file_list_by_mt
		
		self.common.log(2, 'Files to process:[T]%s' % num)
			
		if (num > 0):
			self.common.PrintLine()
			self.common.log(2, 'Processing file:[T]%s' % file_to_process)
			ret = self.CopyFile(file_to_process, self.server_incoming, self.local_incoming)
			if (ret):
				return file_to_process
		else:
			ret = False
				
		return ret
	
	# ------------------------------------------------------------------------------
	
	def ArchiveFile(self, file_name, reject=False):
		self.common.PrintLine()
		if reject:
			self.common.log(2, 'Rejecting file')
			server_folder = self.server_rejected
			local_folder = self.local_rejected
		else:
			self.common.log(2, 'Archiving file')
			server_folder = self.server_archive
			local_folder = self.local_archive
		
		# server
		server_folder = self.GetDatedFolder(server_folder)
		ret = self.CreateFolder(server_folder)
		if (ret):
			ret = self.MoveFile(file_name, self.server_incoming, server_folder)
		
		# local
		local_folder = self.GetDatedFolder(local_folder)
		ret = self.CreateFolder(local_folder)
		if (ret):
			ret = self.MoveFile(file_name, self.local_incoming, local_folder)
		
		return ret

	# ------------------------------------------------------------------------------

	def GetDatedFolder(self, path):
		return '%s%s%s' % (path, datetime.now().strftime("%Y%m%d"), self.path_separator)
	
	# ------------------------------------------------------------------------------

	def SortFileList(self, adict):
		self.file_list_by_mt_sorted_keys = adict.keys()
		self.file_list_by_mt_sorted_keys.sort()
	
	# ------------------------------------------------------------------------------
	
	def GetOldestFileByName(self):
		if (len(self.file_list_by_name) == 0):
			return ''
		else:
			return self.file_list_by_name[0]
	
	# ------------------------------------------------------------------------------
	
	def GetOldestFileByMT(self):
		if (len(self.file_list_by_mt_sorted_keys) == 0):
			return ''
		else:
			return self.file_list_by_mt[self.file_list_by_mt_sorted_keys[0]]
	
	# ------------------------------------------------------------------------------
	
	def PrintFolder(self):
		for mdt in self.file_list_by_mt_sorted_keys:
			self.common.log(1, '%s %s' % (mdt, self.file_list_by_mt[mdt]))
		"""	
		cc = 1
		for k, v in self.file_list_by_mt.iteritems():
			self.common.log(1, '%s %s %s' % (cc, k, v))
			cc += 1
		"""
	
	# ------------------------------------------------------------------------------
	
	def ScanFolder(self):
		self.common.log(1, 'Scanning folder[T][T]%s' % self.server_incoming)
		
		self.file_list_by_name = []
		self.file_list_by_mt = {}
		
		try:
			# do not use this on Windows:
			# dircache.listdir(self.server_incoming)
			# as it's cached (obviously!)
			#
			myfilelist = os.listdir(self.server_incoming)
		
		except OSError:
			self.common.log(3, 'Cannot connect to folder')
			myfilelist = []
		
		# go through items in folder and get files
		cc = 0
		for filename in myfilelist:
			cc += 1
			myfile = os.path.join(self.server_incoming, filename)
			
			# check extension
			if (myfile.endswith('.' + self.movie_extension)):
				try:
					(mode,ino,dev,nlink,uid,gid,size,atime,mtime,ctime) = os.stat(myfile)
					# get modified time (MT) of each file
					mtime = datetime.fromtimestamp(mtime)

					# compare MT with current time
					# only allow files that are older than specified time
					#
					diff_u = self.MakeUnixTime(datetime.now()) - self.MakeUnixTime(mtime)
					
					# add to our lists
					if (diff_u > self.difference_in_mt):
						self.file_list_by_name.append(filename)
						self.file_list_by_mt[str(mtime) + '-' + str(cc)] = filename
				except:
					self.common.log(3, 'Could not process file %s so ignoring it' % myfile)
				
		# sort lists
		self.file_list_by_name.sort()
		self.SortFileList(self.file_list_by_mt)
	
	# ------------------------------------------------------------------------------
	
	def MakeUnixTime(self, my_time):
		return mktime(my_time.timetuple())+1e-6*my_time.microsecond
	
	# ------------------------------------------------------------------------------
	
	def CopyFile(self, filename, source, target):
		#self.common.log(1, 'Copying file:[T][T]%s to %s' % (source, target))
		self.common.log(1, 'Copying file:')
		self.common.log(1, '- from:[T][T][T]%s' % source)
		self.common.log(1, '- to[T][T][T]%s' % target)
		
		try:
			shutil.copy2(source + filename, target + filename)
			#self.common.log(1, 'File copied: %s' % source)
			ret = True
		except IOError as (errno, strerror):
			self.common.log(3, 'Could not copy file: %s (%s)' % (filename, strerror))
			ret = False	
		
		return ret
	
	# ------------------------------------------------------------------------------
	
	def MoveFile(self, filename, source, target):
		self.common.log(1, 'Moving file:')
		self.common.log(1, '- from:[T][T][T]%s' % source)
		self.common.log(1, '- to[T][T][T]%s' % target)
			
		try:
			shutil.move(source + filename, target + filename)
			#self.common.log(1, 'File moved: %s' % source)
			ret = True
		except IOError as (errno, strerror):
			self.common.log(3, 'Could not move file: %s (%s)' % (filename, strerror))
			ret = False	
		
		return ret
	
	# ------------------------------------------------------------------------------
	
	def DeleteFile(self, file_name):
		self.common.log(1, 'Deleting file:[T][T]%s' % file_name)
			
		try:
			os.remove(file_name)
			#self.common.log(1, 'File deleted: %s' % file_name)
			ret = True
		except IOError as (errno, strerror):
			self.common.log(3, 'Could not delete file: %s (%s)' % (file_name, strerror))
			ret = False	
		
		return ret

	# ------------------------------------------------------------------------------
	
	def CreateFolder(self, folder):
		ret = True
		
		try:
			os.mkdir(folder)
			self.common.log(2, 'Folder created:[T][T]%s' % folder)
		except OSError as (errno, strerror):
			if (errno == 17 or errno == 183): #17 for OSX, 183 for Windows
				#self.common.log(1, 'Folder exists: %s' % folder)
				pass
			else:
				self.common.log(3, folder, strerror)				
				ret = False
		
		return ret
	
	# ------------------------------------------------------------------------------
	
	def WriteLog(self, priority, msg):
		# do not log anything here!!
		# this will cause a paradox in our universe
		#
		now = datetime.now()
		filename = '%s%s.csv' % (self.local_log, now.strftime("%Y%m%d"))
		priority = self.common.priorities[priority-1]
		try:
			# create a comma separated line
			msg = msg.replace("\t", ' ')
			date_time = now.strftime("%Y-%m-%d,%H:%M:%S")
			content = "%s,%s,%s\n" % (date_time, priority, msg)
			
			f = open(filename, 'a')
			f.write(content)
			f.closed
		except:
			print 'ERROR writing to log file %s' % filename
		
# ------------------------------------------------------------------------------