#!/usr/bin/python

from math import ceil

class OverlapException:
	pass

class OutOfRackException:
	pass

class RackFullException:
	pass

class Rack(object):
	def __init__(self, name, attr, units):
		self._name = name
		self.units = units

		self.affinity = "bottom"

		self._elements = {}

		self.__attributes = attr

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
		return visitor.visitRack(self)

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

	def _get_power(self):
		n = 0
		for e in self._elements.keys():
			if self._elements[e] is not None:
				n += self._elements[e].power
		return n

	power = property(_get_power)

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

	def _get_depth(self):
		if self.__attributes.has_key('depth'):
			return self.__attributes['depth']
		else:
			return 0

	def _set_depth(self, value):
		self.__attributes['depth'] = value

	depth = property(_get_depth, _set_depth)

class RackElement(object):
	def __init__(self, units=1, name="rack element", network=1, power=1, cliplock=4, image="", notes=""):
		self.units = units
		self.name = name
		self.network = network
		self.power = power
		self.cliplock = cliplock
		self.image = image
		self.notes = notes

	def visit(self, visitor):
		return visitor.visitRackElement(self)

	def _get_units(self):
		return self._units

	def _set_units(self, value):
		self._units = int(value)

	units = property(_get_units, _set_units)

	def _get_network(self):
		return self.__network

	def _set_network(self, value):
		self.__network = int(value)

	network = property(_get_network, _set_network)

	def _get_power(self):
		return self.__power

	def _set_power(self, value):
		self.__power = int(value)

	power = property(_get_power, _set_power)

class Rackmount(RackElement):
	def __init__(self, units=1, name="rackmount", network=1, power=1, cliplock=4, image="", notes=""):
		RackElement.__init__(self, units, name, network, power, cliplock, image, notes)

	def visit(self, visitor):
		return visitor.visitRackmount(self)

class APC(RackElement):
	def __init__(self, units=1, name="APC", network=1, power=1, cliplock=4, image=""):
		RackElement.__init__(self, units, name, network, power, cliplock, image)

	def visit(self, visitor):
		return visitor.visitAPC(self)

class PatchPanel(RackElement):
	def __init__(self, units=1, name = "patch panel", network=0, power=0, cliplock=4):
		RackElement.__init__(self, units, name, network, power, cliplock)

	def visit(self, visitor):
		return visitor.visitPatchPanel(self)

class CableManagement(RackElement):
	def __init__(self, units=1, name = "cable management", network=0, power=0, cliplock=4):
		RackElement.__init__(self, units, name, network, power, cliplock)

	def visit(self, visitor):
		return visitor.visitCableManagement(self)

class Gap(RackElement):
	def __init__(self, units=1, name="gap"):
		RackElement.__init__(self, units, name, 0, 0, 0)

	def visit(self, visitor):
		return visitor.visitGap(self)

class Switch(RackElement):
	def __init__(self, units=1, name="switch", network=1, power=1, cliplock=4, image="", notes=""):
		RackElement.__init__(self,
							 units,
							 name,
							 network,
							 power,
							 cliplock,
							 image,
							 notes)

	def visit(self, visitor):
		return visitor.visitSwitch(self)

class Shelf(RackElement):
	def __init__(self, units=1, name = "shelf", network=0, power=0, cliplock=4, gap=0, notes=""):
		RackElement.__init__(self, units, name, network, power, cliplock, notes)

		self._elements = []
		self._baseline = 43.5
		self._bottomline = 0
		self._bracketunits = 1
		# hack to allow us to tell the builder if the elem above it has
		# enough space to allow things to go into its space
		self.gap = gap

	def addElement(self, element):
		self._elements.append(element)

	def visit(self, visitor):
		return visitor.visitShelf(self)

	def _get_network(self):
		n = self.__network
		for e in self._elements:
			n += e.network
		return n

	def _set_network(self, value):
		self.__network = int(value)

	network = property(_get_network, _set_network)

	def _get_power(self):
		n = self.__power
		for e in self._elements:
			n += e.power
		return n

	def _set_power(self, value):
		self.__power = int(value)

	power = property(_get_power, _set_power)

	def __iadd__(self, o):
		self._elements.append(o)
		return self

	def _get_gap(self):
		return self.__gap

	def _set_gap(self, value):
		self.__gap = int(value)

	gap = property(_get_gap, _set_gap)

	def _get_units(self):
		h = 0
		for e in self._elements:
			if e.height > h:
				h = e.height
		h += self._baseline
		# XXX: hardcoded unit height
		u = int(ceil(h / 43.5))
		# evil hack
		u -= self.gap
		return u

	def _set_units(self, units):
		pass

	units = property(_get_units, _set_units)

class Shelf1RU(Shelf):
	def __init__(self, units=1, name = "1RU shelf", network=0, power=0, cliplock=4, gap=0, notes=""):
		Shelf.__init__(self, units, name, network, power, cliplock, gap, notes)
		self._baseline = 35
		self._bottomline = 10
		self._bracketunits = 1

	def visit(self, visitor):
		return visitor.visitShelf1RU(self)

class Shelf2U(Shelf):
	def __init__(self, units=2, name = "thin shelf w/ 30kg rating", network=0, power=0, cliplock=0, gap=0, notes=""):
		Shelf.__init__(self, units, name, network, power, cliplock, gap, notes)
		self._baseline = 0
		self._bottomline = -15
		self._bracketunits = 2

	def visit(self, visitor):
		return visitor.visitShelf2U(self)

class Shelf1a(Shelf):
	def __init__(self, units=1, name="1U shelf",network=0,power=0,cliplock=0,gap=0, notes=""):
		Shelf.__init__(self, units, name, network, power, cliplock, gap, notes)
		self._baseline = 28.5
		self._bottomline = 10
		self._bracketunits = 1

	def visit(self, visitor):
		return visitor.visitShelf1a(self)

class ShelfElement(object):
	def __init__(self, height=0, width=0, name="shelf element", network=1, power=1, cliplock=0, image="", notes=""):
		self.width = width
		self.height = height
		self._name = name
		self.network = network
		self.power = power
		self.cliplock = cliplock
		self.image = image
		self.notes = notes

	def visit(self, visitor):
		return visitor.visitShelfElement(self)

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

	def _get_network(self):
		return self.__network

	def _set_network(self, value):
		self.__network = int(value)
	
	network = property(_get_network, _set_network)

	def _get_power(self):
		return self.__power

	def _set_power(self, value):
		self.__power = int(value)
	
	power = property(_get_power, _set_power)

class Box(ShelfElement):
	def __init__(self, height=0, width=0, name = "box", network=1, power=1, cliplock=0, image="", notes=""):
		ShelfElement.__init__(self, height, width, name, network, power, cliplock, image, notes)

	def visit(self, visitor):
		return visitor.visitBox(self)

class RackArray:
	def __init__(self):
		self._elements = []
		
	def addElement(self, rack):
		self._elements.append(rack)

	def visit(self, visitor):
		return visitor.visitRackArray(self)

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
