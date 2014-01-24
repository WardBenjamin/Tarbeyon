import time

class ErrorHandler(object):
	def __init__(self):

		self.possibleErrors = {
		"default"  : "Default Error\n",
		"itemID"   : "Not a valid ID\n",
		"newError" : "An unrecognized error has been raised called '"
		}

		self.f = open('error_log.txt', 'a')

	def raise_error(self, error):
		try:
			errorRaised = self.possibleErrors[error]
			currentTime = time.asctime()
			currentTime = currentTime +"\n"
			message = currentTime + errorRaised
			self.f.write(message)
			print(message)
		except:
			errorRaised = self.possibleErrors["newError"]
			currentTime = time.asctime()
			currentTime = currentTime +"\n"
			message = currentTime + errorRaised + str(error) + "'" + "\n"
			self.f.write(message)
			print(message)

eh = ErrorHandler()
eh.raise_error("test")