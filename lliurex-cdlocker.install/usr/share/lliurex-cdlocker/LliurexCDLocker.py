#!/usr/bin/env python
# -*- coding: utf-8 -*

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk,GObject,GLib,Gdk,Gio

import signal
import gettext
import sys
import threading
import copy
import os

import N4dManager

signal.signal(signal.SIGINT, signal.SIG_DFL)
gettext.textdomain('lliurex-cdlocker')
_ = gettext.gettext

CSS_FILE="/usr/share/lliurex-cdlocker/rsrc/style.css"

class LliurexCDLocker:
	
	def __init__(self,args_dic):
		
		self.n4d_man=N4dManager.N4dManager()
		self.n4d_man.set_server(args_dic["server"])
		#self.n4d_man.set_server(args_dic["172.20.9.246"])
		
		if args_dic["gui"]:
			
			self.start_gui()
			GObject.threads_init()
			Gtk.main()
		
	#def __init__(self):
	
	
	def start_gui(self):

		builder=Gtk.Builder()
		builder.set_translation_domain('lliurex-cdlocker')
		if os.path.exists("/srv/svn/xenial/lliurex-cdlocker/trunk/fuentes/lliurex-cdlocker.install/usr/share/lliurex-cdlocker/rsrc/lliurex-cdlocker.ui"):
			builder.add_from_file("/srv/svn/xenial/lliurex-cdlocker/trunk/fuentes/lliurex-cdlocker.install/usr/share/lliurex-cdlocker/rsrc/lliurex-cdlocker.ui")
		else:
			builder.add_from_file("/usr/share/lliurex-cdlocker/rsrc/lliurex-cdlocker.ui")
			
		self.main_window=builder.get_object("main_window")
		
		self.main_box=builder.get_object("main_box")
		self.login_box=builder.get_object("login_box")
		self.cdlocker_box=builder.get_object("cdlocker_box")

		self.stack=Gtk.Stack()
		self.stack.set_transition_type(Gtk.StackTransitionType.CROSSFADE)
		self.stack.set_transition_duration(200)
		self.stack.add_titled(self.login_box,"login","Login")
		self.stack.add_titled(self.cdlocker_box,"cdlocker","CD Locker")
		self.stack.show_all()
		
		self.main_box.pack_start(self.stack,True,True,0)
		
		self.close_button=builder.get_object("close_button")
		self.login_button=builder.get_object("login_button")
		self.shutdown_button=builder.get_object("shutdown_button")
		
		self.user_entry=builder.get_object("user_entry")
		self.password_entry=builder.get_object("password_entry")
		self.server_ip_entry=builder.get_object("server_ip_entry")
		self.login_msg_label=builder.get_object("login_msg_label")
		
		self.lock_label=builder.get_object("lock_label")
		self.lock_switch=builder.get_object("lock_switch")
		self.lock_separator=builder.get_object("lock_separator")
		self.help_label=builder.get_object("help_label")
		
				
		self.login_button.grab_focus()
		
		self.connect_signals()
		self.set_css_info()
		self.main_window.show()
		
	#def start_gui
	
	
	def connect_signals(self):
		
		self.main_window.connect("destroy",Gtk.main_quit)
		self.close_button.connect("clicked",Gtk.main_quit)
		self.login_button.connect("clicked",self.login_clicked)
		self.user_entry.connect("activate",self.entries_press_event)
		self.password_entry.connect("activate",self.entries_press_event)
		self.server_ip_entry.connect("activate",self.entries_press_event)
		
	#def connect_signals
	
	# CSS ###########################################################

	def set_css_info(self):
		
		self.style_provider=Gtk.CssProvider()
		f=Gio.File.new_for_path(CSS_FILE)
		self.style_provider.load_from_file(f)
		Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(),self.style_provider,Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
		self.main_window.set_name("WHITE-BACKGROUND")
		self.user_entry.set_name("CUSTOM-ENTRY")
		self.password_entry.set_name("CUSTOM-ENTRY")
		self.server_ip_entry.set_name("CUSTOM-ENTRY")
		self.lock_label.set_name("DEFAULT-LABEL")
		self.lock_separator.set_name("SEPARATOR")
		self.help_label.set_name("DEFAULT-LABEL-HELP")

	#def set_css_info		
	
	# SIGNALS ########################################################
	
	def entries_press_event(self,widget):
		
		self.login_clicked(None)
		
	#def entries_press_event
	
	
	def login_clicked(self,widget):
		
		user=self.user_entry.get_text()
		password=self.password_entry.get_text()
		server=self.server_ip_entry.get_text()
	
		'''	
		# HACK
		
		user="lliurex"
		password="lliurex"
		server="172.20.9.246"
		'''

		if server!="":
			self.n4d_man.set_server(server)
		
		
		self.login_msg_label.set_text(_("Validating user..."))
		
		self.login_button.set_sensitive(False)
		self.validate_user(user,password)
		
		
	#def login_clicked
	
	def lock_switch_changed(self,widget,data):
		
		self.n4d_man.set_lock_status(self.lock_switch.get_state())
		
	#def lock_switch_changed
	
	# ##################### ##########################################
	
	def validate_user(self,user,password):
		
		
		t=threading.Thread(target=self.n4d_man.validate_user,args=(user,password,))
		t.daemon=True
		t.start()
		GLib.timeout_add(500,self.validate_user_listener,t)
		
	#def validate_user
	
	
	def validate_user_listener(self,thread):
			
		if thread.is_alive():
			return True
				
		self.login_button.set_sensitive(True)
		if not self.n4d_man.user_validated:
			self.login_msg_label.set_markup("<span foreground='red'>"+_("Invalid user")+"</span>")
		else:
			group_found=False
			for g in ["adm","admins","teachers"]:
				if g in self.n4d_man.user_groups:
					group_found=True
					break
					
			if group_found:
				self.login_msg_label.set_text("")
				self.lock_switch.set_state(self.n4d_man.status)
				self.lock_switch.connect("notify::active",self.lock_switch_changed)
				
				self.stack.set_visible_child_name("cdlocker")
				
			else:
				self.login_msg_label.set_markup("<span foreground='red'>"+_("Invalid user")+"</span>")
				
		return False
			
	#def validate_user_listener
	
		
#class LliurexShutdowner


if __name__=="__main__":
	
	pass
	
