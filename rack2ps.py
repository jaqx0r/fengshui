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
		
	def render(self, thing):
		"""
		@param thing the rack or racks to be drawn
		"""
		# o is the output
		o = []

		if isinstance(thing, rack.RackArray):
			o += self.visitRackArray(thing)
		elif isinstance(thing, rack.Rack):
			o += self.visitRack(thing)
		else:
			raise RenderingDumbThingException

		output = "%!\n0.2 0.2 scale\n0 setgray\n"
		psv = postscript.PostScriptRenderer()
		for x in o:
			output += x.visit(psv)
		output += "showpage\n"
		return output

	def visitRackArray(self, racks):
		o = []

		for rack in racks._elements:
			o += self.visitRack(rack)

		return o

	def visitRack(self, rack):
		"""
		@param rack the rack being visited
		"""
		o = []

		o.append(postscript.NewPath())
		o.append(postscript.MoveTo(0, 0))
		o.append(postscript.LineTo(0, self._rackheight))
		o.append(postscript.LineTo(self._rackwidth, self._rackheight))
		o.append(postscript.LineTo(self._rackwidth, 0))
		o.append(postscript.ClosePath())
		o.append(postscript.Stroke())
				 
		for y in range(0, rack._units):
			if rack._elements.has_key(y):
				e = rack._elements[y]
				o += self.visitRackElement(e, y)
			else:
				o += self.visitEmptyRackElement()

		return o

	def visitRackElement(self, element, pos):
		"""
		@param element the element to render
		@param pos position in the rack of this element
		"""
		o = []
		if isinstance(element, rack.Rackmount):
			if 'norackmount' not in self.options:
				re = self.visitRackmount(element)
			else:
				re = self.visitEmptyRackElement()
		elif isinstance(element, rack.PatchPanel):
			if 'nopatchpanel' not in self.options:
				re = self.visitPatchPanel(element)
			else:
				re = self.visitEmptyRackElement()
		elif isinstance(element, rack.CableManagement):
			if 'nocablemanagement' not in self.options:
				re = self.visitPatchPanel(element)
			else:
				re = self.visitEmptyRackElement()
		elif isinstance(element, rack.Shelf):
			if 'noshelf' not in self.options:
				re = self.visitShelfArea(element)
			else:
				for i in range(pos, pos + element._units):
					_ = i
					re = self.visitEmptyRackElement()
		else:
			#re = self.visitEmptyRackElement(pos)
			re = None

		if re is not None:
			o += re

		return o

	def visitEmptyRackElement(self):
		o = []
		
		return o

	def visitRackmount(self, element):
		"""
		@param element the rackmount element
		"""
		o = []

		return o

	def visitPatchPanel(self, panel):
		"""
		@param panel the patchpanel element
		"""
		o = []

		return o

	def visitShelfArea(self, shelf):
		"""
		@param shelf the shelf element
		"""
		# o is the output
		o = []
		
		o.append(postscript.NewPath())
		o.append(postscript.MoveTo(0, 0))
		o.append(postscript.LineTo(self._rackwidth, 0))
		o.append(postscript.LineTo(self._rackwidth, self._unitsize * shelf._units))
		o.append(postscript.LineTo(0, self._unitsize * shelf._units))
		o.append(postscript.ClosePath())

		for e in shelf._elements:
			o += self.visitShelfElement(e)

		return o

	def visitShelf(self, shelf):
		o = []

		return o

	def visitShelfElement(self, element):
		"""
		@param element the element to render
		"""
		# o is the output
		o = []

		o.append(postscript.NewPath())

		o.append(postscript.MoveTo(0, 0))
		o.append(postscript.LineTo(element._width, 0))
		o.append(postscript.LineTo(element._width, element._height))
		o.append(postscript.LineTo(0, element._height))

		o.append(postscript.ClosePath())

		return o

if __name__ == '__main__':
	r = rack.Rack('rack', 47)
	print RackView().render(r)
