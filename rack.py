#!/usr/bin/python

class OverlapException:
	pass

class Rack:
	def __init__(self, name, units):
		self._name = name
		self._units = units

		self._elements = {}

	def addElement(self, position, element):
		if self._elements.has_key(position):
			raise OverlapException
		self._elements[position] = element
		if element._units > 1:
			for i in range(position+1, position + element._units):
				if self._elements.has_key(i):
					raise OverlapException
				self._elements[i] = None

class RackElement:
	def __init__(self, units, name = "rack element"):
		self._units = units
		self._name = name

class Rackmount(RackElement):
	def __init__(self, units, name = "rackmount"):
		RackElement.__init__(self, units, name)

class PatchPanel(RackElement):
	def __init__(self, units, name = "patch panel"):
		RackElement.__init__(self, units, name)

class Shelf(RackElement):
	def __init__(self, units, name = "shelf"):
		RackElement.__init__(self, units, name)

		self._elements = []
		self.baseline = 45
		self.bottomline = 0

	def addElement(self, element):
		self._elements.append(element)

class Shelf1RU(Shelf):
	def __init__(self, units, name = "1RU shelf w/ rails"):
		Shelf.__init__(self, units, name)
		self._baseline = 35
		self._bottomline = 10

class Shelf2U(Shelf):
	def __init__(self, units, name = "2U shelf w/ 30kg rating"):
		Shelf.__init__(self, units, name)
		self._baseline = 0
		self._bottomline = -15

class ShelfElement:
	def __init__(self, width, height, name = "shelf element"):
		self._width = width
		self._height = height
		self._name = name

class Box(ShelfElement):
	def __init__(self, width, height, name = "box"):
		ShelfElement.__init__(self, width, height, name)
