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

		self.ps.translate(72, 72)
		#self.ps.scale(0.3, 0.3)
		
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
		pass

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
	sa = rack.Shelf1RU(11)
	r.addElement(1, sa)
	print RackView().render(r)
