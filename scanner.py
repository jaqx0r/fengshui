#!/usr/bin/python

from token import Token
from sourcefile import SourceFile
from sourceposition import SourcePosition

import string

class Scanner:
	def __init__(self, sourcefile):
		self.filestack = 0
		self.sourcefile = []
		self.sourcefile.append(sourcefile)
		self.currentchar = self.sourcefile[self.filestack].getNextChar()
		self.tokeninspected = None
		self.charpos = 1
		self.linepos = 1
		self.currentspelling = ""
		self.sourceposition = SourcePosition(self.linepos, self.charpos, self.charpos)
		self.incomment = False

	def inspectNextToken(self):
		currentchar = self.currentchar
		charpos = self.charpos
		linepos = self.linepos
		self.sourcefile[self.filestack].mark()
		self.tokeninspected = self.getToken()
		self.sourcefile[self.filestack].reset()
		self.linepos = linepos
		self.charpos = charpos
		self.currentchar = currentchar
		return self.tokeninspected

	def accept(self):
		if self.currentchar == '\n':
			self.charpos = 0
			self.linepos += 1
		if self.currentchar == '"':
			self.charpos += 1
		elif self.currentchar != '\n' and not self.incomment:
			self.currentspelling += self.currentchar
			self.sourceposition.charfinish = self.charpos
		if self.currentchar == '\t':
			self.charpos = ((self.charpos / 8) + 1) * 8 + 1
		else:
			self.charpos += 1
		self.currentchar = self.sourcefile[self.filestack].getNextChar()

	def inspectChar(self, nthchar):
		return self.sourcefile[self.filestack].inspectChar(nthchar)

	def nextToken(self):
		r = None
		if self.currentchar is None:
			r = Token.EOF
		elif self.currentchar == '{':
			self.accept()
			r = Token.LCURLY
		elif self.currentchar == '}':
			self.accept()
			r = Token.RCURLY
		elif self.currentchar == '[':
			self.accept()
			r = Token.LSQUARE
		elif self.currentchar == ']':
			self.accept()
			r = Token.RSQUARE
		elif self.currentchar == '=':
			self.accept()
			r = Token.EQUALS
		elif self.currentchar == ',':
			self.accept()
			r = Token.COMMA
		elif self.currentchar == ';':
			self.accept()
			r = Token.SEMICOLON
		elif self.currentchar == '-' and self.inspectChar(1) == '>':
			self.accept()
			self.accept()
			r = Token.ARROW
		elif self.currentchar == '"':
			self.accept()
			while self.currentchar != '"':
				self.accept()
			self.accept()
			r = Token.ID
		elif self.currentchar in string.digits + string.letters + '_':
			self.accept()
			while self.currentchar in string.digits + string.letters + '_-':
				self.accept()
			r = Token.ID
		return r

	def skipSpaceAndComments(self):
		self.incomment = False
		try:
			while (self.currentchar in string.whitespace) or (self.currentchar == '/' and self.inspectChar(1) == '*'):
				while self.currentchar in string.whitespace:
					self.accept()
				if self.currentchar == '/' and self.inspectChar(1) == '*':
					self.incomment = True
					self.accept()
					self.accept()
					while self.incomment:
						if self.currentchar == '*' and self.inspectChar(1) == '/':
							self.accept()
							self.accept()
							self.incomment = False
						else:
							self.accept()
		except TypeError:
			pass

	def getToken(self):
		if self.tokeninspected != None:
			tok = self.tokeninspected
			self.tokeninspected = None
			return tok
		self.skipSpaceAndComments()
		self.currentspelling = ""
		self.sourceposition = SourcePosition(self.linepos, self.linepos, self.charpos, self.charpos)
		kind = self.nextToken()
		#print self.currentspelling + "$"
		tok = Token(kind, self.currentspelling, self.sourceposition)
		return tok

if __name__ == '__main__':
	from scanner import Scanner
	from sourcefile import SourceFile
	from token import Token
	
	s = Scanner(SourceFile("anchor.feng"))

	t = s.getToken()
	while t.kind is not Token.EOF:
		print t
		t = s.getToken()
