import xmlrpc.client
import ssl
import threading
import time


class N4dManager:
	
	def __init__(self,server=None):
		
		self.debug=True
		
		self.client=None
		self.user_validated=False
		self.user_groups=[]
		self.validation=None
		self.status=False
		
		if server!=None:
			self.set_server(server)
		
	#def init
	
	
	def dprint(self,msg):
		
		if self.debug:
			print(str(msg))
			
	#def dprint
		
	
	def set_server(self,server):
		
		context=ssl._create_unverified_context()	
		self.client=xmlrpc.client.ServerProxy("https://%s:9779"%server,allow_none=True,context=context)
		
	#def set_server
	
	
	def validate_user(self,user,password):
		
		ret=self.client.validate_user(user,password)
		self.user_validated,self.user_groups=ret
			
		
		if self.user_validated:
			self.validation=(user,password)
			self.status=self.is_lock_enabled()
		
		return self.user_validated
		
	#def validate_user
	
	
	def is_lock_enabled(self):
		
		return self.client.is_enabled(self.validation,"CDLockerManager")
		
	#def cron_enabled
	
	
	def set_lock_status(self,status):
		
		ret=self.client.set_lock_status(self.validation,"CDLockerManager",status)
		print(ret)
		
	#def set_lock_status
	
	
	
#class N4dManager
