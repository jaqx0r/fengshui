#!/usr/bin/python

class PostScript:
	"""
	Level 1 PostScript rendering.
	"""
	def __init__(self):
		self.o = []
		self.indent = 0

	def append(self, command):
		self.o.append(" " * self.indent + command)

	def moveto(self, x, y):
		self.append("%s %s moveto" % (x, y))

	def lineto(self, x, y):
		self.append("%s %s lineto" % (x, y))

	def rlineto(self, x, y):
		self.append("%s %s rlineto" % (x, y))

	def gsave(self):
		self.append("gsave")
		self.indent += 2

	def grestore(self):
		self.indent -= 2
		self.append("grestore")

	def newpath(self):
		self.append("newpath")

	def closepath(self):
		self.append("closepath")

	def stroke(self):
		self.append("stroke")

	def fill(self):
		self.append("fill")

	def showpage(self):
		self.append("showpage")

	def findfont(self, font):
		self.append("/%s findfont" % (font,))

	def scalefont(self, scale):
		self.append("%s scalefont" % (scale,))

	def setfont(self):
		self.append("setfont")

	def show(self, text):
		self.append("(%s) show" % (text,))

	def rotate(self, ang):
		self.append("%s rotate" % (ang,))

	def translate(self, x, y):
		self.append("%s %s translate" % (x, y))

	def scale(self, x, y):
		self.append("%s %s scale" % (x, y))

	def clip(self):
		self.append("clip")

	def charpath(self, arg):
		self.append("%s charpath" % (arg,))

	def setgray(self, gray):
		self.append("%s setgray" % (gray,))

	def setlinewidth(self, linewidth):
		self.append("%s setlinewidth" % (linewidth,))

	def comment(self, comment):
		self.append("%% %s" % (comment,))

	def render(self):
		output = "%!\n"
		for line in self.o:
			output += line + "\n"
		return output

if __name__ == '__main__':
	ps = PostScript()
	ps.comment("sample of printing text")
	ps.findfont("Times-Roman")
	ps.scalefont(20)
	ps.setfont()
	ps.gsave()
	ps.newpath()
	ps.moveto(72, 72)
	ps.show("Hello, world!")
	ps.grestore()
	print ps.render()
