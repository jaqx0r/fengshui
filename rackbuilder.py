#!/usr/bin/python

import sys, string
from xml.dom import minidom, Node
import rack

class RackBuilder:
	def __init__(self):
		pass

	def build(self, dom):
		rootNode = dom.documentElement
		try:
			units = rootNode.attributes.get('units').nodeValue
		except AttributeError:
			units = 46
		r = rack.Rack('rack', {}, units)
		for attrName in rootNode.attributes.keys():
			aNode = rootNode.attributes.get(attrName)
			aValue = aNode.nodeValue
			try:
				setattr(r, attrName, aValue)
			except AttributeError, ex:
				print >> sys.stderr, "error setting %s to %s" % (attrName, aValue)
				raise ex
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
					e = rack.ShelfThin()
				elif node.nodeName == "box":
					e = rack.Box()
				elif node.nodeName == "apc":
					e = rack.APC()
				elif node.nodeName == "gap":
					e = rack.Gap()
				else:
					raise NotImplementedError, "no handler for a %s" % node.nodeName

				# Walk the child nodes.
				for c in self.walk(node):
					e += c

				try:
					print "element %s is %s units" % (e.__class__.__name__, e.units)
				except AttributeError:
					pass
				
				attrs = node.attributes							 # [2]
				for attrName in attrs.keys():
					attrNode = attrs.get(attrName)
					attrValue = attrNode.nodeValue
					try:
						setattr(e, attrName, attrValue)
					except AttributeError, ex:
						print >> sys.stderr, "error setting %s to %s" % (attrName, attrValue)
						raise ex
				things.append(e)
		# My, Earth sure has a lot of things.
		#print things
		return things

if __name__ == '__main__':
	dom = minidom.parse("example.feng")
	r = RackBuilder().build(dom)
	import rack2ps
	#print rack2ps.RackView("x").render(r)
