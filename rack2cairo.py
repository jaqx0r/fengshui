#!/usr/bin/python

import rack
import cairo

from math import pi

import mx.DateTime

class RenderingDumbThingException(Exception):
	pass

unitsize = 43.5
rackwidth = 445
rackheight = unitsize * 47
bracketwidth = 15
barwidth = 40
bracketrad = 2

WIDTH = int(rackwidth + 200)
HEIGHT = int(rackheight + 200)

class RackView:
	def __init__(self, name):
		self.options = []
		self.name = name

	def render(self, thing, cr):
		"""
		@param thing the rack or racks to be drawn
		"""

		self.ctx = cr

		self.ctx.set_line_width(1)
		#self.ctx.identity_matrix()
		#self.ctx.scale(205, 660)

		# make it white
		self.ctx.set_source_rgba(1, 1, 1, 1)
		self.ctx.rectangle(0, 0, WIDTH, HEIGHT)
		self.ctx.fill_preserve()
		self.ctx.stroke()

		self.ctx.scale(1, -1)
		self.ctx.translate(0, -HEIGHT)

		# set the font we're using for the whole picture
		self.ctx.select_font_face("Sans", cairo.FONT_SLANT_NORMAL,
								  cairo.FONT_WEIGHT_BOLD)
		self.ctx.set_font_size(20)

		self.ctx.translate(40, 100)
		
		if isinstance(thing, rack.RackArray):
			self.visitRackArray(thing)
		elif isinstance(thing, rack.Rack):
			self.visitRack(thing)
		else:
			raise RenderingDumbThingException

		return None
	
	def visitRackArray(self, racks):
		x = 0
		for rack in racks._elements:
			self.ps.save()
			self.ps.translate(rackheight /2.0 + 300, 0)
			self.ps.scale(0.5, 0.5)
			self.ps.rotate(pi)
			self.ps.translate(x, 0)
			self.visitRack(rack)
			self.ps.restore()

			x += 2 * barwidth + 2 * bracketwidth + rackwidth + 5

	def visitRack(self, rack):
		"""
		@param rack the rack being visited
		"""

		# push the current stack
		self.ctx.save()

		# move in by bar_area.width + mounting_bracket.width
		self.ctx.translate(barwidth + bracketwidth, 0)

		# full outline of rack and brackets
		self.ctx.save()
		self.ctx.set_source_rgba(0.25, 0.25, 0.25, 1)
		#self.ctx.newpath()
		self.ctx.move_to(-bracketwidth, 0)
		self.ctx.line_to(-bracketwidth, rackheight)
		self.ctx.line_to(rackwidth + bracketwidth, rackheight)
		self.ctx.line_to(rackwidth + bracketwidth, 0)
		#self.ctx.closepath()
		self.ctx.stroke()
		# rack outline
		#self.ctx.newpath()
		self.ctx.move_to(0, 0)
		self.ctx.line_to(0, rackheight)
		self.ctx.stroke()
		#self.ctx.newpath()
		self.ctx.move_to(rackwidth, 0)
		self.ctx.line_to(rackwidth, rackheight)
		self.ctx.stroke()
		self.ctx.restore()

# 		# rack label
# 		self.ctx.save()
# 		self.ctx.findfont(self.ctx.quote("Helvetica-Bold"))
# 		self.ctx.scalefont(50)
# 		self.ctx.setfont()
# 		self.ctx.newpath()
# 		self.ctx.move_to(5, rackheight + 15)
# 		self.ctx.show("(%s)" % (rack._name,))
# 		self.ctx.restore()

		for y in range(0, rack.units):
			self.ctx.save()
			self.ctx.translate(0, y * unitsize)

			if rack._elements.has_key(y):
				e = rack._elements[y]
				self.visitRackElement(e, y)
			else:
				self.visitEmptyRackElement()

			self.ctx.restore()

