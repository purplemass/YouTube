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
	
	# ------------------------------------------------------------------------------
	
	def __init__(self, server_path):
		print 'FileOps initialised'		
		self.common.print_line()
		
		self.server_path = server_path
	
	def copyFile(self, file_name):
		commmon.log(2, 'Copying file: %s' % file_name)
	
	def sortedDictValues(self, adict):
		keys = adict.items()
		keys.sort()
		mylist = {}
		for key, value in keys:
			mylist[key] = value
		print mylist
		return [mylist]
	
	def scanFolder(self):
		print 'Scanning folder %s' % self.server_path
		
		self.common.print_line()
		
		self.file_list = {}
		
		# go through items in folder and get files
		cc = 0
		for filename in dircache.listdir(self.server_path):
			cc += 1
			myfile = os.path.join(self.server_path, filename)
			(mode,ino,dev,nlink,uid,gid,size,atime,mtime,ctime) = os.stat(myfile)
			mtime = datetime.fromtimestamp(mtime)
			print cc, mtime.strftime("%Y-%m-%d %H:%M:%S"), filename
			
			self.file_list[str(mtime) + '-' + str(cc)] = filename
				
		self.file_list = self.sortedDictValues(self.file_list)
		
		self.common.print_line()
		self.common.log(1, 'Files to process: %s' % len(self.file_list))
		self.common.print_line()
		
		print self.file_list
		
		cc = 1
		for k, v in self.file_list.iteritems():
			print cc, k, v
			cc =+ 1

# ------------------------------------------------------------------------------
