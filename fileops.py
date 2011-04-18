# ------------------------------------------------------------------------------

import sys, os
from datetime import datetime

# ------------------------------------------------------------------------------

class FileOps():

	# ------------------------------------------------------------------------------
	
	mainmodule = sys.modules['__main__']
	
	server_path = ''
	
	# ------------------------------------------------------------------------------
	
	def __init__(self, server_path):
		print 'FileOps initialsed'
		
		self.server_path = server_path
	
	def scanFolder(self):
		self.mainmodule.print_line()
		print 'Scanning folder %s' % self.server_path
		self.mainmodule.print_line()
				
		for dirname, dirnames, filenames in os.walk(self.server_path):
		
			#for subdirname in dirnames:
			#	print 'Folder %s' % os.path.join(dirname, subdirname)
			
			for filename in filenames:
				myfile = os.path.join(dirname, filename)
				(mode,ino,dev,nlink,uid,gid,size,atime,mtime,ctime) = os.stat(myfile)
				mtime = datetime.fromtimestamp(mtime)
				print mtime.strftime("%Y-%m-%d %H:%M:%S"), filename
		
# ------------------------------------------------------------------------------
