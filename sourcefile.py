#!/usr/bin/python

class SourceFile:
	def __init__(self, filename):
		self.name = filename
		self.file = open(self.name)

	def getNextChar(self):
		c = self.file.read(1)
		if c == '':
			c = None
		return c

	def inspectChar(self, nthChar):
		c = self.file.read(nthChar)[-1]
		self.file.seek(-nthChar, 1)
		return c

	def mark(self):
		self.markpos = self.file.tell()

	def reset(self):
		self.file.seek(self.markpos, 0)

	def __str__(self):
		return self.name
