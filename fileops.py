# ------------------------------------------------------------------------------

import sys, os
from datetime import datetime
import dircache
import shutil

# ------------------------------------------------------------------------------

class FileOps():

	# ------------------------------------------------------------------------------
	
	common = sys.modules['__main__'].common
	
	path_server = ''
	path_incoming = ''
	path_archive = ''
	path_separator = ''
	
	movie_extension = ''
	
	file_list = {}
	file_list_sorted_keys = []
	
	# ------------------------------------------------------------------------------
	
	def __init__(self, paths, movie_extension):
		self.common.log(1, 'FileOps initialised')
		
		self.path_server = paths['server']
		self.path_incoming = paths['incoming']
		self.path_archive = paths['archive']
		self.path_separator = paths['separator']
		
		self.movie_extension = movie_extension
		
		for folder in (self.path_incoming, self.path_archive):
			ret = self.CreateFolder(folder)
			if (ret == False):
				sys.exit('Exiting application')

		
	# ------------------------------------------------------------------------------
	
	def ProcessFolder(self):
		self.ScanFolder()

		file_to_process = self.GetOldestFile()
		num = len(self.file_list)
		
		# log		
		self.common.PrintLine()
		self.common.log(2, 'Files to process: %s' % num)
			
		if (num > 0):
			#self.PrintFolder()
			ret = self.CopyFile(self.path_server + file_to_process, self.path_incoming)
			if (ret):
				return file_to_process
		else:
			ret = False
				
		return ret
	
	# ------------------------------------------------------------------------------
	
	def ArchiveFile(self, file_name):
		self.common.log(2, 'Archiving file: %s' % file_name)
					
		now = datetime.now()
		folder_name = '%s%s%s' % (self.path_archive, now.strftime("%Y%m%d"), self.path_separator)
		
		ret = self.CreateFolder(folder_name)
		
		if (ret):
			ret = self.CopyFile(self.path_incoming + file_name, folder_name + file_name)
			if (ret):
				ret = self.DeleteFile(self.path_incoming + file_name)
		
		return ret
	
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
		self.common.log(1, 'Scanning folder %s' % self.path_server)
		
		self.file_list = {}
		
		try:
			myfilelist = dircache.listdir(self.path_server)
		except OSError:
			self.common.log(3, 'Cannot connect to folder')
			myfilelist = []
		
		# go through items in folder and get files
		cc = 0
		for filename in myfilelist:
			cc += 1
			myfile = os.path.join(self.path_server, filename)
			
			# check extension
			if (myfile.endswith('.' + self.movie_extension)):
				#ERR!!
				(mode,ino,dev,nlink,uid,gid,size,atime,mtime,ctime) = os.stat(myfile)
				mtime = datetime.fromtimestamp(mtime)
				self.file_list[str(mtime) + '-' + str(cc)] = filename
		
		# get sorted keys
		self.SortFileList(self.file_list)
		
	# ------------------------------------------------------------------------------
	
	def CreateFolder(self, folder):
		ret = True
		try:
			os.mkdir(folder)
			self.common.log(2, 'Folder created: %s' % folder)			
		except OSError as (errno, strerror):
			if (errno == 17):
				#self.common.log(1, 'Folder exists: %s' % folder)
				pass
			else:
				self.common.log(3, strerror)
				ret = False
		
		return ret
	
	# ------------------------------------------------------------------------------
	
	def CopyFile(self, source, target):
		self.common.log(1, 'Copying file: %s to %s' % (source, target))
			
		try:
			shutil.copy2(source, target)
			#self.common.log(1, 'File copied: %s' % source)
			ret = True
		except IOError as (errno, strerror):
			self.common.log(3, 'Could not copy file: %s (%s)' % (source, strerror))
			ret = False	
		
		return ret
	
	# ------------------------------------------------------------------------------
	
	def DeleteFile(self, file_name):
		self.common.log(1, 'Deleting file: %s' % file_name)
			
		try:
			os.remove(file_name)
			#self.common.log(1, 'File deleted: %s' % file_name)
			ret = True
		except IOError as (errno, strerror):
			self.common.log(3, 'Could not delete file: %s (%s)' % (file_name, strerror))
			ret = False	
		
		return ret
	
# ------------------------------------------------------------------------------
