#!/usr/bin/python

import rack
import postscript

class RenderingDumbThingException(Exception):
	pass

unitsize = 43.5
rackwidth = 445
rackheight = unitsize * 47
bracketwidth = 15
barwidth = 40
bracketrad = 2

class RackView:
	def __init__(self):
		self.options = []
		self.ps = postscript.PostScript()
		
	def render(self, thing):
		"""
		@param thing the rack or racks to be drawn
		"""

		self.ps.translate(36, 36)
		self.ps.scale(0.3, 0.3)

		# set the font we're using for the whole picture
		self.ps.findfont(self.ps.quote("Helvetica-Bold"))
		self.ps.scalefont(20)
		self.ps.setfont()
		
		if isinstance(thing, rack.RackArray):
			self.visitRackArray(thing)
		elif isinstance(thing, rack.Rack):
			self.visitRack(thing)
		else:
			raise RenderingDumbThingException

		return self.ps.render()

	def visitRackArray(self, racks):
		x = 0
		for rack in racks._elements:
			self.ps.gsave()
			self.ps.translate(x, 0)
			self.visitRack(rack)
			self.ps.grestore()

			x += 2 * barwidth + 2 * bracketwidth + rackwidth + 5

	def visitRack(self, rack):
		"""
		@param rack the rack being visited
		"""

		# push the current stack
		self.ps.gsave()

		# move in by bar_area.width + mounting_bracket.width
		self.ps.translate(barwidth + bracketwidth, 0)

		# full outline of rack and brackets
		self.ps.gsave()
		self.ps.setgray(0.25)
		self.ps.newpath()
		self.ps.moveto(-bracketwidth, 0)
		self.ps.lineto(-bracketwidth, rackheight)
		self.ps.lineto(rackwidth + bracketwidth, rackheight)
		self.ps.lineto(rackwidth + bracketwidth, 0)
		self.ps.closepath()
		self.ps.stroke()
		# rack outline
		self.ps.newpath()
		self.ps.moveto(0, 0)
		self.ps.lineto(0, rackheight)
		self.ps.stroke()
		self.ps.newpath()
		self.ps.moveto(rackwidth, 0)
		self.ps.lineto(rackwidth, rackheight)
		self.ps.stroke()
		self.ps.grestore()

		# rack label
		self.ps.gsave()
		self.ps.findfont(self.ps.quote("Helvetica-Bold"))
		self.ps.scalefont(50)
		self.ps.setfont()
		self.ps.newpath()
		self.ps.moveto(5, rackheight + 15)
		self.ps.show("(%s)" % (rack._name,))
		self.ps.grestore()
				 
		for y in range(0, rack._units):
			self.ps.gsave()
			self.ps.translate(0, y * unitsize)

			if rack._elements.has_key(y):
				e = rack._elements[y]
				self.visitRackElement(e, y)
			else:
				self.visitEmptyRackElement()

			self.ps.grestore()

		# pop off the stack
		self.ps.grestore()

	def visitRackElement(self, element, pos):
		"""
		@param element the element to render
		@param pos position in the rack of this element
		"""

		if element is None:
			return
		
		# render the height bar on the left side of the rack
		self.ps.gsave()
		self.ps.setgray(0.6)
		# reset frame of reference
		self.ps.translate(-bracketwidth-barwidth, 0)
		
		self.ps.newpath()
		self.ps.moveto(20, 0)
		self.ps.lineto(20, element._units * unitsize)
		self.ps.stroke()
		# top and bottom edges
		self.ps.newpath()
		self.ps.moveto(10, 0)
		self.ps.lineto(30, 0)
		self.ps.stroke()
		self.ps.newpath()
		self.ps.moveto(10, element._units * unitsize)
		self.ps.lineto(30, element._units * unitsize)
		self.ps.stroke()
		# arrowheads
		self.ps.newpath()
		self.ps.moveto(15, 10)
		self.ps.lineto(20, 0)
		self.ps.lineto(25, 10)
		self.ps.stroke()
		self.ps.newpath()
		self.ps.moveto(15, element._units * unitsize - 10)
		self.ps.lineto(20, element._units * unitsize)
		self.ps.lineto(25, element._units * unitsize - 10)
		self.ps.stroke()
		# size label
		self.ps.setgray(0.5)
		self.ps.newpath()
		self.ps.moveto(5, element._units * unitsize / 2 - 7)
		self.ps.show("(%s)" % (element._units,))
		self.ps.grestore()

		# draw rack unit position on the right hand side
		self.ps.gsave()
		self.ps.translate(rackwidth + bracketwidth, 0)
		self.ps.setgray(0.5)
		self.ps.newpath()
		self.ps.moveto(5, 5)
		self.ps.show("(%s)" % (pos,))
		self.ps.grestore()
		
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
				self.visitPatchPanel(element)
			else:
				self.visitEmptyRackElement()
		elif isinstance(element, rack.Shelf):
			if 'noshelf' not in self.options:
				self.visitShelfArea(element)
			else:
				for i in range(pos, pos + element._units):
					_ = i
					self.visitEmptyRackElement()

	def visitEmptyRackElement(self):
		e = 5
		self.ps.setgray(0.85)
		self.ps.newpath()
		self.ps.moveto(e, e)
		self.ps.lineto(e, unitsize - e)
		self.ps.lineto(rackwidth - e, unitsize - e)
		self.ps.lineto(rackwidth - e, e)
		self.ps.closepath()
		self.ps.fill()

	def visitRackmount(self, element):
		"""
		@param element the rackmount element
		"""

		self.ps.gsave()
		self.ps.setgray(0)

		# outline of shape
		self.ps.newpath()
		self.ps.moveto(0, 0)
		self.ps.lineto(rackwidth, 0)
		self.ps.lineto(rackwidth, element._units * unitsize)
		self.ps.lineto(0, element._units * unitsize)
		self.ps.closepath()
		self.ps.stroke()

		# label
		self.ps.newpath()
		self.ps.moveto(5, element._units * unitsize - 14 - 5)
		self.ps.show("(%s)" % (element._name,))
		
		self.ps.grestore()

	def visitPatchPanel(self, panel):
		"""
		@param panel the patchpanel element
		"""
		self.visitRackmount(panel)

	def visitShelfArea(self, shelf):
		"""
		@param shelf the shelf element
		"""

		self.visitShelf(shelf)

		x = 0
		for e in shelf._elements:
			# put each shelf element on the shelf, and move across so they
			# don't sit on top of each other
			self.ps.gsave()
			self.ps.translate(x, shelf._baseline)
			
			self.visitShelfElement(e)

			x += e._width

			self.ps.grestore()

	def visitShelf(self, shelf):
		"""
		Draw the shelf shape
		"""

		rad = 5
		bh = shelf._bracketunits * unitsize

		for (gray, stroke) in [(0.6, self.ps.fill), (0, self.ps.stroke)]:
			self.ps.setgray(gray)
			self.ps.newpath()
			# start at the baseline which is relative to the bottom
			# of the rack unit
			self.ps.moveto(0, shelf._baseline)
			# move up to the top of the mounting bracket
			self.ps.lineto(0, bh)
			# move across to start the arc
			self.ps.lineto(-bracketwidth + rad, bh)
			# top left arc
			self.ps.arc(-bracketwidth + rad, bh - rad, rad, 90, 180)
			# left side gets drawn by magic
			# bottom left arc
			self.ps.arc(-bracketwidth + rad, rad, rad, 180, 270)
			# bottom edge of bracket
			self.ps.lineto(0, 0)
			# now to bottom line of actual shelf
			self.ps.lineto(0, shelf._bottomline)
			# across to other side of rack
			self.ps.lineto(rackwidth, shelf._bottomline)
			# to bottom of rack unit
			self.ps.lineto(rackwidth, 0)
			# now inverse of left side
			self.ps.arc(rackwidth + bracketwidth - rad, rad, rad, 270, 0)
			# right side for free
			# top right arc
			self.ps.arc(rackwidth + bracketwidth - rad, bh - rad, rad, 0, 90)
			# close it off
			self.ps.lineto(rackwidth, bh)
			self.ps.lineto(rackwidth, shelf._baseline)
			self.ps.closepath()
			stroke()

	def visitShelfElement(self, element):
		"""
		@param element the element to render
		"""
		self.ps.setgray(0)
		self.ps.newpath()
		self.ps.moveto(0, 0)
		self.ps.lineto(element._width, 0)
		self.ps.lineto(element._width, element._height)
		self.ps.lineto(0, element._height)
		self.ps.closepath()
		self.ps.stroke()

		# draw label
		self.ps.newpath()
		self.ps.moveto(5, element._height - 14 - 5)
		self.ps.show("(%s)" % (element._name,))

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
