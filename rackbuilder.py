#!/usr/bin/python

import sys, string
from xml.dom import minidom, Node
import rack

class RackBuilder:
	def __init__(self):
		pass

	def build(self, dom):
		rootNode = dom.documentElement
		r = rack.Rack('rack', {}, 47)
		for attrName in rootNode.attributes.keys():
			aNode = rootNode.attributes.get(attrName)
			aValue = aNode.nodeValue
			setattr(r, attrName, aValue)
		for c in self.walk(rootNode):
			r += c
		return r

	def walk(self, parent):
		things = []
		for node in parent.childNodes:
			if node.nodeType == Node.ELEMENT_NODE:
				if node.nodeName == "rackmount":
					e = rack.Rackmount()
				elif node.nodeName == "cablemanagement":
					e = rack.CableManagement()
				elif node.nodeName == "switch":
					e = rack.Switch()
				elif node.nodeName == "shelf":
					e = rack.Shelf1RU()
					# Walk the child nodes.
					for c in self.walk(node):
						e += c
				elif node.nodeName == "box":
					e = rack.Box()
				else:
					raise NotImplementedError, "no handler for a %s" % node.nodeName
				
				attrs = node.attributes							 # [2]
				for attrName in attrs.keys():
					attrNode = attrs.get(attrName)
					attrValue = attrNode.nodeValue
					setattr(e, attrName, attrValue)
				things.append(e)
		# My, Earth sure has a lot of things.
		#print things
		return things

if __name__ == '__main__':
	dom = minidom.parse("example.feng")
	r = RackBuilder().build(dom)
	import rack2ps
	#print rack2ps.RackView("x").render(r)
