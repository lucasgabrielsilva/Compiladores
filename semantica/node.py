class Node():
	def __init__(self, scope, type, value, body):
		self.scope = scope 					
		self.type = type 						
		self.value = value 						
		self.body = body				
		self.used = False 		