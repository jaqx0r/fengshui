#!/usr/bin/python

class AST:
	def __init__(self, sourceposition):
		self.sourceposition = sourceposition

	def getPosition(self):
		return self.sourceposition

class Rack(AST):
	def __init__(self, name, elemlist, sourceposition):
		AST.__init__(self, sourceposition)
		self.name = name
		self.elemlist = elemlist

	def visit(self, visitor, obj):
		return visitor.visitRack(self, obj)

class List(AST):
	def __init__(self, sourceposition):
		AST.__init__(self, sourceposition)

class ElemList(List):
	def __init__(self, elem, elemlist, sourceposition):
		List.__init__(self, sourceposition)
		self.elem = elem
		self.elemlist = elemlist

	def visit(self, visitor, obj):
		return visitor.visitElemList(self, obj)

class EmptyElemList(List):
	def __init__(self, sourceposition):
		List.__init__(self, sourceposition)

	def visit(self, visitor, obj):
		return visitor.visitEmptyElemList(self, obj)

class Elem(AST):
	def __init__(self, sourceposition):
		AST.__init__(self, sourceposition)

class RackElem(Elem):
	def __init__(self, identifier, attributes, sourceposition):
		Elem.__init__(self, sourceposition)
		self.name = identifier
		self.attributes = attributes

	def visit(self, visitor, obj):
		return visitor.visitRackElem(self, obj)

class Shelf(Elem):
	def __init__(self, attributes, elemlist, sourceposition):
		Elem.__init__(self, sourceposition)
		self.attributes = attributes
		self.elemlist = elemlist

	def visit(self, visitor, obj):
		return visitor.visitShelf(self, obj)

class AttributeList(List):
	def __init__(self, attribute, list, sourceposition):
		List.__init__(self, sourceposition)
		self.attribute = attribute
		self.list = list

	def visit(self, visitor, obj):
		return visitor.visitAttributeList(self, obj)

class EmptyAttributeList(List):
	def __init__(self, sourceposition):
		List.__init__(self, sourceposition)

	def visit(self, visitor, obj):
		return visitor.visitEmptyAttributeList(self, obj)

class Attribute(AST):
	def __init__(self, name, value, sourceposition):
		AST.__init__(self, sourceposition)
		self.name = name
		self.value = value

	def visit(self, visitor, obj):
		return visitor.visitAttribute(self, obj)

class Terminal(AST):
	def __init__(self, value, sourceposition):
		AST.__init__(self, sourceposition)
		self.spelling = value

class Identifier(Terminal):
	def __init__(self, value, sourceposition):
		Terminal.__init__(self, value, sourceposition)

	def visit(self, visitor, obj):
		return visitor.visitIdentifier(self, obj)
