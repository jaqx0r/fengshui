#!/usr/bin/python

import xml.dom.minidom
import rack

class RenderingDumbThingException:
	pass

class RackView:
	def __init__(self):
		# 47 rack units
		self._unitsize = 43.5
		self._rackheight = self._unitsize * 47
		self._rackwidth = 445

		self._imgheight = self._rackheight
		self._imgwidth = self._imgheight * self._rackwidth / self._rackheight

		self._xpadding = 100
		self._ypadding = 25

		self._image = xml.dom.minidom.parseString("<svg/>")
		self._top = self._image.documentElement
		self._top.setAttribute("xmlns", "http://www.w3.org/2000/svg")

	def render(self, thing):
		"""
		@param thing the rack or racks to be drawn
		"""

		# draw background
		self._top.appendChild(self._image.createComment("background"))
		bg = self._image.createElement("rect")
		self._top.appendChild(bg)
		bg.setAttribute("style", "fill:white;")
		bg.setAttribute("x", "0")
		bg.setAttribute("y", "0")

		if isinstance(thing, rack.Rack):
			self._top.appendChild(self._image.createComment("rack"))
			r = self.visitRack(thing)
			self._top.appendChild(r)

			# offset the rack frame of reference
			r.setAttribute("transform", "translate(%s, %s)" % (self._xpadding, self._ypadding))
		elif isinstance(thing, rack.RackArray):
			self._top.appendChild(self._image.createComment("rackarray"))
			r = self.visitRackArray(thing)
			self._top.appendChild(r)

			# offset the rack array frame of reference
			r.setAttribute("transform", "translate(%s, %s)" % (self._xpadding, self._ypadding))
		else:
			raise RenderingDumbThingException

		w = float(r.getAttribute("width"))
		h = float(r.getAttribute("height"))

		bg.setAttribute("width", "%s" % (w,))
		bg.setAttribute("height", "%s" % (h,))

		self._top.setAttribute("viewBox", "0 0 %s %s" % (w, h))

		#self._top.setAttribute("width", "%spx" % (w,))
		#self._top.setAttribute("height", "%spx" % (h,))

		self._top.setAttribute("width", "1010px")
		self._top.setAttribute("height", "650px")

		return self._image.toxml()

	def visitRackArray(self, racks):
		rs = self._image.createElement("g")
		title = self._image.createElement("title")
		title.appendChild(self._image.createTextNode("Rack Array"))
		rs.appendChild(title)

		xpos = 0
		height = 0
		
		for rack in racks._elements:
			self._top.appendChild(self._image.createComment("rack"))
			r = self.visitRack(rack)
			rs.appendChild(r)

			w = float(r.getAttribute("width")) + 2 * self._xpadding
			h = float(r.getAttribute("height")) + 2 * self._ypadding

			# offset the rack frame of reference
			r.setAttribute("transform", "translate(%s,0)" % (xpos,))
			xpos += w

			if h > height:
				height = h

		rs.setAttribute("width", "%s" % (xpos,))
		rs.setAttribute("height", "%s" % (height,))

		return rs

	def visitRack(self, rack):
		"""
		@param rack the rack being visited
		"""

		# r is our rack element
		r = self._image.createElement("g")
		title = self._image.createElement("title")
		title.appendChild(self._image.createTextNode("Rack"))
		r.appendChild(title)

		# draw a label
		lab = self._image.createElement("text")
		r.appendChild(lab)
		lab.appendChild(self._image.createTextNode(rack._name))
		lab.setAttribute("y", "37")
		lab.setAttribute("x", "20")
		lab.setAttribute("style", "font-family:sans-serif;font-size:40pt;")
		
		# draw the outline of the rack
		rect = self._image.createElement("rect")
		r.appendChild(rect)
		rect.setAttribute("x", "0")
		rect.setAttribute("y", "50")
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
				re.setAttribute("transform", "translate(0,%s)" % (pos * self._unitsize + 50,))

		r.setAttribute("width", "%s" % (self._rackwidth,))
		r.setAttribute("height", "%s" % (self._rackheight + 50,))

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
			measure.setAttribute("style", "fill:none;stroke:#555;")
			# upper horz line
			p1 = self._image.createElement("path")
			measure.appendChild(p1)
			p1.setAttribute("d", "M -50 0 L -30 0")
			# lower horz line
			p2 = self._image.createElement("path")
			measure.appendChild(p2)
			p2.setAttribute("d", "M -50 %s L -30 %s" % (self._unitsize * element._units, self._unitsize * element._units))
			# connecting line
			p3 = self._image.createElement("path")
			measure.appendChild(p3)
			p3.setAttribute("d", "M -40 0 L -40 %s" % (self._unitsize * element._units,))
			# unit size label
			label = self._image.createElement("text")
			measure.appendChild(label)
			label.setAttribute("x", "-%s" % (44 + len("%s" % (element._units,)) * 23,))
			label.setAttribute("y", "%s" % (self._unitsize * element._units / 2.0 + self._unitsize * 0.25,))
			label.setAttribute("style", "fill:black;stroke:none;font-family:sans-serif;font-size:28pt;")
			label.appendChild(self._image.createTextNode("%s" % (element._units,)))

			# draw a position label right side of the rack
			label = self._image.createElement("text")
			re.appendChild(label)
			label.setAttribute("x", "%s" % (self._rackwidth + 25,))
			label.setAttribute("y", "%s" % (self._unitsize * element._units - 10,))
			label.setAttribute("style", "fill:black;stroke:none;text-anchor:left;font-family:sans-serif;font-size:%spx;" % (self._unitsize * 0.5,))
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
		label.setAttribute("x", "%s" % (self._rackwidth + 25,))
		label.setAttribute("y", "%s" % (self._unitsize - 10,))
		label.setAttribute("style", "fill:black;stroke:none;text-anchor:left;font-family:sans-serif;font-size:%spx;" % (self._unitsize * 0.5,))
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
		label.setAttribute("style", "text-anchor:left;font-family:sans-serif;font-size:26pt;")

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
		label.setAttribute("style", "text-anchor:left;font-family:sans-serif;font-size:26pt;")

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

		rect = self._image.createElement("rect")
		e.appendChild(rect)

		rect.setAttribute("x", "0")
		rect.setAttribute("y", "0")
		rect.setAttribute("height", "%s" % (self._unitsize * shelf._units,))
		rect.setAttribute("width", "%s" % (self._rackwidth,))
		rect.setAttribute("style", "fill:none;stroke:none;")

		s = self.visitShelf(shelf)
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

	def visitShelf(self, shelf):
		# e is our shelf
		e = self._image.createElement("g")
		title = self._image.createElement("title")
		title.appendChild(self._image.createTextNode("Shelf 1U"))
		e.appendChild(title)

		e.setAttribute("style", "fill:black;stroke:black;")

		# draw the shelf
		sh = self._image.createElement("path")
		e.appendChild(sh)
		# there are 4 points in the left bracket
		# 4 points in the shelf, and 4 points in the right bracket
		sh.setAttribute("style", "fill:none;stroke:black;")
		# bracket width, height, radius
		bw = 15
		bh = shelf._bracketunits * self._unitsize
		rad = 2
		# d is the complete path of the shelf shape
		d = "M %s %s L %s %s %s %s A %s %s %s %s %s %s %s L %s %s A %s %s %s %s %s %s %s L %s %s %s %s %s %s %s %s %s %s A %s %s %s %s %s %s %s L %s %s A %s %s %s %s %s %s %s L %s %s %s %s %s %s" % (
			# start at the baseline, which is relative to the bottom of the
			# rack unit.  subtracted from self._unitsize which is the offset
			# of the bottom of the rack unit
			0, self._unitsize - shelf._baseline,
			# move up to the top of the mounting bracket
			0, self._unitsize - bh,
			# move back radius
			- bw + rad, self._unitsize - bh,
			# x, y radius
			rad, rad,
			# x axis rotation, large arc, sweep
			0, 0, 0,
			# and down to the point 5 units below the corner
			- bw, self._unitsize - bh + rad,
			# then down to the point 5 mm above the next corner
			- bw, self._unitsize - rad,
			# then the bottom arc
			rad, rad,
			0, 0, 0,
			# across to the bottom, radmm in
			- bw + rad, self._unitsize,
			# and in to the bottom of the rack unit
			0, self._unitsize,
			# now from the bottom, go to the bottomline
			0, self._unitsize - shelf._bottomline,
			# and zip across to the other size of the rack
			self._rackwidth, self._unitsize - shelf._bottomline,
			# down to the bottom of the rack unit
			self._rackwidth, self._unitsize,
			# now the rest is the arc path along the right hand bracket,
			# almost identical but opposite of the left bracket.
			self._rackwidth + bw - rad, self._unitsize,
			# arc radius
			rad, rad,
			0, 0, 0,
			self._rackwidth + bw, self._unitsize - rad,
			# line up
			self._rackwidth + bw, self._unitsize - bh + rad,
			# top arc
			rad, rad,
			0, 0, 0,
			self._rackwidth + bw - rad, self._unitsize - bh,
			# line inwards
			self._rackwidth, self._unitsize - bh,
			# line down to opposite point on baseline
			self._rackwidth, self._unitsize - shelf._baseline,
			# and we're done!
			0, self._unitsize - shelf._baseline)
		   
		sh.setAttribute("d", d)
		
		# add a label
		label = self._image.createElement("text")
		e.appendChild(label)
		label.appendChild(self._image.createTextNode(shelf._name))
		label.setAttribute("x", "20")
		# put label on bottomline
		label.setAttribute("y", "%s" % (self._unitsize - shelf._bottomline - 2,))
		label.setAttribute("style", "fill:black;stroke:none;text-anchor:left;font-family:sans-serif;font-size:20pt;")

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
		label.setAttribute("style", "fill:black;stroke:none;text-anchor:left;font-family:sans-serif;font-size:26pt;")
		# flip it right way up
		label.setAttribute("transform", "translate(20,%s) scale(1,-1)" % (element._height - 32,))

		return e
