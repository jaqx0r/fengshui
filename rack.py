#!/usr/bin/python

class OverlapException:
	pass

class OutOfRackException:
	pass

class Rack:
	def __init__(self, name, units):
		self._name = name
		self._units = units

		self._elements = {}

	def addElement(self, position, element):
		if position > self._units or position < 0:
			raise OutOfRackException
		if self._elements.has_key(position):
			raise OverlapException
		self._elements[position] = element
		if element._units > 1:
			for i in range(position+1, position + element._units):
				if i > self._units or i < 0:
					raise OutOfRackException
				if self._elements.has_key(i):
					raise OverlapException
				self._elements[i] = None

	def visit(self, visitor):
		visitor.visitRack(self)

class RackElement:
	def __init__(self, units, name = "rack element"):
		self._units = units
		self._name = name

	def visit(self, visitor):
		visitor.visitRackElement(self)

class Rackmount(RackElement):
	def __init__(self, units, name = "rackmount"):
		RackElement.__init__(self, units, name)

	def visit(self, visitor):
		visitor.visitRackmount(self)

class PatchPanel(RackElement):
	def __init__(self, units, name = "patch panel"):
		RackElement.__init__(self, units, name)

	def visit(self, visitor):
		visitor.visitPatchPanel(self)

class CableManagement(RackElement):
	def __init__(self, units, name = "cable management"):
		RackElement.__init__(self, units, name)

	def visit(self, visitor):
		visitor.visitCableManagement(self)

class Shelf(RackElement):
	def __init__(self, units, name = "shelf"):
		RackElement.__init__(self, units, name)

		self._elements = []
		self._baseline = 45
		self._bottomline = 0
		self._bracketunits = 1

	def addElement(self, element):
		self._elements.append(element)

	def visit(self, visitor):
		visitor.visitShelf(self)

class Shelf1RU(Shelf):
	def __init__(self, units, name = "1RU shelf"):
		Shelf.__init__(self, units, name)
		self._baseline = 35
		self._bottomline = 10
		self._bracketunits = 1

	def visit(self, visitor):
		visitor.visitShelf1RU(self)

class Shelf2U(Shelf):
	def __init__(self, units, name = "thin shelf w/ 30kg rating"):
		Shelf.__init__(self, units, name)
		self._baseline = 0
		self._bottomline = -15
		self._bracketunits = 2

	def visit(self, visitor):
		visitor.visitShelf2U(self)

class ShelfElement:
	def __init__(self, height, width, name = "shelf element"):
		self._width = width
		self._height = height
		self._name = name

	def visit(self, visitor):
		visitor.visitShelfElement(self)

class Box(ShelfElement):
	def __init__(self, height, width, name = "box"):
		ShelfElement.__init__(self, height, width, name)

	def visit(self, visitor):
		visitor.visitBox(self)

class RackArray:
	def __init__(self):
		self._elements = []
		
	def addElement(self, rack):
		self._elements.append(rack)

	def visit(self, visitor):
		visitor.visitRackArray(self)

class RackVisitor:
	"""Base class for visitors to inherit from"""
	def __init__(self):
		pass

	def visit(self, ast):
		pass

	def visitRackArray(self, ast):
		pass

	def visitRack(self, ast):
		pass

	def visitRackElement(self, ast):
		pass

	def visitRackmount(self, ast):
		pass

	def visitPatchPanel(self, ast):
		pass

	def visitCableManagement(self, ast):
		pass

	def visitShelf(self, ast):
		pass

	def visitShelf1RU(self, ast):
		pass

	def visitShelf2U(self, ast):
		pass

	def visitShelfElement(self, ast):
		pass

	def visitBox(self, ast):
		pass
