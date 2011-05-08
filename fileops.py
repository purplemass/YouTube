# ------------------------------------------------------------------------------

import sys, os
from datetime import datetime
import dircache
import shutil

# ------------------------------------------------------------------------------

class FileOps():

	# ------------------------------------------------------------------------------
	
	mainmodule = sys.modules['__main__']
	common = sys.modules['__main__'].common
	
	server_incoming = ''
	server_archive = ''
	local_incoming = ''
	local_archive = ''
	local_log = ''
	path_separator = ''
	
	movie_extension = ''
	
	file_list = {}
	file_list_sorted_keys = []
	
	# ------------------------------------------------------------------------------
	
	def __init__(self, paths, movie_extension):
		self.common.log(1, 'FileOps initialised')
		self.server_incoming = paths['server_incoming']
		self.server_archive = paths['server_archive']
		
		self.local_incoming = paths['local_incoming']
		self.local_archive = paths['local_archive']
		
		self.local_log = paths['local_log']
		
		self.path_separator = paths['separator']
		
		self.movie_extension = movie_extension
		
		for folder in (self.server_incoming, self.server_archive, 
						self.local_incoming, self.local_archive,
						self.local_log
						):
			ret = self.CreateFolder(folder)
			if (ret == False):
				sys.exit('Exiting application')

		
	# ------------------------------------------------------------------------------
	
	def ProcessFolder(self):
		self.ScanFolder()

		file_to_process = self.GetOldestFile()
		num = len(self.file_list)
		
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
	
	def ArchiveFile(self, file_name):
		self.common.PrintLine()
		self.common.log(2, 'Archiving file')		
		
		# server
		server_folder = self.GetDatedFolder(self.server_archive)
		ret = self.CreateFolder(server_folder)
		if (ret):
			ret = self.MoveFile(file_name, self.server_incoming, server_folder)
		
		# local
		local_folder = self.GetDatedFolder(self.local_archive)
		ret = self.CreateFolder(local_folder)
		if (ret):
			ret = self.MoveFile(file_name, self.local_incoming, local_folder)
		
		return ret

	# ------------------------------------------------------------------------------

	def GetDatedFolder(self, path):
		return '%s%s%s' % (path, datetime.now().strftime("%Y%m%d"), self.path_separator)
	
	# ------------------------------------------------------------------------------

	def SortFileList(self, adict):
		self.file_list_sorted_keys = adict.keys()
		self.file_list_sorted_keys.sort()
	
	# ------------------------------------------------------------------------------
	
	def GetOldestFile(self):
		if (len(self.file_list_sorted_keys) == 0):
			return ''
		else:
			return self.file_list[self.file_list_sorted_keys[0]]
	
	# ------------------------------------------------------------------------------
	
	def PrintFolder(self):
		for mdt in self.file_list_sorted_keys:
			self.common.log(1, '%s %s' % (mdt, self.file_list[mdt]))
		"""	
		cc = 1
		for k, v in self.file_list.iteritems():
			self.common.log(1, '%s %s %s' % (cc, k, v))
			cc += 1
		"""
	
	# ------------------------------------------------------------------------------
	
	def ScanFolder(self):
		self.common.log(1, 'Scanning folder[T][T]%s' % self.server_incoming)
		
		self.file_list = {}
		
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
				#ERR!!
				try:
					(mode,ino,dev,nlink,uid,gid,size,atime,mtime,ctime) = os.stat(myfile)
					mtime = datetime.fromtimestamp(mtime)
					self.file_list[str(mtime) + '-' + str(cc)] = filename
				except:
					self.common.log(3, 'Could not process file %s so ignoring it' % myfile)
		
		# get sorted keys
		self.SortFileList(self.file_list)
		
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
		try:
			# create a comma separated line
			msg = msg.replace("\t", ' ')
			date_time = now.strftime("%Y-%m-%d,%H:%M:%S")
			content = "%s,%s\n" % (date_time, msg)
			
			f = open(filename, 'a')
			f.write(content)
			f.closed
		except:
			print 'ERROR writing to log file %s' % filename
		
# ------------------------------------------------------------------------------