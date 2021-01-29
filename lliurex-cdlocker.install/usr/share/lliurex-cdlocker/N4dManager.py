import n4d.client
import time
import sys


class N4dManager:

	def __init__(self,ticket):

		ticket=ticket[1]+' '+ticket[2]+' '+ticket[3]+' '+ticket[4]
		self.set_server(ticket)
		
	#def init

	def set_server(self,ticket):

		tk=n4d.client.Ticket(ticket)

		self.n4dclient=n4d.client.Client(ticket=tk)
	#def set_server
	
	def is_lock_enabled(self):
		
		return self.n4dclient.CDLockerManager.is_enabled()
		
	#def is_lock_enabled
	
	def set_lock_status(self,status):
		
		self.n4dclient.CDLockerManager.set_lock_status(status)
		
	#def set_lock_status

#class M4dManager
	
	
	
#class N4dManager
