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
		#self.ps.scale(0.3, 0.3)

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
		for rack in racks._elements:
			self.visitRack(rack)

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
		self.ps.setgray(0.5)
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
		self.ps.setgray(0.75)
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
		pass

	def visitShelfArea(self, shelf):
		"""
		@param shelf the shelf element
		"""

		self.ps.newpath()
		self.ps.moveto(0, 0)
		self.ps.lineto(rackwidth, 0)
		self.ps.lineto(rackwidth, unitsize * shelf._units)
		self.ps.lineto(0, unitsize * shelf._units)
		self.ps.closepath()

		for e in shelf._elements:
			self.visitShelfElement(e)

	def visitShelf(self, shelf):
		pass

	def visitShelfElement(self, element):
		"""
		@param element the element to render
		"""
		self.ps.newpath()
		self.ps.moveto(0, 0)
		self.ps.lineto(element._width, 0)
		self.ps.lineto(element._width, element._height)
		self.ps.lineto(0, element._height)
		self.ps.closepath()

if __name__ == '__main__':
	r = rack.Rack('rack', 47)
	sa = rack.Shelf1RU(6)
	r.addElement(1, sa)
	r.addElement(8, rack.Rackmount(1, "rackmount 1"))
	r.addElement(10, rack.Rackmount(2, "rackmount 2"))
	print RackView().render(r)
