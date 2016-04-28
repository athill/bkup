# Vigenere Cypther 
# https://gist.github.com/ilogik/6f9431e4588015ecb194
class Cypher:
	def __init__(self, key=None):
		self.key = key
		if self.key == None:
			import uuid
			self.key = str(uuid.uuid4())


	def encode(self, string):
	    encoded_chars = []
	    for i in xrange(len(string)):
	        key_c = self.key[i % len(self.key)]
	        encoded_c = chr(ord(string[i]) + ord(key_c) % 256)
	        encoded_chars.append(encoded_c)
	    encoded_string = "".join(encoded_chars)
	    return base64.urlsafe_b64encode(encoded_string)


	def decode(self, string):
	    decoded_chars = []
	    string = base64.urlsafe_b64decode(string)
	    for i in xrange(len(string)):
	        key_c = self.key[i % len(self.key)]
	        encoded_c = chr(abs(ord(string[i]) - ord(key_c) % 256))
	        decoded_chars.append(encoded_c)
	    decoded_string = "".join(decoded_chars)
	    return decoded_string