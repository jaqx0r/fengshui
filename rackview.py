#!/usr/bin/python

import xml.dom.minidom
import rack

class RackView:
	def __init__(self):
		# 47 rack units
		self._unitsize = 43
		self._rackheight = self._unitsize * 47
		self._rackwidth = 445

		self._imgheight = 2000
		self._imgwidth = self._imgheight * self._rackwidth / self._rackheight

		self._xpadding = 60
		self._ypadding = 25

		self._image = xml.dom.minidom.parseString("<svg/>")
		self._top = self._image.documentElement
		self._top.setAttribute("width", "%spx" % (self._imgwidth,))
		self._top.setAttribute("height", "%spx" % (self._imgheight,))
		self._top.setAttribute("viewBox", "0 0 %s %s" % (self._rackwidth + 2 * self._xpadding, self._rackheight + 2 * self._ypadding))

	def render(self, rack):
		"""
		@param rack the rack to be drawn
		"""

		# draw background
		self._top.appendChild(self._image.createComment("background"))
		bg = self._image.createElement("rect")
		self._top.appendChild(bg)
		bg.setAttribute("style", "fill:white;")
		bg.setAttribute("x", "0")
		bg.setAttribute("y", "0")
		bg.setAttribute("width", "%s" % (self._rackwidth + 2 * self._xpadding,))
		bg.setAttribute("height", "%s" % (self._rackheight + 2 * self._ypadding,))

		self._top.appendChild(self._image.createComment("rack"))
		r = self.visitRack(rack)
		self._top.appendChild(r)

		# offset the rack frame of reference
		r.setAttribute("transform", "translate(%s, %s)" % (self._xpadding, self._ypadding))

		return self._image.toprettyxml()

	def visitRack(self, rack):
		"""
		@param rack the rack being visited
		"""

		# r is our rack element
		r = self._image.createElement("g")
		title = self._image.createElement("title")
		title.appendChild(self._image.createTextNode("Rack"))
		r.appendChild(title)
		
		# draw the outline of the rack
		rect = self._image.createElement("rect")
		r.appendChild(rect)
		rect.setAttribute("x", "0")
		rect.setAttribute("y", "0")
		rect.setAttribute("width", "%s" % (self._rackwidth,))
		rect.setAttribute("height", "%s" % (self._rackheight,))
		rect.setAttribute("style", "fill:none;stroke:#777;")

		for y in range(0, rack._units):
			if rack._elements.has_key(y):
				e = rack._elements[y]
				re = self.visitRackElement(e, y)
				if e is not None:
					h = e._units
				else:
					h = 1
			else:
				re = self.visitEmptyRackElement(y)
				h = 1
			if re is not None:
				pos = rack._units - y - h
				r.appendChild(self._image.createComment("rack element at pos %s" % (y,)))
				r.appendChild(re)

				# move the rack element to the right position
				re.setAttribute("transform", "translate(0,%s)" % (pos * self._unitsize,))

		return r

	def visitRackElement(self, element, pos):
		"""
		@param element the element to render
		@param pos position in the rack of this element
		"""
		# e is our rack element
		e = self._image.createElement("g")
		title = self._image.createElement("title")
		title.appendChild(self._image.createTextNode("rack element"))
		e.appendChild(title)

		if isinstance(element, rack.Rackmount):
			re = self.visitRackmount(element)
		elif isinstance(element, rack.PatchPanel):
			re = self.visitPatchPanel(element)
		elif isinstance(element, rack.Shelf):
			re = self.visitShelfArea(element)
		else:
			re = None

		if re is not None:
			e.appendChild(re)
			for a in ("x", "y", "width", "height"):
				e.setAttribute(a, re.getAttribute(a))

			# side measurements
			measure = self._image.createElement("g")
			e.appendChild(measure)
			measure.setAttribute("style", "stroke:#777;")
			# upper horz line
			p1 = self._image.createElement("path")
			measure.appendChild(p1)
			p1.setAttribute("d", "M -30 0 -10 0")
			# lower horz line
			p2 = self._image.createElement("path")
			measure.appendChild(p2)
			p2.setAttribute("d", "M -30 %s -10 %s" % (self._unitsize * element._units, self._unitsize * element._units))
			# connecting line
			p3 = self._image.createElement("path")
			measure.appendChild(p3)
			p3.setAttribute("d", "M -20 0 -20 %s" % (self._unitsize * element._units,))
			# unit size label
			label = self._image.createElement("text")
			measure.appendChild(label)
			label.setAttribute("x", "-25")
			label.setAttribute("y", "%s" % (self._unitsize * element._units / 2.0 + self._unitsize * 0.25,))
			label.setAttribute("style", "fill:black;stroke:none;text-anchor:right;font-size:36pt;")
			label.appendChild(self._image.createTextNode("%s" % (element._units,)))

			# draw a position label right side of the rack
			label = self._image.createElement("text")
			re.appendChild(label)
			label.setAttribute("x", "%s" % (self._rackwidth + 10,))
			label.setAttribute("y", "%s" % (self._unitsize * element._units - 10,))
			label.setAttribute("style", "fill:black;stroke:none;text-anchor:left;font-size:%spx;" % (self._unitsize * 0.5,))
			label.appendChild(self._image.createTextNode("%s" % (pos,)))

		return e

	def visitEmptyRackElement(self, pos):

		# e is our rack element
		e = self._image.createElement("g")
		title = self._image.createElement("title")
		title.appendChild(self._image.createTextNode("Empty rack unit"))
		e.appendChild(title)
		
		rect = self._image.createElement("rect")
		e.appendChild(rect)
		# offset slightly
		rect.setAttribute("x", "5")
		rect.setAttribute("y", "2.5")
		# one rack unit high
		rect.setAttribute("height", "35")
		# width of the rack
		rect.setAttribute("width", "435")
		# funny colours
		rect.setAttribute("style", "fill:#CCC;stroke:none;")

		# draw a position label right side of the rack
		label = self._image.createElement("text")
		e.appendChild(label)
		label.setAttribute("x", "%s" % (self._rackwidth + 10,))
		label.setAttribute("y", "%s" % (self._unitsize - 10,))
		label.setAttribute("style", "fill:black;stroke:none;text-anchor:left;font-size:%spx;" % (self._unitsize * 0.5,))
		label.appendChild(self._image.createTextNode("%s" % (pos,)))


		return e

	def visitRackmount(self, element):
		"""
		@param element the rackmount element
		"""

		# e is our rack element
		e = self._image.createElement("g")
		title = self._image.createElement("title")
		title.appendChild(self._image.createTextNode("Rackmount element"))
		e.appendChild(title)

		rect = self._image.createElement("rect")
		e.appendChild(rect)

		rect.setAttribute("x", "0")
		rect.setAttribute("y", "0")
		rect.setAttribute("height", "%s" % (self._unitsize * element._units,))
		rect.setAttribute("width", "445")
		rect.setAttribute("style", "fill:none;stroke:black;")

		label = self._image.createElement("text")
		e.appendChild(label)
		label.appendChild(self._image.createTextNode(element._name))
		label.setAttribute("x", "20")
		label.setAttribute("y", "32")
		label.setAttribute("style", "text-anchor:left;font-size:30pt;")

		return e

	def visitPatchPanel(self, panel):
		"""
		@param panel the patchpanel element
		"""

		# e is our rack element
		e = self._image.createElement("g")
		title = self._image.createElement("title")
		title.appendChild(self._image.createTextNode("Patch Panel element"))
		e.appendChild(title)

		rect = self._image.createElement("rect")
		e.appendChild(rect)

		rect.setAttribute("x", "0")
		rect.setAttribute("y", "0")
		rect.setAttribute("height", "%s" % (self._unitsize * panel._units,))
		rect.setAttribute("width", "445")
		rect.setAttribute("style", "fill:none;stroke:black;")

		# add a label
		label = self._image.createElement("text")
		e.appendChild(label)
		label.appendChild(self._image.createTextNode(panel._name))
		label.setAttribute("x", "20")
		label.setAttribute("y", "32")
		label.setAttribute("style", "text-anchor:left;font-size:30pt;")

		return e

	def visitShelfArea(self, shelf):
		"""
		@param shelf the shelf element
		"""

		# e is our shelf area
		e = self._image.createElement("g")
		title = self._image.createElement("title")
		title.appendChild(self._image.createTextNode("Shelf area"))
		e.appendChild(title)

		e.setAttribute("style", "fill:none;stroke:black;")

		rect = self._image.createElement("rect")
		e.appendChild(rect)

		rect.setAttribute("x", "0")
		rect.setAttribute("y", "0")
		rect.setAttribute("height", "%s" % (self._unitsize * shelf._units,))
		rect.setAttribute("width", "%s" % (self._rackwidth,))

		if isinstance(shelf, rack.Shelf1RU):
			s = self.visitShelf1RU(shelf)
		elif isinstance(shelf, rack.Shelf2U):
			s = self.visitShelf2U(shelf)
		e.appendChild(s)
		# shift the shelf bit to the bottom of the area
		s.setAttribute("transform", "translate(0,%s)" % (self._unitsize * (shelf._units - 1),))

		xpos = 0
		for se in shelf._elements:
			e.appendChild(self._image.createComment("shelf element"))
			shelem = self.visitShelfElement(se)
			e.appendChild(shelem)

			# translate to the baseline of the shelf and flip upside down
			shelem.setAttribute("transform", "translate(%s,%s) scale(1,-1)" % (xpos, self._unitsize * (shelf._units - 1) + (self._unitsize - shelf._baseline)))

			# get width of this one
			w = int(shelem.getAttribute("width"))

			xpos += w

		return e

	def visitShelf1RU(self, shelf):
		"""
		1RU shelf visitor
		"""
		# e is our shelf
		e = self._image.createElement("g")
		title = self._image.createElement("title")
		title.appendChild(self._image.createTextNode("Shelf 1U"))
		e.appendChild(title)

		e.setAttribute("style", "fill:black;stroke:black;")

		# the rackline indicates the top of the rack unit
		rackline = self._image.createElement("path")
		e.appendChild(rackline)

		rackline.setAttribute("style", "stroke:#EEE;")
		rackline.setAttribute("d", "M 0 0 %s 0" % (self._rackwidth,))

		baseline = self._image.createElement("path")
		e.appendChild(baseline)

		baseline.setAttribute("d", "M 0 %s %s %s" % (self._unitsize - shelf._baseline, self._rackwidth, self._unitsize - shelf._baseline))

		bottomline = self._image.createElement("path")
		e.appendChild(bottomline)

		bottomline.setAttribute("d", "M 0 %s %s %s" % (self._unitsize - shelf._bottomline, self._rackwidth, self._unitsize - shelf._bottomline))

		# add a label
		label = self._image.createElement("text")
		e.appendChild(label)
		label.appendChild(self._image.createTextNode(shelf._name))
		label.setAttribute("x", "20")
		label.setAttribute("y", "32")
		label.setAttribute("style", "fill:black;stroke:none;text-anchor:left;font-size:30pt;")

		return e

	def visitShelf2U(self, shelf):
		"""
		2U shelf visitor
		"""
		# e is our shelf
		e = self._image.createElement("g")
		title = self._image.createElement("title")
		title.appendChild(self._image.createTextNode("Shelf 2U"))
		e.appendChild(title)

		e.setAttribute("style", "fill:black;stroke:black;")

		baseline = self._image.createElement("path")
		e.appendChild(baseline)

		baseline.setAttribute("d", "M 0 %s %s %s" % (self._unitsize - shelf._baseline, self._rackwidth, self._unitsize - shelf._baseline))

		bottomline = self._image.createElement("path")
		e.appendChild(bottomline)

		bottomline.setAttribute("d", "M 0 %s %s %s" % (self._unitsize - shelf._bottomline, self._rackwidth, self._unitsize - shelf._bottomline))

		# add a label
		label = self._image.createElement("text")
		e.appendChild(label)
		label.appendChild(self._image.createTextNode(shelf._name))
		label.setAttribute("x", "20")
		label.setAttribute("y", "%s" % (15 + self._unitsize,))
		label.setAttribute("style", "fill:black;stroke:none;text-anchor:left;font-size:20pt;")

		return e

	def visitShelfElement(self, element):
		"""
		@param element the element to render
		"""
		# e is our shelf element
		e = self._image.createElement("g")
		title = self._image.createElement("title")
		title.appendChild(self._image.createTextNode("shelf element"))
		e.appendChild(title)

		rect = self._image.createElement("rect")
		e.appendChild(rect)

		rect.setAttribute("x", "0")
		rect.setAttribute("y", "0")
		rect.setAttribute("width", "%s" % (element._width,))
		rect.setAttribute("height", "%s" % (element._height,))
		rect.setAttribute("style", "fill:none;stroke:black;")

		# hack to pass up width to parent
		e.setAttribute("width", "%s" % (element._width,))

		# add a label
		label = self._image.createElement("text")
		e.appendChild(label)
		label.appendChild(self._image.createTextNode(element._name))
		label.setAttribute("x", "0")
		label.setAttribute("y", "0")
		label.setAttribute("style", "fill:black;stroke:none;text-anchor:left;font-size:30pt;")
		# flip it right way up
		label.setAttribute("transform", "translate(20,%s) scale(1,-1)" % (element._height - 32,))

		return e