# 		# rack stats
# 		self.ctx.save()
# 		size = 40
# 		self.ctx.translate(5, -20 - size)
# 		y = 0
# 		self.ctx.findfont(self.ctx.quote("Helvetica"))
# 		self.ctx.scalefont(size)
# 		self.ctx.setfont()
# 		for (k, v) in [("network port", rack.network),
# 					   ("power outlet", rack.power)
# 					   ]:
# 			self.ctx.newpath()
# 			self.ctx.move_to(0, y)
# 			self.ctx.show("(%s %s%s)" % (v, k, ["s", ""][v == 1]))
# 			y -= size
# 		for (k, v) in [("mm deep", rack.depth),
# 					   ]:
# 			self.ctx.newpath()
# 			self.ctx.move_to(0, y)
# 			self.ctx.show("(%s%s)" % (v, k))
# 			y -= size
# 		self.ctx.restore()

		# pop off the stack
		self.ctx.restore()

	def visitRackElement(self, element, pos):
		"""
		@param element the element to render
		@param pos position in the rack of this element
		"""

		if element is None:
			return

		if not isinstance(element, rack.Gap):
			# render the height bar on the left side of the rack
			self.ctx.save()
			self.ctx.set_source_rgba(0.6, 0.6, 0.6, 1)
			# reset frame of reference
			self.ctx.translate(-bracketwidth-barwidth, 0)
		
			#self.ctx.newpath()
			self.ctx.move_to(20, 0)
			self.ctx.line_to(20, element.units * unitsize)
			self.ctx.stroke()
			# top and bottom edges
			#self.ctx.newpath()
			self.ctx.move_to(10, 0)
			self.ctx.line_to(30, 0)
			self.ctx.stroke()
			#self.ctx.newpath()
			self.ctx.move_to(10, element.units * unitsize)
			self.ctx.line_to(30, element.units * unitsize)
			self.ctx.stroke()
			# arrowheads
			#self.ctx.newpath()
			self.ctx.move_to(15, 10)
			self.ctx.line_to(20, 0)
			self.ctx.line_to(25, 10)
			self.ctx.stroke()
			#self.ctx.newpath()
			self.ctx.move_to(15, element.units * unitsize - 10)
			self.ctx.line_to(20, element.units * unitsize)
			self.ctx.line_to(25, element.units * unitsize - 10)
			self.ctx.stroke()
			# size label
			self.ctx.set_source_rgba(0.5, 0.5, 0.5, 1.0)
			#self.ctx.newpath()
			self.ctx.move_to(5, element.units * unitsize / 2 - 7)
			self.ctx.save()
			self.ctx.scale(1, -1)
			self.ctx.text_path("%s" % (element.units,))
			self.ctx.fill_preserve()
			self.ctx.stroke()
			self.ctx.restore()
			self.ctx.restore()

			# draw rack unit position on the right hand side
			self.ctx.save()
			self.ctx.translate(rackwidth + bracketwidth, 0)
			self.ctx.set_source_rgba(0.5, 0.5, 0.5, 1)
			#self.ctx.newpath()
			self.ctx.move_to(5, 5)
			self.ctx.save()
			self.ctx.scale(1, -1)
			self.ctx.text_path("%s" % (pos+1,))
			self.ctx.fill_preserve()
			self.ctx.stroke()
			self.ctx.restore()
			self.ctx.restore()
		
		if isinstance(element, rack.Rackmount):
			if 'norackmount' not in self.options:
				self.visitRackmount(element)
			else:
				self.visitEmptyRackElement()
		elif isinstance(element, rack.PatchPanel):
			if 'nopatchpanel' not in self.options:
				self.visitPatchPanel(element)
			else:
				self.visitEmptyRackElement()
		elif isinstance(element, rack.CableManagement):
			if 'nocablemanagement' not in self.options:
				self.visitCableManagement(element)
			else:
				self.visitEmptyRackElement()
		elif isinstance(element, rack.Gap):
			self.visitGap(element)
		elif isinstance(element, rack.APC):
			if 'noapc' not in self.options:
				self.visitAPC(element)
			else:
				self.visitEmptyRackElement()
		elif isinstance(element, rack.Switch):
			if 'noswitch' not in self.options:
				self.visitSwitch(element)
			else:
				self.visitEmptyRackElement()
		elif isinstance(element, rack.Shelf):
			if 'noshelf' not in self.options:
				self.visitShelfArea(element)
			else:
				for i in range(pos, pos + element.units):
					_ = i
					self.visitEmptyRackElement()

	def visitEmptyRackElement(self):
		e = 5
		self.ctx.set_source_rgba(0.85, 0.85, 0.85, 1.0)
		#self.ctx.newpath()
		self.ctx.move_to(e, e)
		self.ctx.line_to(e, unitsize - e)
		self.ctx.line_to(rackwidth - e, unitsize - e)
		self.ctx.line_to(rackwidth - e, e)
		#self.ctx.closepath()
		self.ctx.fill()

	def visitRackmount(self, element):
		"""
		@param element the rackmount element
		"""

		self.ctx.save()
		self.ctx.set_source_rgba(0, 0, 0, 1)

		# outline of shape
		#self.ctx.newpath()
		self.ctx.move_to(0, 0)
		self.ctx.line_to(rackwidth, 0)
		self.ctx.line_to(rackwidth, element._units * unitsize)
		self.ctx.line_to(0, element._units * unitsize)
		#self.ctx.closepath()
		self.ctx.stroke()

		# label
		#self.ctx.newpath()
		self.ctx.move_to(5, element._units * unitsize - 14 - 5)
		self.ctx.save()
		self.ctx.scale(1, -1)
		if hasattr(element, 'label'):
			label = "%s (%s)" % (element.name, element.label)
		else:
			label = element.name
		self.ctx.text_path("%s" % (label,))
		self.ctx.fill_preserve()
		self.ctx.stroke()
		self.ctx.restore()

		self.visitShelfElements(element)
		
		self.ctx.restore()

	def visitPatchPanel(self, panel):
		"""
		@param panel the patchpanel element
		"""
		self.visitRackmount(panel)

	def visitAPC(self, apc):
		"""
		@param apc: the APC master switch
		"""
		self.visitRackmount(apc)

	def visitSwitch(self, switch):
		"""
		@param switch: the switch
		"""
		self.visitRackmount(switch)

		iconheight = 20
		iconwidth = 25
		offset = 7

		# draw switch icon
		self.ctx.save()
		self.ctx.set_source_rgba(0, 0, 0, 1)
		self.ctx.translate(rackwidth - iconwidth - 10, switch.units * unitsize - unitsize / 2.0 - (iconheight / 2.0))
		#self.ctx.newpath()
		self.ctx.move_to(0, 0)
		self.ctx.line_to(offset, 0)
		self.ctx.line_to(iconwidth - offset, iconheight)
		self.ctx.line_to(iconwidth, iconheight)
		self.ctx.stroke()
		#self.ctx.newpath()
		self.ctx.move_to(0, iconheight)
		self.ctx.line_to(offset, iconheight)
		self.ctx.line_to(iconwidth - offset, 0)
		self.ctx.line_to(iconwidth, 0)
		self.ctx.stroke()

		arr = 4
		# arrowheads
		#self.ctx.newpath()
		self.ctx.move_to(arr, arr)
		self.ctx.line_to(0, 0)
		self.ctx.line_to(arr, -arr)
		#self.ctx.closepath()
		self.ctx.fill()
		#self.ctx.newpath()
		self.ctx.move_to(arr, iconheight + arr)
		self.ctx.line_to(0, iconheight)
		self.ctx.line_to(arr, iconheight - arr)
		#self.ctx.closepath()
		self.ctx.fill()
		#self.ctx.newpath()
		self.ctx.move_to(iconwidth - arr, iconheight + arr)
		self.ctx.line_to(iconwidth, iconheight)
		self.ctx.line_to(iconwidth - arr, iconheight - arr)
		#self.ctx.closepath()
		self.ctx.fill()
		#self.ctx.newpath()
		self.ctx.move_to(iconwidth - arr, arr)
		self.ctx.line_to(iconwidth, 0)
		self.ctx.line_to(iconwidth - arr, -arr)
		#self.ctx.closepath()
		self.ctx.fill()
		self.ctx.restore()

	def visitGap(self, gap):
		for y in range(0, gap.units):
			self.ctx.save()
			self.ctx.translate(0, y * unitsize)
			self.visitEmptyRackElement()
			self.ctx.restore()

	def visitShelfArea(self, shelf):
		"""
		@param shelf the shelf element
		"""

		self.visitShelf(shelf)
		self.visitShelfElements(shelf)

	def visitShelfElements(self, shelf):
		x = 0
		for e in shelf._elements:
			# put each shelf element on the shelf, and move across so they
			# don't sit on top of each other
			self.ctx.save()
			print "drawing baseline of %s for %s" % (shelf._baseline, shelf.__class__.__name__)
			self.ctx.translate(x, shelf._baseline)

			self.visitShelfElement(e)

			x += e.width

			self.ctx.restore()

	def visitShelf(self, shelf):
		"""
		Draw the shelf shape
		"""

		rad = 5
		bh = shelf._bracketunits * unitsize

		for (gray, stroke) in [(0.6, self.ctx.fill), (0, self.ctx.stroke)]:
			self.ctx.set_source_rgba(gray, gray, gray, 1.0)
			#self.ctx.newpath()
			# start at the baseline which is relative to the bottom
			# of the rack unit
			self.ctx.move_to(0, shelf._baseline)
			# move up to the top of the mounting bracket
			self.ctx.line_to(0, bh)
			# move across to start the arc
			self.ctx.line_to(-bracketwidth + rad, bh)
			# top left arc
			self.ctx.arc(-bracketwidth + rad, bh - rad, rad, pi/2, pi)
			# left side gets drawn by magic
			# bottom left arc
			self.ctx.arc(-bracketwidth + rad, rad, rad, pi, 3*pi/2)
			# bottom edge of bracket
			self.ctx.line_to(0, 0)
			# now to bottom line of actual shelf
			self.ctx.line_to(0, shelf._bottomline)
			# across to other side of rack
			self.ctx.line_to(rackwidth, shelf._bottomline)
			# to bottom of rack unit
			self.ctx.line_to(rackwidth, 0)
			# now inverse of left side
			self.ctx.arc(rackwidth + bracketwidth - rad, rad, rad, 3*pi/2, 0)
			# right side for free
			# top right arc
			self.ctx.arc(rackwidth + bracketwidth - rad, bh - rad, rad, 0, pi/2)
			# close it off
			self.ctx.line_to(rackwidth, bh)
			self.ctx.line_to(rackwidth, shelf._baseline)
			#self.ctx.closepath()
			stroke()

	def visitShelfElement(self, element):
		"""
		@param element the element to render
		"""

		self.ctx.set_source_rgba(0, 0, 0, 1.0)
		#self.ctx.newpath()
		self.ctx.move_to(0, 0)
		self.ctx.line_to(element.width, 0)
		self.ctx.line_to(element.width, element.height)
		self.ctx.line_to(0, element.height)
		#self.ctx.closepath()
		self.ctx.stroke()

		# draw label
		#self.ctx.newpath()
		self.ctx.move_to(5, element.height - 14 - 5)
		self.ctx.save()
		self.ctx.scale(1, -1)
		if hasattr(element, 'label'):
			label = "%s (%s)" % (element.name, element.label)
		else:
			label = element.name
		self.ctx.text_path("%s" % (label,))
		self.ctx.fill_preserve()
		self.ctx.stroke()
		self.ctx.restore()

	def visitCableManagement(self, cman):
		"""
		@param cman: the cable management rack element
		"""

		self.ctx.save()
		self.ctx.set_source_rgba(0, 0, 0, 1.0)
		
		# draw outline
		#self.ctx.newpath()
		self.ctx.move_to(0, 0)
		self.ctx.line_to(rackwidth, 0)
		self.ctx.line_to(rackwidth, cman.units * unitsize)
		self.ctx.line_to(0, cman.units * unitsize)
		#self.ctx.closepath()
		self.ctx.stroke()

		# draw cable holding things
		for (fill, black) in [(self.ctx.fill, 0.5),  (self.ctx.stroke, 0)]:
			for x in [x * rackwidth / 16.0 for x in [3, 8, 13]]:
				self.ctx.save()
				self.ctx.set_source_rgba(black, black, black, 1.0)

				#self.ctx.newpath()
				self.ctx.move_to(x - 5, 0)
				self.ctx.line_to(x - 5, cman.units * unitsize / 2 - 5)
				self.ctx.line_to(x + 5, cman.units * unitsize / 2 - 5)
				self.ctx.line_to(x + 5, 0)
				#self.ctx.closepath()
				fill()

				#self.ctx.newpath()
				self.ctx.move_to(x - 5, cman.units * unitsize)
				self.ctx.line_to(x - 5, cman.units * unitsize / 2 + 5)
				self.ctx.line_to(x + 5, cman.units * unitsize / 2 + 5)
				self.ctx.line_to(x + 5, cman.units * unitsize)
				#self.ctx.closepath()
				fill()
			
				self.ctx.restore()

		self.ctx.restore()

if __name__ == '__main__':
	r = rack.Rack('rack asdfg', 47)
	sa = rack.Shelf2U(6)
	r.addElement(1, sa)
	r.addElement(8, rack.Rackmount(1, "rackmount 1"))
	r.addElement(10, rack.Rackmount(2, "rackmount 2"))

	r.addElement(13, rack.PatchPanel(1, "12p patch panel"))

	s = rack.Shelf1RU(3)
	r.addElement(15, s)

	sa.addElement(rack.Box(200, 100, "box A"))
	sa.addElement(rack.Box(150, 200, "box B"))

	s.addElement(rack.Box(100, 400, "box C"))
	
	print RackView().render(r)
