# attachments.py
#
# by Patrick Nevels
# created 1/17 - 1/19
#
# This class provides a set of methods for downloading 
# email attachments from a given Gmail account


import os, getpass, email, imaplib

class Attachments(object):
	
	# create SSL connection to email server
	def __init__(self, directory = '.'):
		
		self.imap = imaplib.IMAP4_SSL("imap.gmail.com", 993)
		self.dir = directory
	
	# log on
	# TODO figure out the whole error catching thing
	def login(self):
		
		while True:
			try:
				# get the username and password
				usr = raw_input("Enter your email address: ")
				pwd = getpass.getpass("Enter your password: ")
				
				self.imap.login(usr,pwd)
				break
				
			except:
				print "Try again please."
				print "=============================="

	def getAttachments(self):

		self.imap.select("[Gmail]/All Mail")
		resp, items = self.imap.search(None, "ALL")
		items = items[0].split()
		
		# fetch mail and walk though each, determining which has 
		for id in items:
			resp, data = self.imap.fetch(id, "(RFC822)")
			body = data[0] [1]
			mail = email.message_from_string(body)
			
			if mail.get_content_maintype() != 'multipart':
				continue
				
			for part in mail.walk():
				
				if part.get_content_maintype() == 'maintype':
					continue
					
				if part.get('Content-Disposition') is None:
					continue
				
				
				filename = part.get_filename()
				
				if not filename: 
					filename = 'part-%03d%s' % (counter, 'trash')

				
				if 'py' not in filename:
					continue
				else: 
					print "[" + mail["From"] + "] :" +mail["Subject"]
				
				to_path = os.path.join(self.dir, filename)
				
				if not os.path.isfile(to_path):
					fp = open(to_path, 'wb')
					fp.write(part.get_payload(decode=True))
					fp.close()
	