#!/usr/bin/python

class Rack:
	def __init__(self, name, units):
		self._name = name
		self._units = units

		self._elements = {}

	def addElement(self, position, element):
		self._elements[position] = element
		if element._units > 1:
			for i in range(position+1, position + element._units):
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

	def addElement(self, element):
		self._elements.append(element)

class ShelfElement:
	pass

class Box(ShelfElement):
	pass
