# ------------------------------------------------------------------------------

import sys, os
import smtplib
from email.MIMEText import MIMEText

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
	
	def Mail(self, text):
		from_email = 'youtubetest@imagination.com'
		to_email = 'purplemass@gmail.com'
		gmail_user = 'youtubetest@imagination.com '
		gmail_password = '1mag1ant1on'
		subject = 'Test email from the Python app'
		
	 	msg = MIMEText(text.encode('utf-8'), _charset='utf-8')	
		msg['From'] = gmail_user
		msg['To'] = to_email
		msg['Subject'] = subject
		
		mailserver = smtplib.SMTP('smtp.gmail.com')
		if self.mainmodule.settings['test_mode']: mailserver.set_debuglevel(1)
		mailserver.ehlo()
		mailserver.starttls()
		mailserver.ehlo()
		mailserver.login(gmail_user, gmail_password)
		mailserver.sendmail(from_email, to_email, msg.as_string())
		mailserver.close()

# ------------------------------------------------------------------------------
