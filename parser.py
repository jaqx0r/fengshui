#!/usr/bin/python

import sys

from scanner import *
from ast import *
from token import spell

class Parser:
	def __init__(self, scanner):
		self.scanner = scanner
		self.prevtokenposition = SourcePosition()
		self.currenttoken = self.scanner.getToken()
		#print "%s [%s]" % (spell(self.currenttoken.kind), self.currenttoken.spelling)

	def match(self, expected):
		if (self.currenttoken.kind == expected):
			self.accept()
		else:
			raise Exception, "%s: unexpected %s" % (self.currenttoken.sourceposition, self.currenttoken.spelling)

	def accept(self):
		self.prevtokenposition = self.currenttoken.sourceposition
		self.currenttoken = self.scanner.getToken()
		#print "%s [%s]" % (spell(self.currenttoken.kind), self.currenttoken.spelling)

	def start(self, position):
		position.linestart = self.currenttoken.sourceposition.linestart
		position.charstart = self.currenttoken.sourceposition.charstart

	def finish(self, position):
		position.linefinish = self.currenttoken.sourceposition.linefinish
		position.charfinish = self.currenttoken.sourceposition.charfinish

	def parse(self):
		return self.parseRack()

	def parseRack(self):
		sp = SourcePosition()
		self.start(sp)
		self.match(Token.RACK)
		i = self.parseIdentifier()
		self.match(Token.LCURLY)
		s = self.parseElemList()
		self.match(Token.RCURLY)
		self.finish(sp)
		d = Rack(i, s, sp)
		return d

	def parseElemList(self):
		sp = SourcePosition()
		self.start(sp)
		if self.currenttoken.kind != Token.RCURLY:
			if self.currenttoken.kind in (Token.LSQUARE, Token.ID, Token.SHELF):
				s = self.parseElem()
				l2 = self.parseElemList()
				self.finish(sp)
				l = ElemList(s, l2, sp)
			else:
				raise Exception
		else:
			self.finish(sp)
			l = EmptyElemList(sp)
		return l

	def parseElem(self):
		if self.currenttoken.kind == Token.LSQUARE:
			s = self.parseAttributeList()
		elif self.currenttoken.kind == Token.SHELF:
			s = self.parseShelf()
		elif self.currenttoken.kind == Token.ID:
			s = self.parseRackElemOrAttribute()
		return s

	def parseShelf(self):
		sp = SourcePosition()
		self.start(sp)

		self.match(Token.SHELF)
		self.match(Token.LCURLY)
		l = self.parseElemList()
		self.match(Token.RCURLY)
		
		self.finish(sp)
		s = Shelf(l, sp)
		return s

	def parseRackElemOrAttribute(self):
		sp = SourcePosition()
		self.start(sp)

		i = self.parseIdentifier()

		if self.currenttoken.kind == Token.EQUALS:
			self.accept()
			i2 = self.parseIdentifier()
			self.finish(sp)
			ra = Attribute(i, i2, sp)
		elif self.currenttoken.kind == Token.LSQUARE:
			a = self.parseAttributeList()
			self.finish(sp)
			ra = RackElem(i, a, sp)
		else:
			self.finish(sp)
			a = EmptyAttributeList(sp)
			ra = RackElem(i, a, sp)

		return ra

	def parseAttributeList(self):
		sp = SourcePosition()
		self.start(sp)
		self.match(Token.LSQUARE)
		if self.currenttoken.kind == Token.ID:
			al = self.parseProperAttributeList()
			self.match(Token.RSQUARE)
			self.finish(sp)
		elif self.currenttoken.kind == Token.RSQUARE:
			self.accept()
			self.finish(sp)
			al = EmptyAttributeList(sp)
		else:
			raise Exception
		return al

	def parseProperAttributeList(self):
		sp = SourcePosition()
		self.start(sp)
		a = self.parseAttribute()
		if self.currenttoken.kind == Token.COMMA:
			self.accept()
			l2 = self.parseProperAttributeList()
			self.finish(sp)
			l = AttributeList(a, l2, sp)
		else:
			self.finish(sp)
			l = AttributeList(a, EmptyAttributeList(sp), sp)
		return l

	def parseAttribute(self):
		sp = SourcePosition()
		self.start(sp)
		name = self.parseIdentifier()
		self.match(Token.EQUALS)
		value = self.parseIdentifier()
		self.finish(sp)
		a = Attribute(name, value, sp)
		return a
			
	def parseIdentifier(self):
		if self.currenttoken.kind == Token.ID:
			i = Identifier(self.currenttoken.spelling, self.currenttoken.sourceposition)
			self.accept()
		else:
			i = None
		return i

if __name__ == '__main__':
	import sys

	f = sys.argv[1]

	print f

	if f == "":
		f = "rack5.shui"
	
	ast = Parser(Scanner(SourceFile(f))).parse()
