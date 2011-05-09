# ------------------------------------------------------------------------------

import sys, os
import smtplib
from email.MIMEText import MIMEText

# ------------------------------------------------------------------------------

class CommonOps():

	# ------------------------------------------------------------------------------
	
	def __init__(self, application, gmail):
		self.mainmodule = sys.modules['__main__']
		self.write_log = application['write_log']
		self.gmail = gmail
		self.priorities = ('debug', 'notice', 'error')
		
		self.PrintLine(True)
		self.log(1, 'CommonOps initialised')
	
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
			error_msg = 'ERROR: '
		else:
			error_msg = ''
		
		msg = msg.replace('[T]', '\t')
		print '%s%s' % (error_msg, msg)
		
		# write to file
		if (self.write_log and priority > 1):
			try:
				self.mainmodule.fileops.WriteLog(priority, msg)
			except AttributeError:
				pass
	
	# ------------------------------------------------------------------------------
	
	def Mail(self, text):
	 	msg = MIMEText(text.encode('utf-8'), _charset='utf-8')
	 	to = ','.join(self.gmail['to']) 
		msg['To'] = to
		msg['From'] = self.gmail['from']
		msg['Subject'] = self.gmail['subject']
		
		try:
			mailserver = smtplib.SMTP('smtp.gmail.com', self.gmail['smtp_port'])
			if self.gmail['debug']: mailserver.set_debuglevel(1)
			mailserver.ehlo()
			mailserver.starttls()
			mailserver.ehlo()
			mailserver.login(self.gmail['user'], self.gmail['password'])
			mailserver.sendmail(self.gmail['from'], to, msg.as_string())
			#mailserver.close()
			mailserver.quit()
			self.log(2, 'Automated email sent')
		except:
			self.log(3, 'Could not send automated email')

# ------------------------------------------------------------------------------
