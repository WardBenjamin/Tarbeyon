import time, os

class Log(object):
	def __init__(self):

		self.logEntries = {
		"default"  : "Default Entry\n",
		"gameStart"   : "The game has started\n",
		"newEntry" : "An unrecognized entry has been added: '"
		}

		path_to_file = "logs" + os.sep + "game.log"
		if os.path.isfile(path_to_file): 
			try:
				self.f = open(path_to_file, 'a')
			except:
				z


	def add_entry(self, entry):
		try:
			entrytoadd = self.logEntries[entry]
			currentTime = time.asctime()
			currentTime = currentTime +"\n"
			message = currentTime + entrytoadd
			self.f.write(message)
			print(message)
		except:
			entrytoadd = self.logEntries["newEntry"]
			currentTime = time.asctime()
			currentTime = currentTime +"\n"
			message = currentTime + entrytoadd + str(entry) + "'" + "\n"
			self.f.write(message)
			print(message)

log = Log()
log.add_entry("something")