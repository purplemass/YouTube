# ------------------------------------------------------------------------------

import sys, os

# ------------------------------------------------------------------------------

class CommonOps():

	# ------------------------------------------------------------------------------
	
	mainmodule = sys.modules['__main__']
	
	running = True
	write_log = False
	
	# ------------------------------------------------------------------------------
	
	def __init__(self):
		self.PrintLine(True)
		self.log(1, 'CommonOps initialised')
		self.write_log = self.mainmodule.settings['write_log']
	
	# ------------------------------------------------------------------------------
	
	def PrintLine(self, double=False):
		if (double):
			print '=========================================================================='
		else:
			print '--------------------------------------------------------------------------'
	
	# ------------------------------------------------------------------------------
	
	def log(self, priority, msg):
		# priorities:
		# 1 = debug
		# 2 = notice
		# 3 = error
		#
		if priority == 3:
			error = 'ERROR '
		else:
			error = ''
		
		msg = msg.replace('[T]', '\t')
		print '%s%s' % (error, msg)
		
		if (self.write_log and priority > 1):
			try:
				self.mainmodule.fileops.WriteLog(priority, msg)
			except AttributeError:
				pass

# ------------------------------------------------------------------------------
