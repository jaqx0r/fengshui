#!/usr/bin/python

import rack

import string

class RackView:
	def __init__(self, name):
		self.options = []
		self.name = name

		# output variable
		self.o = []
		self.notes = []
		self.images = []
		self.checklist = []

	def render(self, thing):
		"""
		@param thing: the rack or rackarray to be drawn
		"""

		self.o.append("\\section{%s}" % (thing._name,))
		self.o.append("\\begin{multicols}{2}")
		self.o.append("\\includegraphics[height=\\textheight]{%s}" % (string.split(self.name, '.')[0],))
		self.o.append("\\columnbreak")

		# requirements
		#self.o.append("\\\\Requirements")
		#self.o.append("\\begin{itemize}")
		#for (k, v) in [("network port", thing.network),
		#			   ("power outlet", thing.power),
		#			   ]:
		#	self.o.append("\item %s %s%s" % (v, k, ["s", ""][v == 1]))
		#self.o.append("\\end{itemize}")

		# recurse
		for y in range(thing.units-1, -1, -1):
			if thing._elements.has_key(y):
				e = thing._elements[y]
				if e is not None:
					e.visit(self)

		# notes
		#self.o.append("\\subsubsection{Notes}")
		#self.o.append("{\\small")
		#if len(self.notes) > 0:
		#	self.o.append("\\begin{description}")
		#	self.o += self.notes
		#	self.o.append("\\end{description}")
		#self.o.append("}%end small")


		# checklist
		if len(self.checklist) > 0:
		    self.o.append("\\begin{center}")
		    self.o.append("{\\footnotesize")
		    self.o.append("\\begin{tabular}{r|c|c|c|c|c}")
		    self.o.append("&racked&net&pow&on&servs\\\\")
		    self.o.append("\\hline")
		    self.o += self.checklist
		    self.o.append("\\end{tabular}")
		    self.o.append("}%end footnotesize")
		    self.o.append("\\end{center}")

		# images
		self.o.append("\\begin{center}")
		self.o += self.images
		self.o.append("\\end{center}")
		
		self.o.append("\\end{multicols}")

		# spit out
		return string.join(self.o, "\n")

	def visitRackElement(self, e):
		if e.image != "":
			self.images.append("\\includegraphics[width=4cm]{%s}\\\\" % (e.image,))
		if e.notes != "":
			self.notes.append("\\item[%s] %s" % (e.name, e.notes))

		self.checklist.append("%s&&&&&\\\\\n\\hline" % (e.name,))

	def visitCableManagement(self, cman):
		pass

	def visitRackmount(self, rm):
		return self.visitRackElement(rm)

	def visitSwitch(self, sw):
		return self.visitRackElement(sw)

	def visitAPC(self, apc):
		return self.visitRackElement(apc)

	def visitGap(self, gap):
		pass

	def visitShelf(self, shelf):
		l = len(self.images)
		for e in shelf._elements:
			e.visit(self)
		if len(self.images) > l:
			self.images.append("\\\\")

	def visitShelf1RU(self, shelf):
		return self.visitShelf(shelf)

	def visitShelf2U(self, shelf):
		return self.visitShelf(shelf)

	def visitShelf1a(self, shelf):
		return self.visitShelf(shelf)

	def visitBox(self, box):
		if box.image != "":
			self.images.append("\\includegraphics[width=%smm]{%s}" % (box.width/11,box.image))
		if box.notes != "":
			self.notes.append("\\item[%s] %s" % (box._name, box.notes))
		self.checklist.append("%s&&&&&\\\\\n\\hline" % (box._name,))
