#!/usr/bin/python

class OverlapException:
	pass

class OutOfRackException:
	pass

class RackFullException:
	pass

class Rack:
	def __init__(self, name, units):
		self._name = name
		self.units = units

		self.affinity = "bottom"

		self._elements = {}

	def addElement(self, position, element):
		if position > self.units or position < 0:
			raise OutOfRackException
		if self._elements.has_key(position):
			raise OverlapException
		if element.units > 1:
			for i in range(position+1, position + element.units):
				if i > self.units or i < 0:
					raise OutOfRackException
				if self._elements.has_key(i):
					raise OverlapException

		# all ok, place the element
		self._elements[position] = element
		for i in range(position + 1, position + element.units):
			self._elements[i] = None

	def visit(self, visitor):
		visitor.visitRack(self)

	def _get_network(self):
		ports = 0
		for e in self._elements.keys():
			if self._elements[e] is not None:
				ports += self._elements[e].network
		return ports

	network = property(_get_network)

	def _get_units(self):
		return self._units

	def _set_units(self, value):
		self._units = int(value)

	units = property(_get_units, _set_units)

	def __iadd__(self, o):
		if self.affinity == "bottom":
			r = range(0, self.units - o.units + 1)
		else:
			r = range(self.units - o.units, 0, -1)

		for pos in r:
			if not self._elements.has_key(pos):
				try:
					for i in range(pos+1, pos + o.units):
						if self._elements.has_key(i):
							raise OverlapException
				except OverlapException:
					continue
				# all ok, place element
				for i in range(pos+1, pos+o.units):
					self._elements[i] = None
				self._elements[pos] = o
				break

		if o not in self._elements.values():
			raise RackFullException

		return self

	def update(self, d):
		self.__dict__.update(d)

class RackElement(object):
	def __init__(self, units=1, name="rack element", network=1, power=1, cliplock=4):
		self.units = units
		self.name = name
		self.networkports = network
		self.power = power
		self.cliplock = cliplock

	def visit(self, visitor):
		visitor.visitRackElement(self)

	def _get_units(self):
		return self._units

	def _set_units(self, value):
		self._units = int(value)

	units = property(_get_units, _set_units)

class Rackmount(RackElement):
	def __init__(self, units=1, name="rackmount", network=1, power=1, cliplock=1):
		RackElement.__init__(self, units, name, network, power, cliplock)

	def visit(self, visitor):
		visitor.visitRackmount(self)

class PatchPanel(RackElement):
	def __init__(self, units=1, name = "patch panel", network=0, power=0, cliplock=4):
		RackElement.__init__(self, units, name, network, power, cliplock)

	def visit(self, visitor):
		visitor.visitPatchPanel(self)

class CableManagement(RackElement):
	def __init__(self, units=1, name = "cable management", network=0, power=0, cliplock=4):
		RackElement.__init__(self, units, name, network, power, cliplock)

	def visit(self, visitor):
		visitor.visitCableManagement(self)

class Shelf(RackElement):
	def __init__(self, units=1, name = "shelf", network=0, power=0, cliplock=4, gap=0):
		RackElement.__init__(self, units, name, network, power, cliplock)

		self._elements = []
		self._baseline = 45
		self._bottomline = 0
		self._bracketunits = 1
		# hack to allow us to tell the builder if the elem above it has
		# enough space to allow things to go into its space
		self.gap = gap

	def addElement(self, element):
		self._elements.append(element)

	def visit(self, visitor):
		visitor.visitShelf(self)

	def _get_network(self):
		ports = self.network
		for e in self._elements:
			ports += e.network
		return ports

	network = property(_get_network)

	def __iadd__(self, o):
		self._elements.append(o)
		return self

	def _get_gap(self):
		return self.__gap

	def _set_gap(self, value):
		self.__gap = int(value)

	gap = property(_get_gap, _set_gap)

class Shelf1RU(Shelf):
	def __init__(self, units=1, name = "1RU shelf", network=0, power=0, cliplock=4, gap=0):
		Shelf.__init__(self, units, name, network, power, cliplock, gap)
		self._baseline = 35
		self._bottomline = 10
		self._bracketunits = 1

	def visit(self, visitor):
		visitor.visitShelf1RU(self)

class Shelf2U(Shelf):
	def __init__(self, units=2, name = "thin shelf w/ 30kg rating", network=0, power=0, cliplock=0, gap=0):
		Shelf.__init__(self, units, name, network, power, cliplock, gap)
		self._baseline = 0
		self._bottomline = -15
		self._bracketunits = 2

	def visit(self, visitor):
		visitor.visitShelf2U(self)

class ShelfElement(object):
	def __init__(self, height=0, width=0, name="shelf element", network=1, power=1, cliplock=0):
		self.width = width
		self.height = height
		self._name = name
		self.network = network
		self.power = power
		self.cliplock = cliplock

	def visit(self, visitor):
		visitor.visitShelfElement(self)

	def _get_height(self):
		return self.__height

	def _set_height(self, value):
		self.__height = float(value)

	height = property(_get_height, _set_height)

	def _get_width(self):
		return self.__width

	def _set_width(self, value):
		self.__width = float(value)

	width = property(_get_width, _set_width)

class Box(ShelfElement):
	def __init__(self, height=0, width=0, name = "box", network=1, power=1, cliplock=0):
		ShelfElement.__init__(self, height, width, name, network, power, cliplock)

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
