#!/usr/bin/python

import rack
import postscript

class RenderingDumbThingException(Exception):
	pass

class RackView:
	def __init__(self):
		self.options = []
		
		self._unitsize = 43.5
		
		self._rackheight = self._unitsize * 47
		self._rackwidth = 445

		self.ps = postscript.PostScript()
		
	def render(self, thing):
		"""
		@param thing the rack or racks to be drawn
		"""

		self.ps.setlinewidth(1)
		self.ps.setgray(0)
		self.ps.translate(72, 72)
		self.ps.scale(0.3, 0.3)
		
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

		self.ps.newpath()
		self.ps.moveto(0, 0)
		self.ps.lineto(0, self._rackheight)
		self.ps.lineto(self._rackwidth, self._rackheight)
		self.ps.lineto(self._rackwidth, 0)
		self.ps.closepath()
		self.ps.stroke()
				 
		for y in range(0, rack._units):
			if rack._elements.has_key(y):
				e = rack._elements[y]
				self.visitRackElement(e, y)
			else:
				self.visitEmptyRackElement()

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
		#else:
		#	#re = self.visitEmptyRackElement(pos)
		#	re = None

	def visitEmptyRackElement(self):
		pass

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
		self.ps.lineto(self._rackwidth, 0)
		self.ps.lineto(self._rackwidth, self._unitsize * shelf._units)
		self.ps.lineto(0, self._unitsize * shelf._units)
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
	print RackView().render(r)
