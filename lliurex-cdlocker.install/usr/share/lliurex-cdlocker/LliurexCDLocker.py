from PySide2.QtCore import QObject,Signal,Slot,QThread,Property
import os 
import N4dManager
import sys

class Bridge(QObject):

	def __init__(self,ticket=None):

		QObject.__init__(self)

		self.n4d_man=N4dManager.N4dManager(ticket)
		self.getState()
	
	#def _init	

	def getState(self):

		self._loadState=self.n4d_man.is_lock_enabled()

	#def getState

	@Slot(bool)
	def setState(self,state):

		self.n4d_man.set_lock_status(state)

	#def setState

	def _getLoadState(self):

		return self._loadState

	loadState=Property(bool,_getLoadState,constant=True)


#class Bridge


if __name__=="__main__":

	pass