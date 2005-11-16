#!/usr/bin/env python

import pygtk
pygtk.require('2.0')

import gobject
import pango
import gtk
import math
import time
from gtk import gdk
import cairo
import rack2cairo

import xml.dom.minidom
import rackbuilder

ast = xml.dom.minidom.parse("example.feng")
rack = rackbuilder.RackBuilder().build(ast)

if gtk.pygtk_version < (2,7,99):
	print "PyGtk 2.7.99 or later required"
	raise SystemExit

class PyGtkWidget(gtk.Widget):
	__gsignals__ = {'realize': 'override',
					'expose-event' : 'override',
					'size-allocate': 'override',
					'size-request': 'override',}

	def __init__(self):
		gtk.Widget.__init__(self)
		self.draw_gc = None

	def do_realize(self):
		self.set_flags(self.flags() | gtk.REALIZED)
		self.window = gdk.Window(self.get_parent_window(),
								 width=self.allocation.width,
								 height=self.allocation.height,
								 window_type=gdk.WINDOW_CHILD,
								 wclass=gdk.INPUT_OUTPUT,
								 event_mask=self.get_events() | gdk.EXPOSURE_MASK)

		self.window.set_user_data(self)
		self.style.attach(self.window)
		self.style.set_background(self.window, gtk.STATE_NORMAL)
		self.window.move_resize(*self.allocation)

	def do_size_request(self, requisition):
		requisition.width = rack2cairo.WIDTH
		requisition.height = rack2cairo.HEIGHT

	def do_size_allocate(self, allocation):
		self.allocation = allocation
		if self.flags() & gtk.REALIZED:
			self.window.move_resize(*allocation)

	def _expose_cairo(self, event, cr):
		global rack
		rack2cairo.RackView("gtk").render(rack, cr)

	def do_expose_event(self, event):
		self.chain(event)
		cr = self.window.cairo_create()
		return self._expose_cairo(event, cr)

win = gtk.Window()
win.set_title('fengshui')
win.connect('delete-event', gtk.main_quit)

event_box = gtk.EventBox()
event_box.connect("button_press_event", lambda w,e: win.set_decorated(not win.get_decorated()))

win.add(event_box)

w = PyGtkWidget()
event_box.add(w)

#win.move(gtk.gdk.screen_width() - 120, 40)
win.show_all()

gtk.main()
