import smtplib

def send_email_alert():
	SERVER = "localhost"

	FROM = "dmilad@gmail.com"
	TO = ["dmilad@gmail.com"] # must be a list

	SUBJECT = "tweet collector interrupted on node 4"

	TEXT = "pub ip: 50.23.121.179"

	try:
		TEXT += '\n'
		with open('../nohup.out', 'r') as nohup:
			for line in nohup:
				TEXT += '\n' + line
	except:
		pass
	# Prepare actual message

	message = """\
	From: %s
	To: %s
	Subject: %s

	%s
	""" % (FROM, ", ".join(TO), SUBJECT, TEXT)

	# Send the mail
	server = smtplib.SMTP(SERVER)
	server.sendmail(FROM, TO, message)
	server.quit()

if __name__ == '__main__':
	pass