# ------------------------------------------------------------------------------

import sys, os
from datetime import datetime
import dircache

# ------------------------------------------------------------------------------

class FileOps():

	# ------------------------------------------------------------------------------
	
	common = sys.modules['__main__'].common
	
	server_path = ''
	file_list = {}
	file_list_sorted_keys = []
	
	# ------------------------------------------------------------------------------
	
	def __init__(self, server_path):
		self.common.log(1, 'FileOps initialised')
		
		self.server_path = server_path
	
	# ------------------------------------------------------------------------------
	
	def ProcessFolder(self):
		self.ScanFolder()

		file_to_process = self.GetOldestFile()
				
		# log		
		self.common.PrintLine()
		self.common.log(1, 'Files to process: %s' % len(self.file_list))
		self.common.log(2, 'Oldest file: %s' % file_to_process)
		self.common.PrintLine()
		
	# ------------------------------------------------------------------------------
	
	def CopyFile(self, file_name):
		commmon.log(2, 'Copying file: %s' % file_name)
	
	# ------------------------------------------------------------------------------

	def SortFileList(self, adict):
		self.file_list_sorted_keys = adict.keys()
		self.file_list_sorted_keys.sort()
	
	# ------------------------------------------------------------------------------
	
	def GetOldestFile(self):
		return self.file_list[self.file_list_sorted_keys[0]]
	
	# ------------------------------------------------------------------------------
	
	def ScanFolder(self):
		self.common.log(1, 'Scanning folder %s' % self.server_path)
		
		self.file_list = {}
		
		# go through items in folder and get files
		cc = 0
		for filename in dircache.listdir(self.server_path):
			cc += 1
			myfile = os.path.join(self.server_path, filename)
			
			# check extension movie_extension
			if (True):
				(mode,ino,dev,nlink,uid,gid,size,atime,mtime,ctime) = os.stat(myfile)
				mtime = datetime.fromtimestamp(mtime)
				self.file_list[str(mtime) + '-' + str(cc)] = filename
		
		# get sorted keys
		self.SortFileList(self.file_list)
		
		"""
		cc = 1
		for k, v in self.file_list.iteritems():
			print cc, k, v
			cc += 1
		"""
		
		# print files
		self.common.PrintLine()
		for mdt in self.file_list_sorted_keys:
			self.common.log(1, '%s %s' % (mdt, self.file_list[mdt]))

# ------------------------------------------------------------------------------
