#!/usr/bin/python

class PostScript:
	"""
	Level 1 PostScript rendering.
	"""
	def __init__(self):
		self.o = []
		self.indent = 0
		self.functions = ["moveto",
						  "lineto",
						  "rlineto",
						  "newpath",
						  "closepath",
						  "stroke",
						  "fill",
						  "clip",
						  "showpage",
						  "findfont",
						  "scalefont",
						  "setfont",
						  "show",
						  "rotate",
						  "translate",
						  "scale",
						  "charpath",
						  "setgray",
						  "setlinewidth"
						  ]
						  
						  
	def append(self, command):
		self.o.append(" " * self.indent + command)

	def gsave(self):
		self.append("gsave")
		self.indent += 2

	def grestore(self):
		self.indent -= 2
		self.append("grestore")

	def comment(self, comment):
		self.append("%% %s" % (comment,))

	def render(self):
		output = "%!\n"
		for line in self.o:
			output += line + "\n"
		output += "showpage\n"
		return output

	def quote(self, arg):
		"""quote the argument from expansion"""
		return "/" + arg

	def command(self, cmd, *args):
		self.append((("%s " * len(args)) % args) + cmd)

	def __getattr__(self, cmd):
		if cmd not in self.functions:
			raise AttributeError, "PostScript instance has no attribute '%s'" % (cmd,)
		r = lambda *args: self.command(cmd, *args)
		return r

if __name__ == '__main__':
	ps = PostScript()
	ps.comment("sample of printing text")
	ps.findfont(ps.quote("Times-Roman"))
	ps.scalefont(20)
	ps.setfont()
	ps.gsave()
	ps.newpath()
	ps.moveto(72, 72)
	ps.show("(Hello, world!)")
	ps.grestore()
	print ps.render()
