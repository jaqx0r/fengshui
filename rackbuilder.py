#!/usr/bin/python

from ast import *
import rack
import math

class RackBuilder:
	def __init__(self):
		pass

	def build(self, ast):
		return ast.visit(self, None)

	def visitRackArray(self, ast, obj):
		ra = rack.RackArray()
		
		return ast.racklist.visit(self, ra)

	def visitRackList(self, ast, obj):
		rack = ast.rack.visit(self, None)
		obj.addElement(rack)

		ast.racklist.visit(self, obj)

		return obj

	def visitEmptyRackList(self, ast, obj):
		pass

	def visitRack(self, ast, obj):
		name = ast.name.visit(self, obj)
		r = rack.Rack(name, 47)
		ast.name.visit(self, r)
		
		ast.elemlist.visit(self, r)

		return r

	def visitElemList(self, ast, obj):
		elem = ast.elem.visit(self, None)

		if hasattr(elem, 'has_key'):
			obj.update(elem)
		else:
			obj += elem

		ast.elemlist.visit(self, obj)

	def visitEmptyElemList(self, ast, obj):
		pass

	def visitShelf(self, ast, obj):
		attr = ast.attributes.visit(self, obj)

		if attr.has_key('type'):
			t = attr['type']
			del attr['type']
		else:
			t = "heavy"

		if t == "heavy":
			s = rack.Shelf1RU(**attr)
		elif t == "thin":
			s = rack.Shelf2U(**attr)

		ast.elemlist.visit(self, s)

		# work out how tall the shelf is
		h = 0
		for e in s._elements:
			if e.height > h:
				h = e.height
		h += s._baseline
		s.units = int(math.ceil(h / 43.5))

		# evil hack
		s.units -= s.gap
		
		return s

	def visitIdentifier(self, ast, obj):
		return ast.spelling

	def visitAttribute(self, ast, obj):
		a = {}
		key = ast.name.visit(self, obj)
		value = ast.value.visit(self, obj)
		a[key] = value
		return a

	def visitRackElem(self, ast, obj):
		name = ast.name.visit(self, obj)
		attr = ast.attributes.visit(self, obj)

		if attr.has_key('type'):
			t = attr['type']
			del attr['type']
		else:
			t = "rackmount"

		if attr.has_key('label'):
			attr['name'] = attr['label']
			del attr['label']
		else:
			attr['name'] = name

		if t == "rackmount":
			re = rack.Rackmount(**attr)
		elif t == "box":
			re = rack.Box(**attr)
		elif t == "switch":
			re = rack.Box(**attr)
		elif t == "cablemanagement":
			re = rack.CableManagement(**attr)
		return re

	def visitEmptyAttributeList(self, ast, obj):
		return {}

	def visitAttributeList(self, ast, obj):
		a = ast.attribute.visit(self, obj)
		a.update(ast.list.visit(self, obj))
		return a

if __name__ == '__main__':
	from parser import Parser
	from scanner import Scanner
	from sourcefile import SourceFile

	import sys
	try:
		f = sys.argv[1]
	except IndexError:
		f = "rack5.shui"
	ast = Parser(Scanner(SourceFile(f))).parse()
	rack = RackBuilder().build(ast)
	import rack2ps
	print rack2ps.RackView().render(rack)
