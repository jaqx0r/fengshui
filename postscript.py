#!/usr/bin/python

class PostScriptRenderer:
	"""
	Level 1 PostScript renderer.
	"""
	def __init__(self):
		pass

	def render(self, ast):
		output = ast.visit(self)
		return output

	def visitPostScript(self, ast):
		output = "%!\n"
		for child in ast.children:
			output += child.visit(self)
		output += "showpage\n"
		return output

	def visitMoveTo(self, ast):
		output = "%s %s moveto\n" % (ast.src, ast.dst)
		return output

	def visitLineTo(self, ast):
		output = "%s %s lineto\n" % (ast.src, ast.dst)
		return output

	def visitNewPath(self, ast):
		output = "newpath\n"
		return output

	def visitClosePath(self, ast):
		output = "closepath\n"
		return output

	def visitStroke(self, ast):
		output = "stroke\n"
		return output

	def visitFindFont(self, ast):
		output = "%s findfont\n" % (ast.font,)
		return output

	def visitScaleFont(self, ast):
		output = "%s scalefont\n" % (ast.scale,)
		return output

	def visitSetFont(self, ast):
		output = "setfont\n"
		return output

	def visitShow(self, ast):
		output = "(%s) show\n" % (ast.text,)
		return output

class PostScript:
	def __init__(self):
		self.children = []

	def visit(self, visitor):
		return visitor.visitPostScript(self)

class MoveTo:
	def __init__(self, src, dst):
		self.src = src
		self.dst = dst

	def visit(self, visitor):
		return visitor.visitMoveTo(self)

class LineTo:
	def __init__(self, src, dst):
		self.src = src
		self.dst = dst

	def visit(self, visitor):
		return visitor.visitLineTo(self)

class NewPath:
	def __init__(self):
		pass

	def visit(self, visitor):
		return visitor.visitNewPath(self)

class ClosePath:
	def __init__(self):
		pass

	def visit(self, visitor):
		return visitor.visitClosePath(self)

class Stroke:
	def __init__(self):
		pass

	def visit(self, visitor):
		return visitor.visitStroke(self)

class FindFont:
	def __init__(self, font):
		self.font = font

	def visit(self, visitor):
		return visitor.visitFindFont(self)

class ScaleFont:
	def __init__(self, scale):
		self.scale = scale

	def visit(self, visitor):
		return visitor.visitScaleFont(self)

class SetFont:
	def __init__(self):
		pass

	def visit(self, visitor):
		return visitor.visitSetFont(self)

class Show:
	def __init__(self, text):
		self.text = text

	def visit(self, visitor):
		return visitor.visitShow(self)

if __name__ == '__main__':
	ps = PostScript()
	ps.children.append(NewPath())
	ps.children.append(MoveTo(72, 72))
	ps.children.append(LineTo(144, 72))
	ps.children.append(LineTo(144, 144))
	ps.children.append(LineTo(72, 144))
	ps.children.append(ClosePath())
	ps.children.append(Stroke())

	ps.children.append(FindFont("/Times-Roman"))
	ps.children.append(ScaleFont(20))
	ps.children.append(SetFont())
	ps.children.append(NewPath())
	ps.children.append(MoveTo(72, 200))
	ps.children.append(Show("Hello world!"))

	psr = PostScriptRenderer()
	print psr.render(ps)
